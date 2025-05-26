from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional
from app.schemas.classification_results_schema import ClassificationResults
from app.schemas.semantic_search_schema import SemanticSearchSchema
from app.services.tickets_service import (
    classification_results_service,
    get_processed_tickets_service,
    get_open_tickets_service,
    get_closed_tickets_service,
    get_tickets_by_emotion_service,
    get_tickets_by_category_service,
    get_tickets_by_month_service,
    get_ticket_by_id_service,
    get_tickets_by_semantic_search_service
)
from app.utils.parse_date import parse_date
from app.utils.serialize_ticket import serialize_ticket
import requests


router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/processed-tickets")
def get_processed_tickets(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        processed_tickets = get_processed_tickets_service(start, end, db)
        return processed_tickets
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving processed tickets")


@router.post("/classification-results")
def classification_results(results: List[ClassificationResults], db: Session = Depends(get_db)):
    try:
        inserted_tickets = classification_results_service(results, db)
        tickets_payload = [serialize_ticket(t) for t in inserted_tickets]

        try:
            response = requests.post(
                "http://host.docker.internal:5000/semantic-search/sync",
                json={"tickets": tickets_payload},
                timeout=5
            )
            response.raise_for_status()
        except Exception as ex:
            print("Erro ao sincronizar", ex)
            raise HTTPException(status_code=500, detail=f"{ex}")
        
        return { "message": "Classification results saved successfully" }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving classification results {e}")
    
@router.get("/open-tickets")
def get_open_tickets(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_open_tickets_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving open tickets data")

@router.get("/closed-tickets")
def get_closed_tickets(
    start_date: Optional[str] = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_closed_tickets_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving closed tickets data")
    
@router.get("/tickets-by-emotion")
def get_tickets_by_emotion(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    emotion: str = Query(..., description="Emotion to filter by"),
    db: Session = Depends(get_db)
):
    start = parse_date(start_date)
    end = parse_date(end_date)
    try:
        result = get_tickets_by_emotion_service(start, end, emotion, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving tickets by emotion data")

@router.get("/tickets-by-category")
def get_tickets_by_category(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    category: str = Query(..., description="Category to filter by"),
    db: Session = Depends(get_db)
):
    start = parse_date(start_date)
    end = parse_date(end_date)
    try:
        result = get_tickets_by_category_service(start, end, category, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving tickets by category data")
    
@router.get("/tickets-by-month")
def get_tickets_by_month(
    month: str = Query(..., description="Month you want to retrieve in format MM-YYYY"),
    db: Session = Depends(get_db)
):
    try:
        result = get_tickets_by_month_service(month, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving tickets by month data")

@router.get("/by-id/{id}")
def get_ticket_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        ticket = get_ticket_by_id_service(id, db)
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving ticket by ID")
    
@router.post("/semantic-search")
def semantic_search(
    files_to_retrive: list[SemanticSearchSchema],
    db: Session = Depends(get_db)
):
    try:
        tickets = get_tickets_by_semantic_search_service(files_to_retrive, db)
        return tickets

    except Exception as ex:
        print("Erro ao buscar por tickets", ex)
        raise HTTPException(status_code=500, detail=f"{ex}"
)