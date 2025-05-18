from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.settings_service import (
    get_ast_goal_service,
    update_ast_goal_service
)
from app.schemas.settings_schema import AstGoalRequest

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/ast-goal")
def get_ast_goal(db: Session = Depends(get_db)):
    try:
        ast_goal = get_ast_goal_service(db)
        return ast_goal
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving AST goal")

@router.put("/update-ast-goal")
def update_ast_goal(req: AstGoalRequest, db: Session = Depends(get_db)):
    try:
        ast_goal = req.ast_goal
        updated_ast_goal = update_ast_goal_service(ast_goal, db)
        return {"message": "AST goal updated successfully", "Current AST GOAL": updated_ast_goal}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating AST goal")