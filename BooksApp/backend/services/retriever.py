# backend/services/retriever.py

from chromadb import PersistentClient
from backend.utils.config import PERSIST_DIRECTORY
from backend.services.llm_client import get_llm_response, get_embedding
import json

chroma_client = PersistentClient(path=PERSIST_DIRECTORY)
collection = chroma_client.get_or_create_collection(name="book_summaries")

with open('backend/data/book_summaries.json', encoding='utf-8') as f:
    books = json.load(f)
unique_genres = set()
for book in books:
    genre = book.get("genre", "").strip()
    title = book.get("title", "").strip()
    # Desparte genurile compuse
    if genre:
        for sub_genre in genre.split('/'):
            unique_genres.add(sub_genre.strip())
genre_list = sorted(unique_genres)

VULGAR_DETECT_PROMPT = (
    "If the user's message contains offensive, vulgar, or inappropriate language in ANY language, "
    "respond ONLY with 'vulgar'."
    "If the message does NOT contain any offensive, vulgar, or inappropriate language, respond ONLY with 'ok'."
)

CLARIFY_PROMPT = (
    "Your role is to reformulate the user's request as a clear, concise search query for a book.\n"
    
    "📚 Recommendation Rules:\n"
    "Do not answer the question, just rewrite it as a search query in English. "

    "**Respond ONLY in English.**"
)

GENRE_PROMPT = (
    "From the following list of genres, choose the one that best matches the user's request. "
    "If none match, respond with 'any'.\n"
    f"Genres: {', '.join(genre_list)}\n"
    "Respond with only one genre from the list or 'any'."
)


def retrieve_recommendations(query: str, n_results: int = 10):
    
    #print(f"Initial query: {query}")

    # 1. Detectează daca mesajul este vulgar
    vulgar_check, _ = get_llm_response(query, system_prompt=VULGAR_DETECT_PROMPT)
    vulgar_check = vulgar_check.strip().lower()
    #print(f"Vulgar detection: {vulgar_check}")

    if vulgar_check == "vulgar":
        return {"vulgar_message": "Your request contains inappropriate language or content. No recommendations can be made."}

    # 2. Modeleaza mesajul sa fie mai clar
    clarified_query, _ = get_llm_response(query, system_prompt=CLARIFY_PROMPT)

    #print(f"Clarified query: {clarified_query}")

    # 3. Extrage genul din mesaj, este folosit ptr filtrare
    user_genre, _ = get_llm_response(clarified_query, system_prompt=GENRE_PROMPT)
    user_genre = user_genre.strip().lower()
    #print(f"User genre: {user_genre}")
    
    if user_genre == "any":
        return {"any_message": "Can't find any suitable books."}

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
        #print(f"Checking book: {metadata['title']} with genre: {genre} and distance: {distance}")
        if user_genre != "any":
            sub_genres = [g.strip() for g in genre.split('/')]
            #print(f"Sub-genres: {sub_genres} - User genre in sub-genres: {user_genre in sub_genres}")
            if user_genre not in sub_genres:
                continue
        recommendations.append({
            "title": metadata["title"],
            "genre": metadata["genre"],
            "author": metadata.get("author", ""),
            "image": metadata.get("image", "")
        })
        if len(recommendations) >= n_results:
            break

    return recommendations
