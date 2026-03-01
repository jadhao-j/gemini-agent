# Prescription Authorization Agent - Usage Guide

## API Endpoints

### 1. Extract Raw Text
```bash
POST /ocr/text
```
Extracts raw text from prescription image without parsing.

**Example:**
```powershell
curl.exe -X POST "http://127.0.0.1:8000/ocr/text" `
  -F "file=@C:\path\to\prescription.jpg" `
  --max-time 60
```

**Response:**
```json
{
  "status": "success",
  "filename": "prescription.jpg",
  "raw_text": "Patient Name: John Doe\nDiagnosis: Fever\nRx. Medicine 500mg..."
}
```

---

### 2. Extract Structured Prescription Data
```bash
POST /ocr/info
```
Extracts and parses prescription into structured JSON format.

**Example:**
```powershell
curl.exe -X POST "http://127.0.0.1:8000/ocr/info" `
  -F "file=@C:\path\to\prescription.jpg" `
  --max-time 60
```

**Response:**
```json
{
  "status": "success",
  "filename": "prescription.jpg",
  "raw_text": "...",
  "structured": {
    "patient_name": "Dhananjay Ingole",
    "doctor_name": "",
    "registration_number": "",
    "prescription_date": "",
    "diagnosis": "URTI with allergic cough",
    "medicines": [
      {
        "name": "T. Azee 250",
        "dosage": "1",
        "frequency": "",
        "duration": "",
        "instructions": ""
      }
    ],
    "notes": "c/o :- fever, cough , allergic symptoms",
    "confidence": "high"
  }
}
```

---

### 3. Get Prescription Summary
```bash
POST /ocr/summary
```
Extracts prescription info and returns a formatted summary.

**Example:**
```powershell
curl.exe -X POST "http://127.0.0.1:8000/ocr/summary" `
  -F "file=@C:\path\to\prescription.jpg" `
  --max-time 60
```

**Response:**
```json
{
  "status": "success",
  "filename": "prescription.jpg",
  "summary": {
    "patient": "Dhananjay Ingole",
    "diagnosis": "URTI with allergic cough",
    "medicines": [
      "T. Azee 250 - 1",
      "T. Paracetamol 650 - 1"
    ],
    "notes": "c/o :- fever, cough , allergic symptoms",
    "confidence": "high"
  }
}
```

---

## Python Usage (Direct Agent Integration)

You can use the `PrescriptionAgent` directly in your Python code:

```python
from prescription_authorization.agent import prescription_agent

# Process prescription from file
result = prescription_agent.process_prescription_file(
    "path/to/prescription.jpg"
)
print(result)

# Process prescription from bytes
with open("path/to/prescription.jpg", "rb") as f:
    image_bytes = f.read()
    
result = prescription_agent.process_prescription_bytes(
    image_bytes, 
    filename="prescription.jpg"
)
print(result)

# Get formatted summary
structured = result["structured"]
summary = prescription_agent.get_prescription_summary(structured)
print(summary)
```

---

## Health Check

```bash
GET /health
```

Check if the service is running:

```powershell
curl.exe http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "gemini-prescription-agent"
}
```

---

## Interactive API Documentation

Open your browser and visit:
```
http://127.0.0.1:8000/docs
```

This provides an interactive Swagger UI where you can test all endpoints directly.

---

## Starting the Server

```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at:
- **API Base:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## Structured Output Format

The agent returns prescription data in this standardized format:

```python
{
    "patient_name": str,          # Patient's full name
    "doctor_name": str,           # Prescribing doctor's name
    "registration_number": str,   # Doctor's registration/license number
    "prescription_date": str,     # Date of prescription (e.g., "12/28/2025")
    "diagnosis": str,             # Medical diagnosis/chief complaint
    "medicines": [                # List of prescribed medications
        {
            "name": str,          # Medicine name
            "dosage": str,        # Dosage (e.g., "500mg")
            "frequency": str,     # Frequency (e.g., "twice daily")
            "duration": str,      # Duration (e.g., "7 days")
            "instructions": str   # Additional instructions
        }
    ],
    "notes": str,                 # Additional notes or observations
    "confidence": str             # Confidence level: "high", "medium", "low"
}
```

---

## Error Handling

**Common Errors:**

1. **Empty file** (status 400):
   ```
   "Uploaded file is empty"
   ```

2. **Wrong file format** (status 400):
   ```
   "Only image uploads are supported"
   ```

3. **Processing failed** (status 500):
   ```
   "Processing failed: {error details}"
   ```

---

## Notes

- Supported image formats: JPG, PNG, BMP, GIF, WEBP
- Maximum recommended image size: 10MB
- Processing time: 5-15 seconds per image (depends on image quality and Gemini API response time)
- Requires GEMINI_API_KEY in `.env` file
