from fastapi import FastAPI, UploadFile, File, HTTPException
from prescription_authorization.agent import prescription_agent

app = FastAPI(
    title="Gemini Prescription Agent",
    version="1.0.0",
    description="Medical prescription OCR and data extraction service"
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "gemini-prescription-agent"}


@app.post("/ocr/text")
async def ocr_text(file: UploadFile = File(...)):
    """Extract raw text from prescription image"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        result = prescription_agent.process_prescription_bytes(
            image_bytes, filename=file.filename
        )
        return {
            "status": result["status"],
            "filename": result["filename"],
            "raw_text": result["raw_text"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/ocr/info")
async def ocr_info(file: UploadFile = File(...)):
    """Extract structured prescription information from image"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        return prescription_agent.process_prescription_bytes(
            image_bytes, filename=file.filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/ocr/summary")
async def ocr_summary(file: UploadFile = File(...)):
    """Extract prescription info and return formatted summary"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        result = prescription_agent.process_prescription_bytes(
            image_bytes, filename=file.filename
        )
        summary = prescription_agent.get_prescription_summary(result["structured"])
        return {
            "status": result["status"],
            "filename": result["filename"],
            "summary": summary,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
