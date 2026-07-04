import re


def slugify(text: str) -> str:
    """Convert text into a lowercase, hyphen-separated slug."""
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to length characters, appending suffix if shortened."""
    if len(text) <= length:
        return text
    return text[:length] + suffix


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same forwards and backwards, ignoring
    case, spaces, and punctuation."""
    normalized = re.sub(r"[^\w]", "", text).lower()
    return normalized == normalized[::-1]
