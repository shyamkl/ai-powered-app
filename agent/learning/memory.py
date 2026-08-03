import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "corrections.json"


def load_memory():

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8")as f:

        json.dump(
            memory,
            f,
            indent=4,
            ensure_ascii=False,
        )