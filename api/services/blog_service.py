from pymilvus import Collection, connections
from sqlalchemy.orm import Session
from pymilvus import CollectionSchema, FieldSchema, DataType, utility
import numpy as np
import os
import openai
from dotenv import load_dotenv
from api.models import models

# Çevresel değişkenleri yükle
load_dotenv()

# OpenAI API anahtarı yükle
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Milvus bağlantısını başlat
connections.connect(alias="default", host="localhost", port="19530")

# Embedding oluşturma fonksiyonu
def create_embedding(text):
    # Gelen verinin tipi ve içeriği kontrol ediliyor
    print(f"Gelen text tipi: {type(text)}")
    print(f"Gelen text içeriği: {text}")
    
    # Eğer gelen veri bir liste ise stringe dönüştürülüyor
    if isinstance(text, list):
        text = " ".join(text)
    
    # Eğer hala string değilse hata fırlatılıyor
    if not isinstance(text, str):
        raise ValueError("Gelen veri string olmalı!")
    
    try:
        # OpenAI API kullanarak embedding oluşturma
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        embedding = np.array(embedding)

        # Vektör normalizasyonu
        normalized_embedding = embedding / np.linalg.norm(embedding)

        return normalized_embedding

    except Exception as e:
        print(f"Error while creating embedding: {e}")
        return None

# MSSQL'den blogları çekip Milvus'a ekleyen fonksiyon
def add_blogs_from_mssql(db: Session):
    # MSSQL'den blog verilerini al
    blogs = db.query(models.Blog).all()

    # Milvus koleksiyonunun var olup olmadığını kontrol et
    if not utility.has_collection("news_blogs_collections"):
        print("Milvus koleksiyonu bulunamadı. Lütfen koleksiyonu oluşturun.")
        return

    milvus_collection = Collection("news_blogs_collections")

    for blog in blogs:
        # Embedding oluştur
        embedding = create_embedding(blog.context)

        # Eğer embedding None dönerse işlemi atla
        if embedding is None:
            print(f"Embedding oluşturulamadı! Blog ID: {blog.id}, Blog Name: {blog.blog_name}")
            continue
        
        print(f"ID: {blog.id}, Title: {blog.blog_name} (type: {type(blog.blog_name)}), Context: {blog.context} (type: {type(blog.context)}), Embedding shape: {embedding.shape}")

        try:
            # Veriyi Milvus'a ekle
            ids = [blog.id]
            titles = [str(blog.blog_name)]
            contexts = [str(blog.context)]
            embeddings = [embedding.tolist()] 
            
            # Milvus koleksiyonuna veri ekle
            milvus_collection.insert([ids, titles, contexts, embeddings])
            print(f"Blog '{blog.blog_name}' başarıyla Milvus'a eklendi.")
        except Exception as e:
            print(f"Milvus'a ekleme hatası: {str(e)}")
