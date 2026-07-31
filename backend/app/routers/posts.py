import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import require_site_password
from app.database import get_db
from app.models import POST_STATUSES, Post
from app.schemas import GenerateRequest, StatusUpdate
from app.services import bluesky, image_gen, linkedin, mastodon, meta, x_platform
from app.services.content_factory import SUPPORTED_PLATFORMS, generate_content

router = APIRouter(prefix="/api/posts", tags=["posts"], dependencies=[Depends(require_site_password)])

CONNECTORS = {
    "bluesky": bluesky,
    "mastodon": mastodon,
    "x": x_platform,
    "linkedin": linkedin,
}


def _get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found.")
    return post


@router.get("")
def list_posts(db: Session = Depends(get_db)):
    return db.execute(select(Post).order_by(Post.created_at.desc())).scalars().all()


@router.post("/generate")
def generate(payload: GenerateRequest, db: Session = Depends(get_db)):
    platforms = payload.platforms or SUPPORTED_PLATFORMS
    invalid = [p for p in platforms if p not in SUPPORTED_PLATFORMS]
    if invalid:
        raise HTTPException(400, f"Unsupported platforms: {', '.join(invalid)}")

    try:
        result = generate_content(payload.topic, payload.keywords, payload.link, platforms)
    except RuntimeError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(502, f"Error during generation: {exc}") from exc

    image_url = image_gen.image_url_for(result.get("image_description", payload.topic))

    post = Post(
        topic=payload.topic,
        keywords=payload.keywords,
        link=payload.link,
        status="pending_approval",
        platform_posts=json.dumps(result.get("platform_posts", {})),
        image_url=image_url,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.patch("/{post_id}/status")
def update_status(post_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in POST_STATUSES:
        raise HTTPException(400, f"Invalid status. Allowed: {', '.join(POST_STATUSES)}")
    post = _get_post_or_404(post_id, db)
    post.status = payload.status
    db.commit()
    db.refresh(post)
    return post


@router.post("/{post_id}/publish/{platform}")
def publish(post_id: int, platform: str, db: Session = Depends(get_db)):
    post = _get_post_or_404(post_id, db)
    if post.status != "approved":
        raise HTTPException(400, "Only approved posts can be published.")

    platform_posts = json.loads(post.platform_posts or "{}")
    if platform not in platform_posts:
        raise HTTPException(400, f"No generated content for platform '{platform}' on this post.")

    text = platform_posts[platform].get("post") or platform_posts[platform].get("caption", "")
    hashtags = platform_posts[platform].get("hashtags", [])
    full_text = text + ("\n\n" + " ".join(f"#{h.lstrip('#')}" for h in hashtags) if hashtags else "")

    results = json.loads(post.publish_results or "{}")

    try:
        if platform == "instagram":
            outcome = meta.publish_instagram(full_text, post.image_url)
        elif platform == "facebook":
            outcome = meta.publish_facebook(full_text)
        elif platform in CONNECTORS:
            outcome = CONNECTORS[platform].publish(full_text)
        else:
            raise RuntimeError(f"No publisher implemented for '{platform}' yet.")
        results[platform] = {"status": "success", **outcome}
    except Exception as exc:
        results[platform] = {"status": "error", "detail": str(exc)}

    post.publish_results = json.dumps(results)
    db.commit()
    db.refresh(post)
    return post


@router.get("/meta/platform-status")
def platform_status():
    return {
        "bluesky": bluesky.is_configured(),
        "mastodon": mastodon.is_configured(),
        "x": x_platform.is_configured(),
        "linkedin": linkedin.is_configured(),
        "facebook": meta.facebook_configured(),
        "instagram": meta.instagram_configured(),
    }
