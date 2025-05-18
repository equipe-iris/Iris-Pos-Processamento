from sqlalchemy.orm import Session
from app.models.settings import Settings
from app.utils.settings_utils import ensure_settings_exists

def get_ast_goal_service(db: Session) -> float:
    try:
        settings = db.query(Settings).first()
        if settings:
            return settings.ast_goal
        else:
            raise ValueError("Settings not found.")
    except Exception as e:
        raise Exception(f"Error retrieving AST goal: {e}")

def update_ast_goal_service(ast_goal: float, db: Session):
    try:
        if ast_goal < 0:
            raise ValueError("AST goal must be a non-negative number.")
        
        ensure_settings_exists(db)
        settings = db.query(Settings).first()
        if settings:
            settings.ast_goal = ast_goal
            db.commit()
            db.refresh(settings)
            return settings.ast_goal
        else:
            raise ValueError("Settings not found.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating AST goal: {e}") 