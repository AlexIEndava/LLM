# backend/services/retriever.py

from openai import OpenAI
from chromadb import PersistentClient
from backend.utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY

client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = PersistentClient(path=PERSIST_DIRECTORY)
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
    # Generează embedding pentru query
    response = client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    )
    query_embedding = response.data[0].embedding

    # Caută cele mai apropiate cărți în ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    recommendations = []
    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        recommendations.append({
            "title": metadata["title"],
            "score": 1 - distance  # sau altă formulă de scor
        })
    return recommendations
