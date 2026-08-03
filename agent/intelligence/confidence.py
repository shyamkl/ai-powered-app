def confidence_level(score:float):

    """
    Converts a similarity score into a confidence level.
    """
    if score>=0.80:
        return "HIGH"
    if score>=0.60:
        return "MEDIUM"

    return "LOW"

def needs_fallback(score: float):

    """
    Returns True when the classifier should
    gather more evidence.
    """

    return score < 0.60       
