import re


def extract_features(text: str):
    """
    Extract meaningful semantic words from a venue name.

    Example:

    Joe's Texas Steakhouse & Grill

    →

    ["texas", "steakhouse", "grill"]
    """

    if not text:
        return []

    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    words = text.split()

    stop_words = {

        "the",
        "and",
        "of",
        "at",
        "by",
        "restaurant",
        "cafe",
        "bar",
        "pub",
        "hotel",
        "club",
        "co",
        "company",
        "inc",
        "llc",
        "ltd",

        "mr",
        "mrs",
        "dr",

        "my",
        "our",
        "your",

    }

    features = []

    for word in words:

        if len(word) <= 2:
            continue

        if word in stop_words:
            continue

        features.append(word)

    return features