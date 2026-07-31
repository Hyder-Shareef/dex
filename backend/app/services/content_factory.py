import json

from app.config import settings
from app.services.llm_client import get_client

SUPPORTED_PLATFORMS = [
    "linkedin",
    "instagram",
    "facebook",
    "x",
    "bluesky",
    "mastodon",
    "tiktok",
    "threads",
    "youtube_shorts",
]

PLATFORM_GUIDELINES = {
    "linkedin": (
        "Professional and insightful, 3-4 sentences, business-oriented tone. "
        "End with a call to action that invites comments or discussion."
    ),
    "instagram": (
        "Visual storytelling, 2-3 sentences, inspirational tone with light emoji use. "
        "Call to action like 'swipe to learn more' or 'link in bio'."
    ),
    "facebook": (
        "Friendly and community-focused, 2-3 sentences, conversational. "
        "Call to action that invites likes/shares/comments."
    ),
    "x": (
        "Concise and impactful, under 280 characters total including hashtags. "
        "Spark curiosity or discussion."
    ),
    "bluesky": (
        "Concise, under 300 characters total including hashtags. Conversational, no corporate tone."
    ),
    "mastodon": (
        "Conversational and community-driven, under 500 characters. Can be slightly longer-form than X/Bluesky."
    ),
    "tiktok": (
        "Fun, energetic caption for a short video, 1-2 sentences plus a suggested video concept."
    ),
    "threads": (
        "Casual, conversational, 1-2 short paragraphs, ending with a question to spark replies."
    ),
    "youtube_shorts": (
        "A short punchy title (under 60 characters) plus a 1-2 sentence description and a suggested video concept."
    ),
}

SYSTEM_PROMPT = (
    "You are a social media content generation assistant. Given a topic, optional "
    "keywords, and an optional link, you write platform-specific posts.\n\n"
    "Ground every post in the actual topic provided — never invent facts, statistics, "
    "or claims not implied by the topic. Keep a consistent voice across platforms while "
    "adapting length, tone, and format to each platform's norms.\n\n"
    "Respond ONLY with a JSON object of this exact shape:\n"
    "{\n"
    '  "name": "<short internal label for this post>",\n'
    '  "image_description": "<one-sentence description of an image that would suit this post, '
    'suitable as an AI image generation prompt>",\n'
    '  "platform_posts": {\n'
    '    "<platform_key>": {\n'
    '      "post": "<the post text>",\n'
    '      "hashtags": ["<tag1>", "<tag2>"],\n'
    '      "call_to_action": "<short CTA, or empty string if not applicable>"\n'
    "    },\n"
    "    ... one entry per requested platform ...\n"
    "  }\n"
    "}\n\n"
    "Platform-specific guidelines:\n"
    + "\n".join(f"- {key}: {rule}" for key, rule in PLATFORM_GUIDELINES.items())
)


def generate_content(topic: str, keywords: str | None, link: str | None, platforms: list[str]) -> dict:
    client = get_client()
    user_prompt = (
        f"Topic: {topic}\n"
        f"Keywords/focus areas: {keywords or 'none provided'}\n"
        f"Link to include (if relevant): {link or 'none provided'}\n"
        f"Generate posts for exactly these platforms: {', '.join(platforms)}\n"
    )
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.6,
    )
    return json.loads(response.choices[0].message.content)
