import os
import openai
from dotenv import load_dotenv
from api.services.vectordb_service import search_in_milvus, create_embedding
from sqlalchemy import Session

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=question,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Bir hata oluştu, lütfen tekrar deneyin."
    




    

def chatbot_query(question: str, db: Session):
    # Sorguya ait gömülü vektörü oluştur
    question_embedding = create_embedding(question)

    # En yakın sonuçları bulmak için Milvus'a sorgu gönder
    top_results = search_in_milvus(question_embedding, db, top_k=5)

    return top_results


