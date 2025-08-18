from flask import Blueprint, request, jsonify
from backend.services.llm_client import generate_and_save_image
from backend.services.embedding_service import update_book_embedding
import json
import os

bp = Blueprint('generate_image', __name__)

BOOKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'book_images')

@bp.route('/generate-image/', methods=['POST'])
def generate_image():
    data = request.json
    print("Received data for image generation:", data)
    title = data.get('title')
    author = data.get('author')
    if not title or not author:
        return jsonify({'error': 'Missing title or author'}), 400

    prompt = f"A creative book cover for '{title}' by {author}"
    filename = f"{title.lower().replace(' ', '_').replace(':', '').replace(',', '')}.png"
    filepath = os.path.join(IMAGES_DIR, filename)

    try:
        generate_and_save_image(prompt, filepath)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        books = json.load(f)
    for book in books:
        if book.get('title') == title:
            book['image'] = filename
            update_book_embedding(book)  # actualizează embedding-ul pentru cartea modificată
            break
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    return jsonify({'image': filename})