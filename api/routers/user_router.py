from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.services.log_service import create_log, get_logs
from models.models import get_db

router = APIRouter()

@router.post("/create_log/")
def create_log_route(user_question: str, assistant_answer: str, db: Session = Depends(get_db)):
    try:
        log = create_log(db, user_question, assistant_answer)
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/logs/")
def get_logs_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs    
