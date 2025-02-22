from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from typing import List, Optional
import uuid
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="vectordb",
        user="postgres",
        password="yourpassword",
        host="0.0.0.0",
        port=5432
    )

class Problem(BaseModel):
    problemId: str
    title: str
    description: str
    solution: str

@app.post("/embeddings")
async def generate_embeddings(problem: Problem):
    # Generate embeddings for the problem
    text = f"{problem.title} {problem.description} {problem.solution}"
    embedding = model.encode(text)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Store the embedding
        cur.execute(
            "INSERT INTO embeddings (problem_id, embedding) VALUES (%s, %s)",
            (problem.problemId, embedding.tolist())
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def semantic_search(query: str, limit: int = 5):
    print("hi friend")
    # Generate embedding for the query
    query_embedding = model.encode(query)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Perform semantic search using cosine similarity
        cur.execute("""
            SELECT p.id, p.title, p.description, p.solution, 
                   1 - (e.embedding <-> %s::vector) as similarity
            FROM problems p
            JOIN embeddings e ON p.id = e.problem_id
            WHERE 1 - (e.embedding <-> %s::vector) > 0.7
            ORDER BY similarity DESC
            LIMIT %s
        """, (query_embedding.tolist(), query_embedding.tolist(), limit))
        
        results = cur.fetchall()
        
        problems = [
            {
                "id": str(row[0]),
                "title": row[1],
                "description": row[2],
                "solution": row[3],
                "similarity": float(row[4])
            }
            for row in results
        ]
        
        cur.close()
        conn.close()
        print(problems)
        return problems
    except Exception as e:
        logger.error(f"Error during semantic search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)