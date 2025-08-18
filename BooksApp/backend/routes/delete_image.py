from flask import Blueprint, request, jsonify
import os
import json
from backend.services.embedding_service import update_book_embedding

bp = Blueprint('delete_image', __name__)

BOOKS_FILE = 'backend/data/book_summaries.json'
IMAGES_DIR = 'backend/data/book_images'

@bp.route('/delete-image/', methods=['POST'])
def delete_image():
    data = request.json
    title = data.get('title')
    if not title:
        return jsonify({'success': False, 'error': 'Missing title'}), 400

    # Actualizează JSON și șterge fișierul imagine
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        books = json.load(f)
    found = False
    for book in books:
        if book.get('title') == title and book.get('image'):
            image_path = os.path.join(IMAGES_DIR, book['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
            book['image'] = ""
            update_book_embedding(book)  # actualizează embeddingul fără imagine
            found = True
            break
    if found:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Book or image not found'}), 404