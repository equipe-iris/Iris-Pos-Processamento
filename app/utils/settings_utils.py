from sqlalchemy.orm import Session
from app.models.settings import Settings

def ensure_settings_exists(db: Session):
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings(ast_goal=0.0)
        db.add(settings)
        db.commit()
        print("Settings created with default values.")