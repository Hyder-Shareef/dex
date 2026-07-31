import re


def image_url_for(description: str) -> str:
    """Pollinations.ai generates an image on-the-fly from a URL-encoded prompt — free, no API key."""
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", description).strip()
    slug = re.sub(r"\s+", "-", slug)
    return f"https://image.pollinations.ai/prompt/{slug}"
