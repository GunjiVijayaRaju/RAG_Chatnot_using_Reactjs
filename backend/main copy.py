from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import shutil
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq

# FastAPI App
app = FastAPI()

# Directory for file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

# Enable CORS (allows frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def delete_all_files():
    """Function to delete all uploaded files."""
    deleted_files = []
    for file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(file)
    return deleted_files

# Clear files on backend startup
deleted_on_startup = delete_all_files()
print(f"Deleted on startup: {deleted_on_startup}")

# Groq API Key and Model
groq_api_key = "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"
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Initialize memory for conversation history
memory = ConversationBufferMemory(memory_key="history")
chain = ConversationChain(llm=llm, memory=memory, verbose=True)

# Request model
class ChatRequest(BaseModel):
    message: str

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        print("User Question:", request.message)
        response = chain.predict(input=request.message)
        print("Response:", response)
        return {"response": response, "history": memory.chat_memory.messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# File Upload Endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": f"File '{file.filename}' uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def get_uploaded_files():
    files = os.listdir(UPLOAD_DIR)
    print("files=========>",files)
    return {"files": files}

@app.post("/delete-all-files")
async def api_delete_all_files():
    deleted_files = delete_all_files()
    return {"message": "Deleted files", "files": deleted_files}

@app.delete("/delete-file/{filename}")
async def delete_file(filename: str):
    file_path = Path(UPLOAD_DIR) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        return {"message": f"File '{filename}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")    