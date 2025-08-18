# backend/services/embedding_service.py

#python -m backend.services.embedding_service

import json
import os
from chromadb import PersistentClient
from backend.utils.config import PERSIST_DIRECTORY
from backend.services.llm_client import get_embedding

# Initialize ChromaDB client
chroma_client = PersistentClient(path=PERSIST_DIRECTORY)
collection = chroma_client.get_or_create_collection(name="book_summaries")

# Load book summaries from JSON file
DATA_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')
)

def generate_embeddings():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        books = json.load(file)

    for book in books:
        # Folosește cheile în engleză
        title = book.get('title')
        author = book.get('author')
        genre = book.get('genre')
        description = book.get('description')
        image = book.get('image', '')

        # Obține embedding pentru descriere folosind funcția din llm_client.py
        embedding = get_embedding(description)

        # Store embedding in ChromaDB cu toate metadatele
        collection.add(
            embeddings=[embedding],
            metadatas=[{
                "title": title,
                "author": author,
                "genre": genre,
                "description": description,
                "image": image
            }],
            ids=[title.replace(" ", "_")]
        )

    print("Embeddings generated and stored successfully.")

def update_book_embedding(book):
    title = book.get('title')
    author = book.get('author')
    genre = book.get('genre')
    description = book.get('description')
    image = book.get('image', '')

    embedding = get_embedding(description)
    # Șterge vechiul embedding dacă există
    collection.delete(ids=[title.replace(" ", "_")])
    # Adaugă embedding nou cu imaginea actualizată
    collection.add(
        embeddings=[embedding],
        metadatas=[{
            "title": title,
            "author": author,
            "genre": genre,
            "description": description,
            "image": image
        }],
        ids=[title.replace(" ", "_")]
    )

if __name__ == "__main__":
    generate_embeddings()
