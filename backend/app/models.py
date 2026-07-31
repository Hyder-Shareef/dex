from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

POST_STATUSES = ["draft", "pending_approval", "approved", "rejected", "published"]


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String)
    keywords: Mapped[str | None] = mapped_column(String, nullable=True)
    link: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="draft")

    platform_posts: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON: {platform: {...}}
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    publish_results: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON: {platform: {status, detail}}

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
