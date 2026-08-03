from sentence_transformers import SentenceTransformer

global_model = None

def get_model():
    global global_model

    if global_model is None:
        global_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

    return global_model


def embed(text: str):
    model = get_model()
    return model.encode(text, normalize_embeddings=True)