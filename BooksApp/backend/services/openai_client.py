# backend/services/openai_client.py

import json
import os

# cale relativă către book_summaries.json
DATA_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')
)

def get_summary_by_title(title: str) -> str:
    """
    Caută în book_summaries.json cartea cu titlul exact și returnează descrierea.
    Dacă nu există, returnează un string gol.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except FileNotFoundError:
        # eventual log aici
        return ""

    for book in books:
        # verificăm atât cheie română, cât și engleză
        if book.get('titlu') == title or book.get('title') == title:
            return book.get('descriere') or book.get('description') or ""
    return ""
