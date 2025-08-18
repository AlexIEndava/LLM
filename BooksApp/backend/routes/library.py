from flask import Blueprint, jsonify
import json
import os

bp = Blueprint('library', __name__)

@bp.route('/all-books/', methods=['GET'])
def all_books():
    books_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')
    with open(books_file, encoding='utf-8') as f:
        books = json.load(f)
    return jsonify(books)