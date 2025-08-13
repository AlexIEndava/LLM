# backend/services/retriever.py


from chromadb import PersistentClient
from backend.utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY
from backend.services.llm_client import get_llm_response, get_embedding
import json


chroma_client = PersistentClient(path=PERSIST_DIRECTORY)
collection = chroma_client.get_or_create_collection(name="book_summaries")

SYSTEM_PROMPT = (
        "You are a helpful assistant that recommends books based only on the provided book_summaries.\n"
        "Each object includes the title of the book, author, genre, and a brief summary.\n\n"

        "📚 Recommendation Rules:\n"
        "- Only recommend books that appear in the provided book_summaries.\n"
        "- Do not invent or mention any book that is not included.\n"
        "- If no suitable match is found, respond politely that no recommendation can be made.\n"
        "- If multiple books match, list them all.\n"
        "- If multiple books match the user's interests, you must list all of them.\n"
        "- Format your response as a bullet list.\n"
        "- Each bullet must begin with the book title in **double asterisks**, followed by a short reason for the match.\n"
        "- Do not omit any relevant title from the book_summaries.\n\n"
 
        "🛠️ Tool Usage:\n"
        "- You must wrap the book title in double asterisks in your response (e.g., **The Great Gatsby**).\n"
        "- Use the exact title provided in the book_summaries.\n"

        "⚠️ Content Safety:\n"
        "- If the user message includes offensive or inappropriate language, do not generate a recommendation.\n"
        "- If the user asks for content that violates OpenAI's content policy, such as hate speech, violence, or adult content, do not generate a recommendation.\n"
        "- Politely respond with a warning and stop the conversation.\n"
)

with open('backend/data/book_summaries.json', encoding='utf-8') as f:
    books = json.load(f)
unique_genres = set()
for book in books:
    genre = book.get("genre", "").strip()
    if genre:
        unique_genres.add(genre)
genre_list = sorted(unique_genres)

GENRE_PROMPT = (
    "From the following list of genres, choose the one that best matches the user's request. "
    "If none match, respond with 'any'.\n"
    f"Genres: {', '.join(genre_list)}\n"
    "Respond with only one genre from the list or 'any'."
)

def retrieve_recommendations(query: str, n_results: int = 5) -> list[dict]:
    # 1. Reformulează/clarifică query-ul cu LLM chat completions
    print(f"Initial query: {query}")
    clarified_query, _ = get_llm_response(query, system_prompt=SYSTEM_PROMPT)
    print(f"Clarified query: {clarified_query}")

    # Extrage genul cu LLM
    user_genre, _ = get_llm_response(clarified_query, system_prompt=GENRE_PROMPT)
    user_genre = user_genre.strip()
    print(f"User genre: {user_genre}")

    # Generează embedding pentru query
    query_embedding = get_embedding(clarified_query)
    

    # Caută cele mai apropiate cărți în ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    recommendations = []
    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        genre = metadata.get("genre", "").lower()
        # Filtrare fuzzy/substring
        if user_genre != "any" and user_genre not in genre:
            continue
        recommendations.append({
            "title": metadata["title"],
            "genre": metadata["genre"],
            "score": max(0, 1 - distance / 2)
        })
        if len(recommendations) >= n_results:
            break
    return recommendations

