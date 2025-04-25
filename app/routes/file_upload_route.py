from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.schemas.file_schema import FileCreateSchema
from app.services.file_upload_service import (
    upload_file_service,
    get_pending_files_service
)

router = APIRouter(prefix="/files", tags=["file-upload"])

@router.post("/upload")
def upload_file(file: FileCreateSchema, db: Session = Depends(get_db)):
    try:
        file_id = upload_file_service(file, db)
        return {"file_id": file_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving file to database")
    
@router.get("/pending-files")
def get_pending_files(db: Session = Depends(get_db)):
    try:
        pending_files = get_pending_files_service(db)
        return pending_files
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving pending files")

@router.get("/processed-files")
def get_processed_files(db: Session = Depends(get_db)):
    try:
        processed_files = get_pending_files_service(db)
        return processed_files
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving processed files")
