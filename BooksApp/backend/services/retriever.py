# backend/services/retriever.py

import openai
from chromadb import PersistentClient
from backend.utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize a persistent ChromaDB client
chroma_client = PersistentClient(path=PERSIST_DIRECTORY)

# Create or get the collection that holds our book embeddings
collection = chroma_client.get_or_create_collection(name="book_summaries")

def retrieve_recommendations(query: str, n_results: int = 5) -> list[dict]:
    """
    Generate an embedding for the user query, then return top-N recommended books.

    Args:
        query (str): The search query or topic string.
        n_results (int): Number of top results to return.

    Returns:
        list[dict]: A list of dicts with keys 'title' and 'score',
                    where 'score' approximates similarity.
    """
    # Generate embedding for the query text
    response = openai.Embedding.create(
        input=[query],
        model="text-embedding-3-small"
    )
    query_embedding = response["data"][0]["embedding"]

    # Query the vector store
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    recommendations = []
    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        title = metadata.get("title") or metadata.get("titlu")
        # Convert distance to a similarity-like score (1 - distance)
        score = 1 - distance
        recommendations.append({"title": title, "score": score})
    return recommendations
