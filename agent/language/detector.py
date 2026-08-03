from langdetect import detect, LangDetectException


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.

    Returns:
        ISO language code
        Example:
            en
            fr
            de
            ar
            ja
            hi
    """

    try:
        return detect(text)
    except LangDetectException:
        return "unknown"