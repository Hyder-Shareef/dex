import httpx

from app.config import settings


def is_configured() -> bool:
    return bool(settings.mastodon_instance_url and settings.mastodon_access_token)


def publish(text: str) -> dict:
    if not is_configured():
        raise RuntimeError("Mastodon is not configured (MASTODON_INSTANCE_URL / MASTODON_ACCESS_TOKEN missing).")

    base = settings.mastodon_instance_url.rstrip("/")
    with httpx.Client(timeout=15) as client:
        resp = client.post(
            f"{base}/api/v1/statuses",
            headers={"Authorization": f"Bearer {settings.mastodon_access_token}"},
            data={"status": text},
        )
        resp.raise_for_status()
        result = resp.json()

    return {"uri": result.get("uri"), "url": result.get("url")}
