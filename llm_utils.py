#llm_utils.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

client = InferenceClient(
    provider="auto",
    api_key=HUGGINGFACE_TOKEN,
)

def extract_entity_from_question(question):
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Wyodrębnij dokładnie nazwę głównej encji (osoby, rzeczy lub pojęcia) z tego pytania. "
                        f"Zwróć tylko tę nazwę bez dodatkowych słów:\n{question}"
                    )
                }
            ],
        )
        answer = completion.choices[0].message["content"].strip()
        print(f"Model response: '{answer}'")  # DEBUG
        entity = clean_entity_text(answer)
        print(f"Cleaned entity: '{entity}'")  # DEBUG
        return entity
    except Exception as e:
        print("[❌] Błąd podczas wywołania HF InferenceClient:", e)
        return "Błąd zapytania"

def clean_entity_text(text):
    # Spróbuj usunąć cudzysłowy, kropki i zbędne spacje
    text = text.strip().strip('"').strip("'").strip()
    return text
