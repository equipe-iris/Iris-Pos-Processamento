from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.services.dashboard_service import (
    get_cards_service,
    get_categories_service,
    get_satisfaction_score_service,
    get_daily_satisfaction_service,
    get_average_service_time_service,
    get_open_tickets_service
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/cards")
def get_cards(db: Session = Depends(get_db)):
    try:
        result = get_cards_service(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving cards data")

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    try:
        result = get_categories_service(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving categories data")

@router.get("/satisfaction-score")
def get_satisfaction_score(
    start_date: date = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: date = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        result = get_satisfaction_score_service(start_date, end_date, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving satisfaction score data")

@router.get("/daily-satisfaction")
def get_daily_satisfaction(
    start_date: date = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: date = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        result = get_daily_satisfaction_service(start_date, end_date, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving daily satisfaction data")

@router.get("/average-service-time")
def get_average_service_time(
    start_date: date = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: date = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        result = get_average_service_time_service(start_date, end_date, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving average service time data")

@router.get("/open-tickets")
def get_open_tickets(db: Session = Depends(get_db)):
    try:
        result = get_open_tickets_service(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving open tickets data")
