from app.schemas.classification_results_schema import ClassificationResults
from app.schemas.tickets_schema import TicketSchema
from sqlalchemy.orm import Session
from app.models.processed_tickets import ProcessedTickets
from app.models.tickets_files import TicketsFiles
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List

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
                    "start_date": ticket.start_date,
                    "end_date": ticket.end_date,
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

def get_processed_tickets_service(db: Session) -> List[TicketSchema]:
    try:
        processed_tickets = db.query(ProcessedTickets).all()
        return [TicketSchema.model_validate(ticket) for ticket in processed_tickets]
    except Exception as e:
        print(f"Error retrieving processed tickets: {e}")
        raise Exception(e)
