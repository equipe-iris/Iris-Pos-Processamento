from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.services.dashboard_service import (
    get_total_tickets_service,
    get_tickets_by_date_service,
    get_categories_service,
    get_emotions_service,
    get_daily_emotion_service,
    get_average_service_time_service,
    get_daily_tickets_service
)
from typing import Optional
from app.utils.parse_date import parse_date

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/total-tickets")
def get_cards(db: Session = Depends(get_db)):
    try:
        result = get_total_tickets_service(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving total tickets data")

@router.get("/tickets")
def get_tickets_by_date(
    date: str = Query(..., description="Date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        parsed_date = parse_date(date)
        result = get_tickets_by_date_service(parsed_date, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving tickets by date data")

@router.get("/categories")
def get_categories(
    start_date: Optional[str] = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_categories_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving categories data")

@router.get("/emotions")
def get_emotions(
    start_date: Optional[str] = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_emotions_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving emotions data")

@router.get("/daily-emotion")
def get_daily_emotion(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_daily_emotion_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving daily emotion data")

@router.get("/average-service-time")
def get_average_service_time(
    months: int = Query(..., description="Number of months to calculate average service time. 0 for all time"),
    db: Session = Depends(get_db)
):
    try:
        result = get_average_service_time_service(months, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving average service time data")

@router.get("/daily-tickets")
def get_daily_tickets(
    start_date: Optional[str] = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        result = get_daily_tickets_service(start, end, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving daily tickets data")