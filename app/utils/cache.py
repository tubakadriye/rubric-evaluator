import json, hashlib, os

CACHE_FILE = "cache.json"


def cache_key(text):
    return hashlib.md5(text.encode()).hexdigest()


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE) as f:
        return json.load(f)


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def cached_call(key, fn):
    cache = load_cache()

    if key in cache:
        return cache[key]

    result = fn()
    cache[key] = result
    save_cache(cache)

    return result