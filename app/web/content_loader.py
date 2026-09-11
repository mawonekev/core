import json
from functools import lru_cache
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / 'content'


@lru_cache(maxsize=None)
def get_region_content(slug: str) -> dict:
    path = CONTENT_DIR / 'regions' / f'{slug}.json'
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@lru_cache(maxsize=None)
def get_attraction_content(slug: str) -> dict:
    path = CONTENT_DIR / 'attractions' / f'{slug}.json'
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}
