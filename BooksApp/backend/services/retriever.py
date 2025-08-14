# backend/services/retriever.py

from chromadb import PersistentClient
from backend.utils.config import OPENAI_API_KEY, PERSIST_DIRECTORY
from backend.services.llm_client import get_llm_response, get_embedding
import json

chroma_client = PersistentClient(path=PERSIST_DIRECTORY)
collection = chroma_client.get_or_create_collection(name="book_summaries")

with open('backend/data/book_summaries.json', encoding='utf-8') as f:
    books = json.load(f)
unique_genres = set()
unique_titles = set()
for book in books:
    genre = book.get("genre", "").strip()
    title = book.get("title", "").strip()
    # Desparte genurile compuse
    if genre:
        for sub_genre in genre.split('/'):
            unique_genres.add(sub_genre.strip())
    if title:
        unique_titles.add(title)
genre_list = sorted(unique_genres)
title_list = sorted(unique_titles)

print("Genres:", genre_list)
print("Titles:", title_list)

GENRE_PROMPT = (
    "From the following list of genres, choose the one that best matches the user's request. "
    "If the user's message contains offensive, vulgar, or inappropriate language, respond only with 'vulgar'. "
    "If none match, respond with 'any'.\n"
    f"Genres: {', '.join(genre_list)}\n"
    "Respond with only one genre from the list, 'vulgar', or 'any'."
)

SYSTEM_PROMPT = (
    "You are a helpful assistant that recommends books based only on the provided books: {titles}.\n"
    "Each object includes the title of the book, author, genre, and a brief summary.\n\n"

    "📚 Recommendation Rules:\n"
    "- Only recommend books that appear in the provided books.\n"
    "- Do not invent or mention any book that is not included.\n"
    "- If no suitable match is found, respond politely that no recommendation can be made.\n"
    "- If multiple books match, list them all.\n"
    "- If multiple books match the user's interests, you must list all of them.\n"
    "- Format your response as a bullet list.\n"
    "- Each bullet must begin with the book title in **double asterisks**, followed by a short reason for the match.\n"
    "- Do not omit any relevant title from the books.\n\n"
 
    "🛠️ Tool Usage:\n"
    "- You must wrap the book title in double asterisks in your response (e.g., **The Great Gatsby**).\n"
    "- Use the exact title provided in the books.\n"

    "⚠️ Content Safety:\n"
    "- If the user message includes offensive or inappropriate language, do not generate a recommendation.\n"
    "- If the user asks for content that violates OpenAI's content policy, such as hate speech, violence, or adult content, do not generate a recommendation.\n"
    "- Politely respond with a warning and stop the conversation.\n\n"

    "**Respond ONLY in English.**"
).format(titles=', '.join(title_list))

CLARIFY_PROMPT = (
    "Reformulate the user's request as a clear, concise search query for a book. "
    "Do not answer the question, just rewrite it as a search query in English."
)

def retrieve_recommendations(query: str, n_results: int = 5):
    # 1. Reformulează/clarifică query-ul cu LLM chat completions
    print(f"Initial query: {query}")

    
    clarified_query, _ = get_llm_response(query, system_prompt=SYSTEM_PROMPT)
    print(f"Clarified query: {clarified_query}")

    # Extrage genul cu LLM
    user_genre, _ = get_llm_response(clarified_query, system_prompt=GENRE_PROMPT)
    user_genre = user_genre.strip().lower()
    print(f"User genre: {user_genre}")

    if user_genre == "vulgar":
        return {"vulgar_message": clarified_query}
    
    if user_genre == "any":
        return {"vulgar_message": clarified_query}

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
        print(f"Checking book: {metadata['title']} with genre: {genre} and distance: {distance}")
        if user_genre != "any":
            sub_genres = [g.strip() for g in genre.split('/')]
            print(f"Sub-genres: {sub_genres} - User genre in sub-genres: {user_genre in sub_genres}")
            if user_genre not in sub_genres:
                continue
        recommendations.append({
            "title": metadata["title"],
            "genre": metadata["genre"],
            "score": max(0, 1 - distance / 2)
        })
        if len(recommendations) >= n_results:
            break

    return recommendations
