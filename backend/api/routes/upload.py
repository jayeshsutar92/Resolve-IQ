from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
import pypdf
from services.workflow_service import WorkflowService
from api.dependencies import get_workflow_service
from schemas.chat import ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def upload_document(
    file: UploadFile = File(...),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF and TXT files are supported.")
        
    text = ""
    try:
        content = await file.read()
        if file.content_type == "application/pdf":
            from io import BytesIO
            pdf_reader = pypdf.PdfReader(BytesIO(content))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        else:
            text = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to read file: {e}")

    if not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No readable text found in document.")

    return await workflow_service.process_document(document_text=text)
