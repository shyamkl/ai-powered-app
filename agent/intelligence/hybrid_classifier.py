from collections import defaultdict

from agent.language.translator import translate_to_english
from agent.intelligence.similarity import top_categories
from agent.services.semantic_features import extract_features
from agent.learning.retriever import retrieve
from agent.intelligence.confidence import (
    confidence_level,
    needs_fallback,
)

WEIGHTS = {
    "name": 1.0,
    "description": 0.8,
    "categories": 1.5,
    "cuisine": 1.2,
    "amenities": 0.8,
    "feature": 2.0,
    "memory": 3.0,
}


def _score_text(
    final_scores,
    text: str,
    weight: float,
    top_k: int,
):
    """
    Helper function to score any text field.
    """

    if not text:
        return

    translated = translate_to_english(text)

    results = top_categories(
        translated,
        top_k,
    )

    for category, score in results:
        final_scores[category] += score * weight


def classify(
    name: str,
    description: str = "",
    categories: str = "",
    cuisine: str = "",
    amenities: str = "",
    top_k: int = 5,
):
    """
    Global Venue Hybrid Classifier.

    Uses:

    • venue name
    • description
    • provider categories
    • cuisine
    • amenities
    • semantic features
    • learning memory
    """

    final_scores = defaultdict(float)

    # -------------------------
    # Venue Name
    # -------------------------

    _score_text(
        final_scores,
        name,
        WEIGHTS["name"],
        top_k,
    )

    # -------------------------
    # Description
    # -------------------------

    _score_text(
        final_scores,
        description,
        WEIGHTS["description"],
        top_k,
    )

    # -------------------------
    # Categories
    # -------------------------

    _score_text(
        final_scores,
        categories,
        WEIGHTS["categories"],
        top_k,
    )

    # -------------------------
    # Cuisine
    # -------------------------

    _score_text(
        final_scores,
        cuisine,
        WEIGHTS["cuisine"],
        top_k,
    )

    # -------------------------
    # Amenities
    # -------------------------

    _score_text(
        final_scores,
        amenities,
        WEIGHTS["amenities"],
        top_k,
    )

    # -------------------------
    # Semantic Features
    # -------------------------

    combined_text = " ".join(
        [
            name,
            description,
            categories,
            cuisine,
            amenities,
        ]
    )

    translated = translate_to_english(
        combined_text
    )

    features = extract_features(
        translated
    )

    for feature in features:

        results = top_categories(
            feature,
            top_k,
        )

        for category, score in results:

            final_scores[category] += (
                score * WEIGHTS["feature"]
            )

    # -------------------------
    # Learning Memory
    # -------------------------

    learned = retrieve(name)

    if learned is not None:

        item, similarity = learned

        if similarity >= 0.80:

            final_scores[item["category"]] += (
                similarity * WEIGHTS["memory"]
            )

    # -------------------------
    # Ranking
    # -------------------------

    results = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    if not results:

        return {
            "prediction": "Unknown",
            "score": 0.0,
            "confidence": "LOW",
            "needs_fallback": True,
            "top_matches": [],
        }

    best_category, best_score = results[0]

    return {
        "prediction": best_category,
        "score": round(best_score, 3),
        "confidence": confidence_level(best_score),
        "needs_fallback": needs_fallback(best_score),
        "top_matches": results[:5],
    }