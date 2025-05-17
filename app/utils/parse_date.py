from typing import Optional
from datetime import datetime, date
from fastapi import HTTPException

def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}")