import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, date
from app.models.processed_tickets import ProcessedTickets
from typing import Optional
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

def get_cards_service(db: Session):
    try:
        total = db.query(func.count(ProcessedTickets.id)).scalar()
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        daily = db.query(func.count(ProcessedTickets.id)).filter(
            ProcessedTickets.start_date >= start_of_day,
            ProcessedTickets.start_date <= end_of_day
        ).scalar()
        return {"total_tickets": total, "tickets_today": daily}
    except Exception as e:
        logger.error(f"Error in get_cards_service: {e}")
        raise

def get_categories_service(start_date: Optional[date], end_date: Optional[date], db: Session):
    try:
        query = db.query(
            ProcessedTickets.service_rating.label("category"),
            func.count(ProcessedTickets.id).label("quantity")
        )
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        results = query.group_by(ProcessedTickets.service_rating).all()
        categories = [
            {"category": r.category.lower(), "quantity": r.quantity} for r in results
        ]
        return categories
    except Exception as e:
        logger.error(f"Error in get_categories_service: {e}")
        raise

def get_emotions_service(start_date: Optional[date], end_date: Optional[date], db: Session):
    try:
        query = db.query(
            ProcessedTickets.sentiment_rating.label("emotion"),
            func.count(ProcessedTickets.id).label("quantity")
        )
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        results = query.group_by(ProcessedTickets.sentiment_rating).all()
        emotions = [
            {"emotion": r.emotion.lower(), "quantity": r.quantity} for r in results
        ]
        return emotions
    except Exception as e:
        logger.error(f"Error in get_emotions_service: {e}")
        raise

def get_daily_emotion_service(start_date: Optional[date], end_date: Optional[date], db: Session):
    try:
        query = db.query(
            func.date(ProcessedTickets.start_date).label("date"),
            ProcessedTickets.sentiment_rating,
            func.count().label("quantity")
        )
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        results = query.group_by(
            func.date(ProcessedTickets.start_date),
            ProcessedTickets.sentiment_rating
        ).order_by(func.date(ProcessedTickets.start_date)).all()

        daily = {}
        for r in results:
            date_str = r.date.isoformat()
            if date_str not in daily:
                daily[date_str] = {"date": date_str, "positivo": 0, "neutro": 0, "negativo": 0}
            emotion = r.sentiment_rating.lower()
            if emotion in daily[date_str]:
                daily[date_str][emotion] = r.quantity

        return list(daily.values())
    except Exception as e:
        logger.error(f"Error in get_daily_emotion_service: {e}")
        raise

def get_average_service_time_service(months: int, db: Session):
    try:
        query = db.query(
            func.date_trunc('month', ProcessedTickets.start_date).label("date"),
            func.avg(
                func.extract(
                    'epoch', ProcessedTickets.end_date - ProcessedTickets.start_date
                ) / 60
            ).label("avg_time")
        ).filter(ProcessedTickets.end_date.isnot(None))

        today = datetime.today()
        if months and months > 0:
            start_month = (today.replace(day=1) - relativedelta(months=months-1))
            query = query.filter(ProcessedTickets.start_date >= start_month)
        else:
            first_ticket = db.query(func.min(ProcessedTickets.start_date)).scalar()
            if first_ticket:
                start_month = first_ticket.replace(day=1)
                months = (today.year - start_month.year) * 12 + (today.month - start_month.month) + 1
            else:
                start_month = today.replace(day=1)
                months = 1

        results = query.group_by(func.date_trunc('month', ProcessedTickets.start_date))\
                       .order_by(func.date_trunc('month', ProcessedTickets.start_date)).all()

        result_dict = {r.date.date(): r.avg_time for r in results}

        months_list = [
            (today.replace(day=1) - relativedelta(months=i)).date()
            for i in reversed(range(months))
        ]

        avg_times = [
            {
                "date": m.isoformat(),
                "average_time": round(result_dict[m], 2) if m in result_dict and result_dict[m] is not None else 0
            }
            for m in months_list
        ]
        return avg_times
    except Exception as e:
        logger.error(f"Error in get_average_service_time_service: {e}")
        raise

def get_open_tickets_service(db: Session):
    try:
        count = db.query(func.count(ProcessedTickets.id)).filter(ProcessedTickets.end_date.is_(None)).scalar()
        return {"open_ticket_count": count}
    except Exception as e:
        logger.error(f"Error in get_open_tickets_service: {e}")
        raise
