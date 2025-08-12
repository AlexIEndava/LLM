# backend/routes/recommend.py
from flask import Blueprint, request, jsonify
from backend.services.retriever import retrieve_recommendations

recommend_router = Blueprint("recommend", __name__)

@recommend_router.route("/", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    results = retrieve_recommendations(query)
    return jsonify(results)
