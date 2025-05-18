# 🧠 GenAI Chatbot (RAG + Conversational AI)

This is a **RAG-based chatbot** that supports both:

- Conversational question-answering (normal chat)
- Retrieval-Augmented Generation (RAG): responds based on ingested documents

It includes a **React frontend** powered by Vite and a **FastAPI backend**.

---

## 🚀 Features

- Conversational responses using LLM
- Contextual answers using document ingestion (RAG)
- Seamless frontend-backend integration

---

## 🧩 Technologies Used

- React + Vite
- FastAPI (Python)
- Langchain
- Retrieval-Augmented Generation (RAG)
- OpenAI or compatible LLM

---

## 🛠️ Installation & Usage

### 📦 Frontend Setup

```bash
cd frontend
npm install           # Installs frontend dependencies
npm run dev           # Starts the Vite development server

### 📦 Backend up
cd backend
pip install -r requirements.txt   # Installs backend Python dependencies
uvicorn main:app --reload         # Starts the FastAPI backend server

