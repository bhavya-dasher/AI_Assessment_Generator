import requests
import json
from config import OLLAMA_URL, MODEL, OLLAMA_TIMEOUT

def generate_quiz(study_text: str, num_questions: int = 10) -> list[dict]:
    prompt = f"""
You are an expert quiz generator for students.
Analyze the study material below and generate exactly {num_questions} multiple choice questions.

STRICT RULES:
- Each question must have exactly 4 options labeled A, B, C, D
- Only one correct answer per question
- Include a brief explanation for the correct answer
- Questions must be based ONLY on the provided material
- Respond ONLY with valid JSON, no extra text

JSON format:
{{
  "questions": [
    {{
      "question": "Your question here?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "answer": "A",
      "explanation": "Brief reason why A is correct"
    }}
  ]
}}

Study Material:
\"\"\"
{study_text}
\"\"\"
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=OLLAMA_TIMEOUT
        )
        response.raise_for_status()
        raw = response.json().get("response", "")
        parsed = json.loads(raw)
        return parsed.get("questions", [])

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Ollama is not running. Start it with: ollama serve")
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON. Try again.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")