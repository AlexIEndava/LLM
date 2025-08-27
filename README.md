# 📚 BooksApp – Smart Librarian

> **A modern AI-powered web app for book recommendations, summaries, TTS/STT, and interactive bookshelf UI.**

![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/flask-web%20app-lightgrey?logo=flask)
![OpenAI](https://img.shields.io/badge/openai-embeddings%20%7C%20chat-green?logo=openai)
![ChromaDB](https://img.shields.io/badge/chromadb-vector%20store-orange?logo=databricks)

---

## ✨ Features

- **Semantic Book Recommendation:** Find relevant books by theme, genre, or keywords using OpenAI embeddings and ChromaDB.
- **Conversational Chatbot:** Natural language queries, moderation, and intent detection.
- **Text-to-Speech & Speech-to-Text:** Listen to summaries or dictate your queries.
- **Book Cover Generation:** Create or delete AI-generated book cover images.
- **Interactive Bookshelf UI:** Modern, responsive interface with animated cards and sections.
- **Automatic Moderation:** Filters offensive or irrelevant queries.

---

## 🚀 Quickstart

```bash
git clone https://github.com/AlexIEndava/LLM.git
cd BooksApp

# Add your OpenAI key in backend/.env
echo "OPENAI_API_KEY=sk-..." > backend/.env
PERSIST_DIRECTORY=./backend/data/chroma_db

pip install -r requirements.txt
cd BooksApp
python -m backend.services.embedding_service  (for updating ChromaDB)
python -m backend.app
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🗂️ Project Structure

```
BooksApp/
│
├── backend/
│   │   .env                  # Environment variables (API keys, config)
│   │   app.py                # Main Flask app, registers all routes and serves frontend
│   │
│   ├── data/
│   │   │   book_summaries.json   # Main book database (title, author, genre, description, image)
│   │   │
│   │   ├── book_images/         # AI-generated book cover images (PNG)
│   │   │   └── *.png
│   │   │
│   │   └── chroma_db/           # ChromaDB vector store files (for semantic search)
│   │       ├── chroma.sqlite3
│   │       └── ... (binary index files)
│   │
│   ├── routes/                  # Flask blueprints for API endpoints
│   │   │   recommend.py         # Book recommendation logic (semantic search, moderation)
│   │   │   generate_image.py    # Generate book cover images using OpenAI
│   │   │   delete_image.py      # Delete book cover images
│   │   │   library.py           # Library management (list all books)
│   │   │   summary.py           # Get book summary by title
│   │   │   speech_to_text.py    # Speech-to-text endpoint (audio to text)
│   │   │   tts.py               # Text-to-speech endpoint (summary to audio)
│   │   │   __init__.py
│   │
│   ├── services/                # Core business logic and integrations
│   │   │   embedding_service.py # Generate and store embeddings for books
│   │   │   llm_client.py        # OpenAI API client (LLM, embeddings, TTS, STT, image)
│   │   │   retriever.py         # Recommendation and retrieval logic
│   │   │   summary_service.py   # Service for fetching book summaries
│   │
│   ├── utils/
│       │   config.py            # Configuration constants (API keys, paths)
│   
│
└── fronted/
    │   index.html               # Main web UI (loads components dynamically)
    │
    ├── components/
    │   │   header.html          # Header/navigation bar
    │   │   library.html         # Library section (all books)
    │   │   recommend.html       # Recommendation section (query, results)
    │
    ├── css/
    │   │   styles.css           # Main stylesheet
    │
    └── js/
        │   app.js              # Main frontend logic (UI, API calls, TTS/STT, image actions)
```

---

## 💡 Example Usage

- **Ask for recommendations:**  
  Type or dictate a query like `Suggest a fantasy book about courage` and receive relevant book cards.
- **Flip a card:**  
  Click a book card to see its summary and listen to it via TTS.
- **Generate or delete covers:**  
  Use the buttons to create or remove AI-generated book covers.
- **Browse your library:**  
  Switch between recommendations and your full book collection.

---

## ⚙️ Requirements

- Python 3.9+
- Flask
- OpenAI API key (`OPENAI_API_KEY`)
- ChromaDB (for local vector store)
- Modern browser (for UI and speech features)

---

## 📖 Add More Books

- Edit `backend/data/book_summaries.json` to add new books (title, author, genre, description, image).
- Run `python backend/services/embedding_service.py` to update embeddings.

---

## 📝 License

MIT License

---

> Made with ❤️ for book lovers and AI enthusiasts.
