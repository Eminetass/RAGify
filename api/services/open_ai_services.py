import os
import openai
from dotenv import load_dotenv
from api.services.vectordb_service import search_in_milvus, create_embedding
from sqlalchemy.orm import Session
import numpy as np
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Bir hata oluştu, lütfen tekrar deneyin."
    




    


def chatbot_query(question, db):
    print(f"Gelen question tipi: {type(question)}")

    if isinstance(question, list):
        question = " ".join(question)

    if not isinstance(question, str):
        raise ValueError("Question string olmalı!")

    
    question_embedding = create_embedding(question)

    if isinstance(question_embedding, np.ndarray):
        question_embedding = question_embedding.tolist()

    
    top_results = search_in_milvus(question_embedding, db, top_k=5)

   
    if not top_results.get("results"):
        return "Sonuç bulunamadı."

    
    contexts = "\n".join([result["context"] for result in top_results["results"]])

    
    full_prompt = f"Bu blog içeriklerine dayanarak sorunuz: {question}\n\nİçerikler:\n{contexts}\n\nCevap:"
    response = get_openai_response(full_prompt)

    return response




