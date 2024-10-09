from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pymilvus import Collection
from api.services.vectordb_service import initialize_milvus, search_in_milvus, create_blogs_collection, create_embedding
from api.models import models
from api.services.blog_service import add_blogs_from_mssql
from fastapi import APIRouter
from api.services.open_ai_services import chatbot_query

app = FastAPI()

router = APIRouter()
templates = Jinja2Templates(directory="C:/Users/erene/OneDrive/Masaüstü/softtech_staj/RAGify/api/templates")


models.create_tables()


initialize_milvus()
app.include_router(router)


create_blogs_collection()
db = next(models.get_db())
add_blogs_from_mssql(db)

@router.get("/")
def read_root(request: Request, db: Session = Depends(models.get_db)):
    print("Ana sayfa isteği alındı")  
    all_blogs = db.query(models.Blog).all()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": all_blogs})

@router.post("/blogs/add")
def add_blog(blog_name: str = Form(...), context: str = Form(...), author: str = Form(...), db: Session = Depends(models.get_db)):
    new_blog = models.Blog(blog_name=blog_name, context=context, author=author)
    db.add(new_blog)
    db.commit()
    
    
    embedding = create_embedding(context)
    
    try:
        milvus_collection = Collection("news_blogs_collections")
        
        insert_data = [
            [new_blog.id],
            [blog_name],
            [context],
            [embedding.tolist()]
        ]
        milvus_collection.insert(insert_data)
        print(f"Blog '{blog_name}' başarıyla Milvus'a eklendi.")
    except Exception as e:
        print(f"Milvus'a ekleme hatası: {str(e)}")

    return {"message": "Blog başarıyla eklendi."}

@router.post("/blogs/delete")
def delete_blog(blog_id: int, db: Session = Depends(models.get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return {"message": "Blog başarıyla silindi."}
    else:
        return {"message": "Blog bulunamadı."}

@router.post("/search")
def search(query: str = Form(...), db: Session = Depends(models.get_db)):
    try:
        processed_results = search_in_milvus(query, db)
        return {"results": processed_results}
    except Exception as e:
        return {"error": str(e)}

@router.post("/chatbot/")
async def ask_chatbot(question: str = Form(...), db: Session = Depends(models.get_db)):
    
    response = chatbot_query(question, db)
    return {"response": response}


