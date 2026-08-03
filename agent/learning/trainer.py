from agent.learning.memory import (
    load_memory,
    save_memory,
)

from agent.intelligence.embedder import embed


def learn(text: str, category: str):

    memory = load_memory()

    memory.append(
        {
            "text": text,
            "embedding": embed(text).tolist(),
            "category": category,
        }
    )

    save_memory(memory)