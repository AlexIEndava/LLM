# backend/app.py

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routes.recommend import router as recommend_router
from backend.routes.summary import router as summary_router

app = FastAPI(
    title="Smart Librarian API",
    description="Recomandări de cărți și rezumate cu OpenAI + ChromaDB",
    version="0.1.0"
)

# Servește tot conținutul din fronted/ ca fișiere statice la /static
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../fronted")),
    name="static"
)

# Servește index.html la rădăcina aplicației
@app.get("/", include_in_schema=False)
async def serve_ui():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "../fronted/index.html")
    )

# Înregistrează rutele API
app.include_router(recommend_router, prefix="/recommend", tags=["recommend"])
app.include_router(summary_router, prefix="/summary",   tags=["summary"])

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
