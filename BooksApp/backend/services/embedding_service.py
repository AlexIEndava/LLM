# backend/services/embedding_service.py

import openai
import json
from chromadb import PersistentClient
from backend.utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY
import os

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize ChromaDB client
chroma_client = PersistentClient(path=PERSIST_DIRECTORY)

# Get or create collection for storing book embeddings
collection = chroma_client.get_or_create_collection(name="book_summaries")

# Load book summaries from JSON file
DATA_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'book_summaries.json')
)

def generate_embeddings():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        books = json.load(file)

    for book in books:
        description = book.get('descriere') or book.get('description')
        title = book.get('titlu') or book.get('title')
        
        # Generate embedding using OpenAI
        response = openai.Embedding.create(
            input=[description],
            model="text-embedding-3-small"
        )
        embedding = response["data"][0]["embedding"]

        # Store embedding in ChromaDB
        collection.add(
            embeddings=[embedding],
            metadatas=[{"title": title}],
            ids=[title.replace(" ", "_")]  # id simplu bazat pe titlu
        )

    print("Embeddings generated and stored successfully.")

if __name__ == "__main__":
    generate_embeddings()
