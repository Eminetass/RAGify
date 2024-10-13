#FasAPI dan gerekli modülller,Session sınıfını içe aktarma,fonksiyon içe katarmalaır yapılıyor.
from fastapi import APIRouter, HTTPException , Depends
from sqlalchemy.orm import Session
from api.services.blog_service import create_embedding
from models.models import get_db

#yeni bir API router'ı oluşturuluyor.
router = APIRouter()


#POST isteği için bir API rotası tanımlanıyor.Fonksiyon tanımlanıyor. Kullanıcıdan alınan metni embedding'e dönüştürür ve sonucu döndürür.
@router.post("/create_embedding/")
def create_embedding_route(text: str, db: Session = Depends(get_db)):
    try:
        embedding = create_embedding(text)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
