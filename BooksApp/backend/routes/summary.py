# backend/routes/summary.py
from flask import Blueprint, request, jsonify
from backend.services.openai_client import get_summary_by_title

summary_router = Blueprint("summary", __name__)

@summary_router.route("/", methods=["GET"])
def summary():
    title = request.args.get("title", "")
    summary_text = get_summary_by_title(title)
    if not summary_text:
        return jsonify({"error": "Titlu negăsit"}), 404
    return jsonify({"title": title, "summary": summary_text})
