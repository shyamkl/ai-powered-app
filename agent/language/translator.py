"""
translator.py

Converts text from any language into English.
This helps the agent understand venue categories globally.
"""

from deep_translator import GoogleTranslator


def translate_to_english(text: str) -> str:
    """
    Translate any language into English.

    Returns the original text if translation fails.
    """

    if not text:
        return text

    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        return translated

    except Exception as e:
        print(f"[Translator] {e}")

        return text