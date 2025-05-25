from app.schemas.classification_results_schema import ClassificationResults
from app.schemas.tickets_schema import TicketSchema
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.processed_tickets import ProcessedTickets
from app.models.tickets_files import TicketsFiles
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Optional
from datetime import date
from calendar import monthrange

def safe_parse_date(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None

def classification_results_service(results_list: List[ClassificationResults], db: Session):
    try:
        tickets_data = []
        for results in results_list:
            tickets_data.extend([
                {
                    "original_id": ticket.id,
                    "title": ticket.title,
                    "service_rating": ticket.service_rating,
                    "sentiment_rating": ticket.sentiment_rating,
                    "start_date": safe_parse_date(ticket.start_date),
                    "end_date": safe_parse_date(ticket.end_date),
                    "file_id": results.file_id
                }
                for ticket in results.processed_tickets
            ])

        db.bulk_insert_mappings(ProcessedTickets, tickets_data)
        db.commit()

    except Exception as e:
        print(f"Error saving classification results: {e}")

    finally:
        try:
            for results in results_list:
                file = db.query(TicketsFiles).filter(TicketsFiles.id == results.file_id).first()
                if file:
                    file.processing_status = True
                    file.finished_at = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
            db.commit()
        except Exception as update_error:
            print(f"Error updating file status: {update_error}")

def get_processed_tickets_service(start_date: Optional[date], end_date: Optional[date], db: Session) -> List[TicketSchema]:
    try:
        query = db.query(ProcessedTickets)
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        processed_tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in processed_tickets]
    except Exception as e:
        print(f"Error retrieving processed tickets: {e}")
        raise Exception(e)
    
def get_open_tickets_service(start_date: Optional[date], end_date: Optional[date], db: Session) -> List[TicketSchema]:
    try:
        query = db.query(ProcessedTickets).filter(ProcessedTickets.end_date.is_(None))
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        open_tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in open_tickets]
    except Exception as e:
        print(f"Error in get_open_tickets_service: {e}")
        raise

def get_closed_tickets_service(start_date: Optional[date], end_date: Optional[date], db: Session) -> List[TicketSchema]:
    try:
        query = db.query(ProcessedTickets).filter(ProcessedTickets.end_date.is_not(None))
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        open_tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in open_tickets]
    except Exception as e:
        print(f"Error in get_closed_tickets_service: {e}")
        raise

def get_tickets_by_emotion_service(start_date: Optional[date], end_date: Optional[date], emotion: str, db: Session) -> List[TicketSchema]:
    try:
        query = db.query(ProcessedTickets).filter(ProcessedTickets.sentiment_rating == emotion)
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in tickets]
    except Exception as e:
        print(f"Error in get_tickets_by_emotion_service: {e}")
        raise

def get_tickets_by_category_service(start_date: Optional[date], end_date: Optional[date], category: str, db: Session) -> List[TicketSchema]:
    try:
        query = db.query(ProcessedTickets).filter(ProcessedTickets.service_rating == category)
        if start_date:
            filter_start = datetime.combine(start_date, datetime.min.time())
            query = query.filter(ProcessedTickets.start_date >= filter_start)
        if end_date:
            filter_end = datetime.combine(end_date, datetime.max.time())
            query = query.filter(ProcessedTickets.start_date <= filter_end)
        tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in tickets]
    except Exception as e:
        print(f"Error in get_tickets_by_category_service: {e}")
        raise

def get_tickets_by_month_service(month_year: str, db: Session) -> List[TicketSchema]:
    try:
        month, year = map(int, month_year.split("/"))
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])

        filter_start = datetime.combine(first_day, datetime.min.time())
        filter_end = datetime.combine(last_day, datetime.max.time())

        query = db.query(ProcessedTickets).filter(
            ProcessedTickets.start_date >= filter_start,
            ProcessedTickets.start_date <= filter_end
        )
        tickets = query.all()
        return [TicketSchema.model_validate(ticket) for ticket in tickets]
    except Exception as e:
        print(f"Error in get_tickets_by_month_service: {e}")
        raise

def get_ticket_by_id_service(ticket_id: int, db: Session) -> TicketSchema:
    try:
        ticket = db.query(ProcessedTickets).filter(ProcessedTickets.id == ticket_id).first()
        if not ticket:
            raise Exception("Ticket not found")
        return TicketSchema.model_validate(ticket)
    except Exception as e:
        print(f"Error in get_ticket_by_id_service: {e}")
        raise