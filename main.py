
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import openai
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()
# Allow React frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all domains (for development)
    allow_methods=["*"],    # allow all HTTP methods
    allow_headers=["*"],    # allow all headers
)

# Set your OpenAI API key (replace with your key)
openai.api_key = "YOUR_OPENAI_API_KEY"

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(req: QueryRequest):
    user_question = req.question

    # 1️ Generate SQL from question using OpenAI
    prompt = f"""
    You are a SQL expert. Here is the database schema:
    Table sales(id INTEGER, product TEXT, revenue REAL, date TEXT)

    Generate a SQL query to answer this question:
    {user_question}

    Only provide the SQL query without explanation.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0
        )
        sql_query = response.choices[0].text.strip()
    except Exception as e:
        return {"error": f"LLM error: {str(e)}"}

    # Execute SQL safely
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql(sql_query, conn)
        conn.close()
    except Exception as e:
        return {"error": f"SQL error: {str(e)}"}

    # 3️ Optional: generate natural language explanation
    try:
        explanation_prompt = f"Explain this SQL result in simple terms: {df.to_dict(orient='records')}"
        explanation = openai.Completion.create(
            engine="text-davinci-003",
            prompt=explanation_prompt,
            max_tokens=150,
            temperature=0
        )
        answer_text = explanation.choices[0].text.strip()
    except:
        answer_text = "Here is your result."

    return {
        "answer": answer_text,
        "table": df.to_dict(orient="records"),
        "sql_used": sql_query
    }

@app.get("/")
def read_root():
    return {"message": "AI Data Agent is running!"}