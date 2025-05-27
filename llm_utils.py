#llm_utils.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

client = InferenceClient(
    provider="auto",
    api_key= "",
)

def extract_entities_from_question(question):
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Z tego pytania wyodrębnij wszystkie encje (osoby, organizacje, miejsca, itp.). "
                        f"Zwróć tylko listę nazw rozdzieloną przecinkami, bez żadnych innych słów:\n{question}"
                    )
                }
            ],
        )
        answer = completion.choices[0].message["content"].strip()
        print(f"Model raw response: '{answer}'")  # DEBUG

        entities = [clean_entity_text(e) for e in answer.split(",") if e.strip()]
        print(f"Extracted entities: {entities}")  # DEBUG
        return entities
    except Exception as e:
        print("[❌] Błąd podczas wywołania HF InferenceClient:", e)
        return []

def clean_entity_text(text):
    return text.strip().strip('"').strip("'").strip()
