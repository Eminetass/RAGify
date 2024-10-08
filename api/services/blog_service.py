from pymilvus import Collection
from sqlalchemy.orm import Session
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
from transformers import AutoTokenizer, AutoModel
import torch
from api.models import models
import numpy as np
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def create_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
   
    with torch.no_grad():
        outputs = model(**inputs)
        
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    
    normalized_embedding = embedding / np.linalg.norm(embedding)

    return normalized_embedding

def add_blogs_from_mssql(db: Session):
    
    blogs = db.query(models.Blog).all()  

  
    milvus_collection = Collection("news_blogs_collection")

    for blog in blogs:
        
        embedding = create_embedding(blog.context)

        
        print(f"ID: {blog.id}, Title: {blog.blog_name} (type: {type(blog.blog_name)}), Context: {blog.context} (type: {type(blog.context)}), Embedding shape: {embedding.shape}")

       
        try:
            
            ids = [blog.id]
            titles = [str(blog.blog_name)]
            contexts = [str(blog.context)]
            embeddings = [embedding.tolist()] 
            
            milvus_collection.insert([ids, titles, contexts, embeddings])
            print(f"Blog '{blog.blog_name}' başarıyla Milvus'a eklendi.")
        except Exception as e:
            print(f"Milvus'a ekleme hatası: {str(e)}")
