import json
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')

def get_summary_by_title(title: str) -> str:
    if not title:
        raise ValueError("Title must not be empty.")

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Book summaries file not found.")
    except json.JSONDecodeError:
        raise ValueError("Book summaries file is not a valid JSON.")

    for book in books:
        if book.get('title') == title:
            description = book.get('description')
            if description:
                return description
            else:
                raise ValueError(f"No description found for book with title '{title}'.")
    raise ValueError(f"No book found with title '{title}'.")
