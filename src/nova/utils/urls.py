"""URL helpers."""


def normalize_google_sheet_url(url: str) -> str:
    """Clean a Google Sheet URL: strip query params (?usp=sharing etc) and fragments."""
    if not url or not isinstance(url, str):
        return url
    stripped = url.strip()
    for sep in ("?", "#"):
        if sep in stripped:
            stripped = stripped.split(sep)[0].strip()
    return stripped
