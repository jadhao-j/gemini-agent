"""
Example: Using the Prescription Agent directly in Python

This demonstrates how to use the PrescriptionAgent directly in your code
without going through the FastAPI endpoints.
"""

from prescription_authorization.agent import prescription_agent
import json


def example_process_from_file():
    """Example: Process prescription from a file path"""
    print("=" * 60)
    print("Example 1: Process Prescription from File")
    print("=" * 60)

    try:
        result = prescription_agent.process_prescription_file(
            "C:\\Users\\A\\Downloads\\WhatsApp Image 2026-02-28 at 6.01.36 PM.jpeg"
        )

        print(f"Status: {result['status']}")
        print(f"Filename: {result['filename']}")
        print(f"\nRaw Text:\n{result['raw_text']}\n")
        print(f"Structured Data:\n{json.dumps(result['structured'], indent=2)}\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def example_process_from_bytes():
    """Example: Process prescription from bytes"""
    print("=" * 60)
    print("Example 2: Process Prescription from Bytes")
    print("=" * 60)

    try:
        with open(
            "C:\\Users\\A\\Downloads\\WhatsApp Image 2026-02-28 at 6.01.36 PM.jpeg",
            "rb",
        ) as f:
            image_bytes = f.read()

        result = prescription_agent.process_prescription_bytes(
            image_bytes, filename="prescription.jpg"
        )

        print(f"Status: {result['status']}")
        print(f"Filename: {result['filename']}")
        print(f"\nStructured Data:\n{json.dumps(result['structured'], indent=2)}\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def example_get_summary():
    """Example: Get formatted prescription summary"""
    print("=" * 60)
    print("Example 3: Get Prescription Summary")
    print("=" * 60)

    try:
        # First process the prescription
        with open(
            "C:\\Users\\A\\Downloads\\WhatsApp Image 2026-02-28 at 6.01.36 PM.jpeg",
            "rb",
        ) as f:
            image_bytes = f.read()

        result = prescription_agent.process_prescription_bytes(
            image_bytes, filename="prescription.jpg"
        )

        # Get the summary
        summary = prescription_agent.get_prescription_summary(result["structured"])

        print(f"Patient: {summary['patient']}")
        print(f"Diagnosis: {summary['diagnosis']}")
        print(f"\nMedicines:")
        for med in summary["medicines"]:
            print(f"  - {med}")
        print(f"\nNotes: {summary['notes']}")
        print(f"Confidence: {summary['confidence']}")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def example_extract_medicines():
    """Example: Extract only medications from prescription"""
    print("=" * 60)
    print("Example 4: Extract Only Medicines")
    print("=" * 60)

    try:
        with open(
            "C:\\Users\\A\\Downloads\\WhatsApp Image 2026-02-28 at 6.01.36 PM.jpeg",
            "rb",
        ) as f:
            image_bytes = f.read()

        result = prescription_agent.process_prescription_bytes(image_bytes)
        medicines = result["structured"]["medicines"]

        print(f"Total medicines found: {len(medicines)}\n")
        for i, med in enumerate(medicines, 1):
            print(f"{i}. {med['name']}")
            print(f"   Dosage: {med['dosage']}")
            print(f"   Frequency: {med['frequency']}")
            print(f"   Duration: {med['duration']}")
            print(f"   Instructions: {med['instructions']}")
            print()

    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Uncomment the examples you want to run
    example_process_from_file()
    print("\n")
    example_get_summary()
    print("\n")
    example_extract_medicines()

    # example_process_from_bytes()
