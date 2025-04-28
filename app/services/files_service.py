from sqlalchemy.orm import Session
from app.models.tickets_files import TicketsFiles
from app.schemas.file_schema import FileCreateSchema, FileSchema
from app.utils.check_filename import check_filename
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List

def upload_file_service(file: FileCreateSchema, db: Session) -> int:
    isValid = check_filename(file.name)
    if not isValid:
        raise ValueError("Invalid file name.")
    
    try:
        db_file = TicketsFiles(
            name=file.name,
            upload_datetime=datetime.now(tz=ZoneInfo("America/Sao_Paulo")),
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file.id

    except Exception as e:
        db.rollback()
        raise Exception(e)
    
def get_pending_files_service(db: Session) -> List[FileSchema]:
    try:
        pending_files = db.query(TicketsFiles).filter(TicketsFiles.processing_status == False).all()
        return [FileSchema.model_validate(file) for file in pending_files]
    except Exception as e:
        print(f"Error retrieving pending files: {e}")
        raise Exception(e)
        

def get_processed_files_service(db: Session) -> List[FileSchema]:
    try:
        processed_files = db.query(TicketsFiles).filter(TicketsFiles.processing_status == True).all()
        return [FileSchema.model_validate(file) for file in processed_files]
    except Exception as e:
        print(f"Error retrieving processed files: {e}")
        raise Exception(e)


    

    
