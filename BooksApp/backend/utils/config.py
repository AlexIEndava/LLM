# backend/utils/config.py

import os
from dotenv import load_dotenv

# Încarcă variabilele din .env din backend/
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Extrage cheia OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Lipsește cheia OPENAI_API_KEY în .env")

# Director pentru ChromaDB (opțional suprascris și din .env)
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")
