# Offline ChatGPT Clone

A fully local AI assistant built using:

- FastAPI
- Streamlit
- Ollama
- Qwen2.5
- SQLite
- LangChain
- RAG (PDF Upload)

## Features

- Fully offline AI chat
- Streaming responses
- Persistent chat history
- Multiple conversations
- PDF upload + RAG
- Local vector retrieval
- SQLite memory

## Tech Stack

- Python
- FastAPI
- Streamlit
- Ollama
- SQLAlchemy
- LangChain
- SQLite

## Run Locally

### Install dependencies

pip install -r requirements.txt

### Start Backend

uvicorn backend.app:app --reload

### Start Frontend

streamlit run frontend/streamlit_app.py

## Model Used

qwen2.5:3b via Ollama

## Future Improvements

- Source citations
- Voice assistant
- Dark modern UI
- Multi-PDF support
- Docker deployment
- Authentication