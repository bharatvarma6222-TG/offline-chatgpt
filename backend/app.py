from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import requests
import json
import shutil

from backend.rag.ingest import ingest_pdf
from backend.rag.retriever import retrieve_context

from backend.database.db import engine, SessionLocal
from backend.database.models import Message
from backend.database.db import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"


class ChatRequest(BaseModel):
    chat_id: str
    messages: list


# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    db = SessionLocal()

    # Save latest user message
    last_user_message = req.messages[-1]

    db.add(
        Message(
            chat_id=req.chat_id,
            role=last_user_message["role"],
            content=last_user_message["content"]
        )
    )

    db.commit()

    # User query
    user_query = last_user_message["content"]

    # Retrieve RAG context
    try:
        context = retrieve_context(user_query)
    except:
        context = "No PDF context available."

    # Augmented prompt
    augmented_prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{user_query}
"""

    payload = {
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "user",
                "content": augmented_prompt
            }
        ],
        "stream": True
    }

    def generate():

        full_response = ""

        with requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True
        ) as response:

            for line in response.iter_lines():

                if line:

                    decoded_line = line.decode("utf-8")

                    data = json.loads(decoded_line)

                    if "message" in data:

                        content = data["message"]["content"]

                        full_response += content

                        yield content

        # Save assistant response
        db.add(
            Message(
                chat_id=req.chat_id,
                role="assistant",
                content=full_response
            )
        )

        db.commit()

        db.close()

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )


# =========================
# PDF UPLOAD ENDPOINT
# =========================
@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process PDF
    result = ingest_pdf(file_path)

    return {
        "message": result
    }


@app.get("/chat-history/{chat_id}")
def get_chat_history(chat_id: str):

    db = SessionLocal()

    messages = db.query(Message).filter(
        Message.chat_id == chat_id
    ).all()

    result = []

    for msg in messages:

        result.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    db.close()

    return result


@app.get("/chats")
def get_chats():

    db = SessionLocal()

    chats = db.query(Message.chat_id).distinct().all()

    db.close()

    return [chat[0] for chat in chats]
