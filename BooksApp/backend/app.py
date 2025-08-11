# backend/app.py

import uvicorn
from fastapi import FastAPI
from utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY
#from routes.recommend import router as recommend_router
#from routes.summary import router as summary_router

app = FastAPI(
    title="Smart Librarian API",
    description="Recomandări de cărți și rezumate cu OpenAI + ChromaDB",
    version="0.1.0"
)

# Înregistrează rutele
#app.include_router(recommend_router, prefix="/recommend", tags=["recommend"])
#app.include_router(summary_router, prefix="/summary", tags=["summary"])

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Smart Librarian API este funcțională"}

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
