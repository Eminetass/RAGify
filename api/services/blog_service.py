from pymilvus import Collection, connections
from sqlalchemy.orm import Session
from pymilvus import CollectionSchema, FieldSchema, DataType, utility
import numpy as np
import os
import openai
from dotenv import load_dotenv
from api.models import models


load_dotenv()


openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")


connections.connect(alias="default", host="localhost", port="19530")


def create_embedding(text):
    
    print(f"Gelen text tipi: {type(text)}")
    print(f"Gelen text içeriği: {text}")
    
   
    if isinstance(text, list):
        text = " ".join(text)
    
    
    if not isinstance(text, str):
        raise ValueError("Gelen veri string olmalı!")
    
    try:
       
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        embedding = np.array(embedding)

        
        normalized_embedding = embedding / np.linalg.norm(embedding)

        return normalized_embedding

    except Exception as e:
        print(f"Error while creating embedding: {e}")
        return None


def add_blogs_from_mssql(db: Session):
    
    blogs = db.query(models.Blog).all()

    
    if not utility.has_collection("news_blogs_collections"):
        print("Milvus koleksiyonu bulunamadı. Lütfen koleksiyonu oluşturun.")
        return

    milvus_collection = Collection("news_blogs_collections")

    for blog in blogs:
        
        embedding = create_embedding(blog.context)

        
        if embedding is None:
            print(f"Embedding oluşturulamadı! Blog ID: {blog.id}, Blog Name: {blog.blog_name}")
            continue
        
        print(f"ID: {blog.id}, Title: {blog.blog_name} (type: {type(blog.blog_name)}), Context: {blog.context} (type: {type(blog.context)}), Embedding shape: {embedding.shape}")

        try:
            
            ids = [blog.id]
            titles = [str(blog.blog_name)]
            contexts = [str(blog.context)]
            embeddings = [embedding.tolist()] 
            
            # Milvus koleksiyonuna veri ekle
            milvus_collection.insert([ids, titles, contexts, embeddings])
            print(f"Blog '{blog.blog_name}' başarıyla Milvus'a eklendi.")
        except Exception as e:
            print(f"Milvus'a ekleme hatası: {str(e)}")
