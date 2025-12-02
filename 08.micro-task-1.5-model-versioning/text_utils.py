import re

def clean_text(text: str) -> str:
    """
    Basic text cleaning / normalisation.
    Steps:
    - Lowercase
    - Remove punctuation and non-alphanumeric characters (keep letters, numbers, spaces)
    - Collapse multiple spaces into a single space and strip leading/trailing spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
