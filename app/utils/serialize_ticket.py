from datetime import datetime

def serialize_ticket(ticket):
    data = ticket.model_dump()
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data