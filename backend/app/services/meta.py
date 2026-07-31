import httpx

from app.config import settings

GRAPH_URL = "https://graph.facebook.com/v20.0"


def facebook_configured() -> bool:
    return bool(settings.meta_page_access_token and settings.meta_page_id)


def instagram_configured() -> bool:
    return bool(settings.meta_page_access_token and settings.meta_ig_user_id)


def publish_facebook(text: str) -> dict:
    if not facebook_configured():
        raise RuntimeError("Facebook is not configured (requires a Meta app reviewed for page publishing).")

    with httpx.Client(timeout=15) as client:
        resp = client.post(
            f"{GRAPH_URL}/{settings.meta_page_id}/feed",
            data={"message": text, "access_token": settings.meta_page_access_token},
        )
        resp.raise_for_status()
        result = resp.json()

    post_id = result.get("id", "")
    return {"uri": post_id, "url": f"https://facebook.com/{post_id}" if post_id else None}


def publish_instagram(caption: str, image_url: str) -> dict:
    if not instagram_configured():
        raise RuntimeError("Instagram is not configured (requires a Meta app reviewed for IG publishing).")
    if not image_url:
        raise RuntimeError("Instagram requires an image; none was generated for this post.")

    with httpx.Client(timeout=20) as client:
        container_resp = client.post(
            f"{GRAPH_URL}/{settings.meta_ig_user_id}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": settings.meta_page_access_token,
            },
        )
        container_resp.raise_for_status()
        creation_id = container_resp.json()["id"]

        publish_resp = client.post(
            f"{GRAPH_URL}/{settings.meta_ig_user_id}/media_publish",
            data={"creation_id": creation_id, "access_token": settings.meta_page_access_token},
        )
        publish_resp.raise_for_status()
        result = publish_resp.json()

    post_id = result.get("id", "")
    return {"uri": post_id, "url": None}
