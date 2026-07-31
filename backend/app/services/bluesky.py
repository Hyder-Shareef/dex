from datetime import datetime, timezone

import httpx

from app.config import settings

BASE_URL = "https://bsky.social/xrpc"


def is_configured() -> bool:
    return bool(settings.bluesky_handle and settings.bluesky_app_password)


def publish(text: str) -> dict:
    """Post to Bluesky via the AT Protocol. Returns {url, uri} on success, raises on failure."""
    if not is_configured():
        raise RuntimeError("Bluesky is not configured (BLUESKY_HANDLE / BLUESKY_APP_PASSWORD missing).")

    with httpx.Client(timeout=15) as client:
        session_resp = client.post(
            f"{BASE_URL}/com.atproto.server.createSession",
            json={"identifier": settings.bluesky_handle, "password": settings.bluesky_app_password},
        )
        session_resp.raise_for_status()
        session = session_resp.json()

        record = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        }
        post_resp = client.post(
            f"{BASE_URL}/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {session['accessJwt']}"},
            json={
                "repo": session["did"],
                "collection": "app.bsky.feed.post",
                "record": record,
            },
        )
        post_resp.raise_for_status()
        result = post_resp.json()

    post_id = result["uri"].split("/")[-1]
    handle = settings.bluesky_handle.lstrip("@")
    return {"uri": result["uri"], "url": f"https://bsky.app/profile/{handle}/post/{post_id}"}
