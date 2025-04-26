from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.schemas.classification_results_schema import ClassificationResults
from app.services.tickets_service import (
    classification_results_service,
    get_processed_tickets_service
)


router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/processed-tickets")
def get_processed_tickets(db: Session = Depends(get_db)):
    try:
        processed_tickets = get_processed_tickets_service(db)
        return processed_tickets
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving processed tickets")


@router.post("/classification-results")
def classification_results(results: ClassificationResults, db: Session = Depends(get_db)):
    try:
        classification_results_service(results, db)
        return { "message": "Classification results saved successfully" }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving classification results")
    
    
