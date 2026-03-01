"""Prescription Authorization Agent - Main service for prescription processing"""

import os
from typing import Any, Dict, Union
from pathlib import Path

from prescription_authorization.models.ocr_engine import (
    extract_prescription_info_from_bytes,
    extract_prescription_info_from_image_path,
)


class PrescriptionAgent:
    """Main agent for processing prescriptions with structured output"""

    def __init__(self):
        self.name = "Prescription Authorization Agent"
        self.version = "1.0.0"

    def process_prescription_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a prescription image file and return structured data.
        
        Args:
            file_path: Path to the prescription image file
            
        Returns:
            Dictionary with raw_text and structured prescription data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prescription file not found: {file_path}")

        result = extract_prescription_info_from_image_path(file_path)
        return {
            "status": "success",
            "filename": Path(file_path).name,
            "raw_text": result["raw_text"],
            "structured": result["structured"],
        }

    def process_prescription_bytes(
        self, image_bytes: bytes, filename: str = "prescription.jpg"
    ) -> Dict[str, Any]:
        """
        Process prescription image from bytes and return structured data.
        
        Args:
            image_bytes: Image data as bytes
            filename: Optional filename for reference
            
        Returns:
            Dictionary with raw_text and structured prescription data
        """
        if not image_bytes:
            raise ValueError("Image bytes cannot be empty")

        result = extract_prescription_info_from_bytes(image_bytes)
        return {
            "status": "success",
            "filename": filename,
            "raw_text": result["raw_text"],
            "structured": result["structured"],
        }

    def get_prescription_summary(
        self, structured_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a summary of the structured prescription data.
        
        Args:
            structured_data: Structured prescription data
            
        Returns:
            Formatted summary dictionary
        """
        medicines_list = []
        for med in structured_data.get("medicines", []):
            med_info = f"{med.get('name', 'Unknown')}"
            if med.get("dosage"):
                med_info += f" - {med.get('dosage')}"
            if med.get("frequency"):
                med_info += f" ({med.get('frequency')})"
            medicines_list.append(med_info)

        return {
            "patient": structured_data.get("patient_name", "Unknown"),
            "diagnosis": structured_data.get("diagnosis", "Not specified"),
            "medicines": medicines_list,
            "notes": structured_data.get("notes", ""),
            "confidence": structured_data.get("confidence", "low"),
        }


# Global agent instance
prescription_agent = PrescriptionAgent()
