from pymilvus import Collection
from sqlalchemy.orm import Session
from api.models import models

from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


collection_name = "news_blogs_collection"

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def initialize_milvus():
    
    connection_alias = "default"
    if connection_alias in connections.list_connections():
        try:
            connections.disconnect(connection_alias)
            print(f"'{connection_alias}' bağlantısı kapatıldı.")
        except Exception as e:
            print(f"Bağlantı kapatma hatası: {str(e)}")

    try:
        connections.connect(connection_alias, host='localhost', port='19530')
        print("Milvus'a bağlanıldı.")
    except Exception as e:
        print(f"Bağlantı hatası: {str(e)}")
        return

from sklearn.preprocessing import normalize

def create_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        # Normalizasyon ekle
        embedding = normalize(embedding.reshape(1, -1))  
        return embedding.flatten()  

    
    
    normalized_embedding = embedding / np.linalg.norm(embedding)
    return normalized_embedding

def check_collection(news_blogs: str) -> bool:
    
    try:
        collection_exists = utility.has_collection(collection_name)
        return collection_exists
    except Exception as e:
        print(f"Koleksiyon kontrol hatası: {str(e)}")
        return False
    


def normalize_vector(vector):
    norm = np.linalg.norm(vector)  
    if norm == 0: 
       return vector  
    return vector / norm 


def create_blogs_collection():
  
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False)  
    title_field = FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500)  
    context_field = FieldSchema(name="context", dtype=DataType.VARCHAR, max_length=2000)  
    embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)  

    schema = CollectionSchema(fields=[id_field, title_field, context_field, embedding_field], description="Blog collection")

    collection_name = "news_blogs_collection"
    if not utility.has_collection(collection_name):
        blogs_collection = Collection(name=collection_name, schema=schema)
        print("Koleksiyon başarıyla oluşturuldu.")
    else:
        print(f"Koleksiyon '{collection_name}' zaten mevcut.")

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }

    try:
        blogs_collection.create_index("embedding", index_params)
        print("İndeks başarıyla oluşturuldu.")
    except Exception as e:
        print(f"İndeks oluşturma hatası: {str(e)}")
        return

    try:
        blogs_collection.load()
        print("Koleksiyon başarıyla belleğe yüklendi.")
    except Exception as e:
        print(f"Koleksiyonu yükleme hatası: {str(e)}")




def search_in_milvus(query: str, db: Session, top_k: int = 5):
    
    query_embedding = create_embedding(query)

   
    milvus_collection = Collection("news_blogs_collection")
    milvus_collection.load()  

    
    search_params = {
        "metric_type": "L2",  
        "params": {"nprobe": 200},  
    }

    try:

        results = milvus_collection.search(
            data=[query_embedding.tolist()],  
            anns_field="embedding",  
            param=search_params,
            limit=top_k  
        )

        print("query")
        print(query_embedding)
        print("query embedding to list")
        print(query_embedding.tolist())
    except Exception as e:
        return {"error": f"Arama sırasında hata oluştu: {str(e)}"}

   
    processed_results = []
    
    for hits in results:  
        for hit in hits:  
            blog_id = hit.id  
            distance = hit.distance 

           
            blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

            if blog:
                processed_results.append({
                    "id": blog_id,
                    "distance": distance,
                    "blog_name": blog.blog_name,
                    "context": blog.context,
                    "author": blog.author
                })

    return {"results": processed_results}


