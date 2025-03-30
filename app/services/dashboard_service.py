import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, date
from app.models import ProcessedTickets

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

def get_categories_service(db: Session):
    try:
        results = db.query(
            ProcessedTickets.service_rating.label("category"),
            func.count(ProcessedTickets.id).label("quantity")
        ).group_by(ProcessedTickets.service_rating).all()
        categories = [
            {"category": r.category.lower(), "quantity": r.quantity} for r in results
        ]
        return categories
    except Exception as e:
        logger.error(f"Error in get_categories_service: {e}")
        raise

def get_satisfaction_score_service(start_date: date, end_date: date, db: Session):
    try:
        current_datetime = datetime.now()
        filter_start = datetime.combine(start_date, datetime.min.time())
        filter_end = datetime.combine(end_date, datetime.max.time())
        tickets = db.query(ProcessedTickets).filter(
            ProcessedTickets.start_date >= filter_start,
            func.coalesce(ProcessedTickets.end_date, current_datetime) <= filter_end
        ).all()
        total = len(tickets)
        if total == 0:
            return {"score": 0, "ticket_count": 0}
        positive = sum(1 for t in tickets if t.sentiment_rating.lower() == "positivo")
        neutral = sum(1 for t in tickets if t.sentiment_rating.lower() == "neutro")
        negative = sum(1 for t in tickets if t.sentiment_rating.lower() == "negativo")
        weighted_sum = positive * 50 + neutral * 30 + negative * 20
        score = (weighted_sum / (total * 50)) * 100
        return {"score": round(score, 2), "ticket_count": total}
    except Exception as e:
        logger.error(f"Error in get_satisfaction_score_service: {e}")
        raise

def get_daily_satisfaction_service(start_date: date, end_date: date, db: Session):
    try:
        current_datetime = datetime.now()
        filter_start = datetime.combine(start_date, datetime.min.time())
        filter_end = datetime.combine(end_date, datetime.max.time())
        subquery = db.query(
            func.date(func.coalesce(ProcessedTickets.end_date, func.current_date())).label("date"),
            ProcessedTickets.sentiment_rating
        ).filter(
            ProcessedTickets.start_date >= filter_start,
            func.coalesce(ProcessedTickets.end_date, current_datetime) <= filter_end
        ).subquery()
        results = db.query(
            subquery.c.date,
            func.count().label("total"),
            func.sum(case((subquery.c.sentiment_rating.ilike("positivo"), 1), else_=0)).label("positive"),
            func.sum(case((subquery.c.sentiment_rating.ilike("neutro"), 1), else_=0)).label("neutral"),
            func.sum(case((subquery.c.sentiment_rating.ilike("negativo"), 1), else_=0)).label("negative"),
        ).group_by(subquery.c.date).order_by(subquery.c.date).all()
        daily = []
        for r in results:
            total = r.total
            weighted_sum = r.positive * 50 + r.neutral * 30 + r.negative * 20
            score = (weighted_sum / (total * 50)) * 100 if total > 0 else 0
            daily.append({
                "date": r.date.isoformat(),
                "score": round(score, 2),
                "ticket_count": total
            })
        return daily
    except Exception as e:
        logger.error(f"Error in get_daily_satisfaction_service: {e}")
        raise

def get_average_service_time_service(db: Session):
    try:
        results = db.query(
            func.date(ProcessedTickets.start_date).label("date"),
            func.avg(
                func.extract(
                    'epoch', func.coalesce(ProcessedTickets.end_date, func.now()) - ProcessedTickets.start_date
                ) / 60
            ).label("avg_time")
        ).group_by(func.date(ProcessedTickets.start_date)).order_by(func.date(ProcessedTickets.start_date)).all()
        avg_times = [
            {"date": r.date.isoformat(), "average_time": round(r.avg_time, 2) if r.avg_time is not None else None}
            for r in results
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
