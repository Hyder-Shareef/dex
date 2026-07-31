import hmac

from fastapi import Header, HTTPException, Query

from app.config import settings


def require_site_password(
    x_site_password: str | None = Header(None),
    site_password: str | None = Query(None),
):
    """No-op if SITE_PASSWORD isn't set (local dev). Otherwise gates every route below."""
    if not settings.site_password:
        return
    provided = x_site_password or site_password
    if not provided or not hmac.compare_digest(provided, settings.site_password):
        raise HTTPException(401, "Invalid site password.")
