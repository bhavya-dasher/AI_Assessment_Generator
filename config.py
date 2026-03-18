import os

# --- Ollama Settings ---
OLLAMA_URL = "http://192.168.200.44:11434/api/generate"
MODEL = "qwen2.5:3b"
OLLAMA_TIMEOUT = 600  # seconds

# --- Quiz Settings ---
DEFAULT_QUESTIONS = 10
MIN_QUESTIONS = 5
MAX_QUESTIONS = 20
QUESTIONS_STEP = 5
MIN_WORDS_IN_PDF = 50        # Warn user if PDF has less than this

# --- File Storage ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = ["pdf"]