#kg_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_knowledge_graph_list(query, limit=5):
    url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        "query": query,
        "key": API_KEY,
        "limit": limit,
        "indent": True,
        "languages": "pl"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "itemListElement" in data:
            return [item["result"] for item in data["itemListElement"]]
        return []
    except requests.exceptions.RequestException as e:
        print("[❌] Błąd połączenia z Google Knowledge Graph API:", e)
        return []
