import httpx

from app.config import settings

API_URL = "https://api.linkedin.com/rest/posts"


def is_configured() -> bool:
    return bool(settings.linkedin_access_token and settings.linkedin_person_urn)


def publish(text: str) -> dict:
    if not is_configured():
        raise RuntimeError(
            "LinkedIn is not configured (requires an app approved by LinkedIn for the w_member_social scope)."
        )

    payload = {
        "author": settings.linkedin_person_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    with httpx.Client(timeout=15) as client:
        resp = client.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {settings.linkedin_access_token}",
                "LinkedIn-Version": "202401",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            json=payload,
        )
        resp.raise_for_status()
        post_id = resp.headers.get("x-restli-id", "")

    return {"uri": post_id, "url": None}
