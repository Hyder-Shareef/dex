from pydantic import BaseModel

from app.models import POST_STATUSES


class GenerateRequest(BaseModel):
    topic: str
    keywords: str | None = None
    link: str | None = None
    platforms: list[str] | None = None  # None = all supported platforms


class PostOut(BaseModel):
    id: int
    topic: str
    keywords: str | None
    link: str | None
    status: str
    platform_posts: str | None
    image_url: str | None
    publish_results: str | None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class StatusUpdate(BaseModel):
    status: str

    def validate_status(self):
        if self.status not in POST_STATUSES:
            raise ValueError(f"Invalid status. Allowed: {', '.join(POST_STATUSES)}")
