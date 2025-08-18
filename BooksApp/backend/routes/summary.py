# backend/routes/summary.py
from flask import Blueprint, request, jsonify
from backend.services.openai_client import get_summary_by_title

bp = Blueprint('summary', __name__)

@bp.route('/summary/', methods=['POST'])
def summary():
    data = request.json
    title = data.get('title')
    summary = get_summary_by_title(title)
    return jsonify({'summary': summary})
