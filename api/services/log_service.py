from models import Log
from sqlalchemy.orm import Session

def create_log(db: Session, user_question: str, assistant_answer: str):
    
   
    new_log = Log(
        user_question=user_question,
        assistant_answer=assistant_answer
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_logs(db: Session, skip: int = 0, limit: int = 10):

    return db.query(Log).offset(skip).limit(limit).all()
