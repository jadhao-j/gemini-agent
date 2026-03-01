import os
import json
import re
from io import BytesIO
from typing import Any, Dict, List

from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, "..", ".."))

load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"))
load_dotenv(dotenv_path=os.path.join(MODULE_DIR, ".env"), override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?", "", stripped).strip()
        stripped = re.sub(r"```$", "", stripped).strip()
    return stripped


def _safe_json_loads(text: str) -> Dict[str, Any]:
    text = _strip_code_fence(text)
    return json.loads(text)


def _fallback_parse(raw_text: str) -> Dict[str, Any]:
    text = re.sub(r"\s+", " ", raw_text).strip()

    date_match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
    reg_match = re.search(r"\b(?:MH-\d{5}|DEA\s?#?:\s?\d{7}|NPI\s?#?:\s?\d{7}|\d{7})\b", text, re.IGNORECASE)

    med_pattern = re.compile(r"\b([A-Za-z][A-Za-z0-9-]{2,})\s+(\d{1,4}(?:-\d{1,4})?)\s?mg\b", re.IGNORECASE)
    medicines: List[Dict[str, str]] = []
    for m in med_pattern.finditer(raw_text):
        medicines.append(
            {
                "name": m.group(1),
                "dosage": f"{m.group(2)} mg",
                "frequency": "",
                "duration": "",
                "instructions": "",
            }
        )

    return {
        "patient_name": "",
        "doctor_name": "",
        "registration_number": reg_match.group(0) if reg_match else "",
        "prescription_date": date_match.group(0) if date_match else "",
        "diagnosis": "",
        "medicines": medicines,
        "notes": "",
        "confidence": "low",
    }


def _extract_raw_text(image: Image.Image) -> str:
    prompt = (
        "Extract all readable text from this prescription image exactly as written. "
        "Return plain text only."
    )
    response = gemini_model.generate_content([prompt, image])
    return (response.text or "").strip()


def extract_text_from_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    try:
        image = Image.open(image_path)
        return _extract_raw_text(image)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text using Gemini API: {e}")


def extract_text_from_bytes(image_bytes: bytes) -> str:
    try:
        image = Image.open(BytesIO(image_bytes))
        return _extract_raw_text(image)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text using Gemini API: {e}")


def extract_prescription_info_from_text(raw_text: str) -> Dict[str, Any]:
    prompt = (
        "You are a medical document parser. Convert the prescription text into strict JSON only. "
        "Use this exact schema with keys: "
        "patient_name, doctor_name, registration_number, prescription_date, diagnosis, "
        "medicines (array of objects with name,dosage,frequency,duration,instructions), notes, confidence. "
        "If a field is missing, return empty string; for medicines return empty array. "
        "Do not add extra keys.\n\n"
        f"Prescription text:\n{raw_text}"
    )

    try:
        response = gemini_model.generate_content(prompt)
        parsed = _safe_json_loads(response.text or "")
    except Exception:
        parsed = _fallback_parse(raw_text)

    required = {
        "patient_name": "",
        "doctor_name": "",
        "registration_number": "",
        "prescription_date": "",
        "diagnosis": "",
        "medicines": [],
        "notes": "",
        "confidence": "low",
    }
    for k, v in required.items():
        parsed.setdefault(k, v)

    if not isinstance(parsed.get("medicines"), list):
        parsed["medicines"] = []

    normalized_meds = []
    for med in parsed["medicines"]:
        if not isinstance(med, dict):
            continue
        normalized_meds.append(
            {
                "name": str(med.get("name", "")).strip(),
                "dosage": str(med.get("dosage", "")).strip(),
                "frequency": str(med.get("frequency", "")).strip(),
                "duration": str(med.get("duration", "")).strip(),
                "instructions": str(med.get("instructions", "")).strip(),
            }
        )
    parsed["medicines"] = normalized_meds
    return parsed


def extract_prescription_info_from_image_path(image_path: str) -> Dict[str, Any]:
    raw_text = extract_text_from_image(image_path)
    structured = extract_prescription_info_from_text(raw_text)
    return {"raw_text": raw_text, "structured": structured}


def extract_prescription_info_from_bytes(image_bytes: bytes) -> Dict[str, Any]:
    raw_text = extract_text_from_bytes(image_bytes)
    structured = extract_prescription_info_from_text(raw_text)
    return {"raw_text": raw_text, "structured": structured}
