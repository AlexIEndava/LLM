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
git clone https://github.com/username/BooksApp.git
cd BooksApp

# Add your OpenAI key in backend/.env
echo "OPENAI_API_KEY=sk-..." > backend/.env

pip install -r requirements.txt
python backend/app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🗂️ Project Structure

```
BooksApp/
│
├── backend/
│   ├── app.py                  # Flask server, main routes
│   ├── .env                    # API keys and config
│   ├── data/
│   │   ├── book_summaries.json # Book database (title, author, genre, description, image)
│   │   ├── book_images/        # Book cover images
│   │   └── chroma_db/          # ChromaDB vector store files
│   ├── routes/                 # Flask blueprints for API endpoints
│   │   ├── recommend.py        # Book recommendation logic
│   │   ├── generate_image.py   # Book cover generation
│   │   ├── delete_image.py     # Book cover deletion
│   │   ├── library.py          # Library management
│   │   ├── summary.py          # Book summary endpoint
│   │   ├── speech_to_text.py   # Speech-to-text endpoint
│   │   └── tts.py              # Text-to-speech endpoint
│   ├── services/
│   │   ├── embedding_service.py# Embedding generation and storage
│   │   ├── llm_client.py       # LLM API client
│   │   ├── openai_client.py    # OpenAI API integration
│   │   └── retriever.py        # Book retriever logic
│   └── utils/
│       └── config.py           # Configuration and constants
│
├── fronted/
│   ├── index.html              # Main web UI
│   ├── components/
│   │   ├── header.html
│   │   ├── library.html
│   │   └── recommend.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
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
