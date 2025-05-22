#cache.py
import json
import os

CACHE_FILE = "cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cached_result(key):
    cache = load_cache()
    return cache.get(key)

def set_cached_result(key, value):
    cache = load_cache()
    cache[key] = value
    save_cache(cache)
