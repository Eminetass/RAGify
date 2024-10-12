from fastapi import APIRouter, HTTPException , Depends
from sqlalchemy.orm import Session
from api.services.blog_service import create_embedding
from models.models import get_db

router = APIRouter()

@router.post("/create_embedding/")
def create_embedding_route(text: str, db: Session = Depends(get_db)):
    try:
        embedding = create_embedding(text)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))