# backend/routes/recommend.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.retriever import retrieve_recommendations

# definește aici modelul de request
class RecommendRequest(BaseModel):
    query: str

# instanțiezi router-ul
router = APIRouter()

@router.post("/", response_model=list[dict])
async def recommend(req: RecommendRequest):
    """
    Primește {"query": "..."} și returnează o listă de recomandări:
    [{ "title": str, "score": float }, ...]
    """
    results = retrieve_recommendations(req.query)
    return results
