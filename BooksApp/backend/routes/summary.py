# backend/routes/summary.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.openai_client import get_summary_by_title

class SummaryResponse(BaseModel):
    title: str
    summary: str

router = APIRouter()

@router.get("/", response_model=SummaryResponse)
async def summary(title: str):
    """
    Primește /summary?title=... și returnează {"title":..., "summary": ...}
    """
    summary_text = get_summary_by_title(title)
    if not summary_text:
        raise HTTPException(status_code=404, detail="Titlu negăsit")
    return {"title": title, "summary": summary_text}
