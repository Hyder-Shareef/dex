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
    "You are an elite multi-channel social media copywriter and brand strategist. "
    "Given a campaign topic, raw product description, or story brief, your job is to "
    "INTELLIGENTLY SYNTHESIZE the core value proposition and write RADICALLY DIFFERENT, "
    "PLATFORM-NATIVE copy for each requested channel.\n\n"
    "CRITICAL RULES:\n"
    "1. NEVER repeat, dump, or copy-paste the raw input description verbatim into any post.\n"
    "2. EXTRACT the product/concept name, core benefits, target audience, and key problem solved.\n"
    "3. REFRAME the copy with distinct psychological hooks tailored to each platform's culture:\n"
    "   - LinkedIn: Professional thought leadership, workplace/lifestyle productivity, structured bullet points, reflective peer question.\n"
    "   - Instagram: Aesthetic lifestyle storytelling, punchy opening line, visual spacing, emoji accents, clean hashtag cluster, link in bio CTA.\n"
    "   - X: Ultra-concise, under 280 characters strict including hashtags, punchy thread hook or bulleted spec list.\n"
    "   - TikTok: High-energy creator POV caption + an explicit [Video Concept] describing visual and audio direction in 15-30s.\n"
    "   - Threads: Casual, authentic hot take or debate starter ending in an engaging question.\n"
    "   - Facebook: Warm, community-oriented recommendation with practical benefits.\n"
    "   - Bluesky: Sharp, non-corporate conversational perspective (< 300 chars).\n"
    "   - Mastodon: Open-web, tech/sustainability/thoughtful community focus (< 500 chars).\n"
    "   - YouTube Shorts: Punchy title (< 60 chars) + hook description + quick visual breakdown.\n\n"
    "Respond ONLY with a JSON object of this exact shape:\n"
    "{\n"
    '  "name": "<concise 3-5 word campaign label>",\n'
    '  "image_description": "<vivid, artistic visual description of an image for AI generation without text>",\n'
    '  "platform_posts": {\n'
    '    "<platform_key>": {\n'
    '      "post": "<the bespoke platform post text>",\n'
    '      "hashtags": ["<tag1>", "<tag2>"],\n'
    '      "call_to_action": "<short CTA>"\n'
    '    }\n'
    "  }\n"
    "}\n"
)


def _extract_brief(topic: str, keywords: str | None) -> dict:
    """Intelligently parse product names, benefits, and categories from freeform input."""
    import re

    # Try extracting bold product name like **EcoFlow Smart Water Bottle**
    bold_match = re.search(r"\*\*([^*]+)\*\*", topic)
    first_line = topic.strip().split("\n")[0].replace("###", "").replace("Product Description", "").strip()

    if bold_match and len(bold_match.group(1)) < 60:
        name = bold_match.group(1).strip()
    elif first_line and len(first_line) < 60 and not first_line.lower().startswith("http"):
        name = first_line
    else:
        # Fallback to first few words
        words = topic.replace("\n", " ").split()
        name = " ".join(words[:4]) if len(words) >= 4 else topic[:30]

    # Extract bullet points
    raw_bullets = re.findall(r"^[*-•]\s*(.+)$", topic, flags=re.MULTILINE)
    bullets = [b.strip() for b in raw_bullets if len(b.strip()) > 3]

    if not bullets:
        # Split sentences as fallback benefits
        sentences = [s.strip() for s in re.split(r"[.!?]\s+", topic) if len(s.strip()) > 15]
        bullets = sentences[1:5] if len(sentences) > 1 else [topic[:100]]

    # Parse tags
    kw_tags = [k.strip().lower().replace(" ", "").replace("#", "") for k in (keywords or "").split(",") if k.strip()]
    if not kw_tags:
        # Derive intelligent tags from extracted name
        clean_words = [re.sub(r"[^a-zA-Z]", "", w).lower() for w in name.split() if len(w) > 3]
        kw_tags = clean_words[:3] or ["innovation", "lifestyle", "growth"]

    return {
        "name": name,
        "bullets": bullets,
        "tags": kw_tags,
        "clean_name": re.sub(r"[^a-zA-Z0-9\s]", "", name).strip(),
    }


def _mock_generate_content(topic: str, keywords: str | None, link: str | None, platforms: list[str]) -> dict:
    info = _extract_brief(topic, keywords)
    p_name = info["name"]
    bullets = info["bullets"]
    tags = info["tags"]
    link_cta = f" Check it out: {link}" if link else ""
    link_bio = " Tap link in bio to shop the drop." if not link else f" Explore now: {link}"

    b1 = bullets[0] if len(bullets) > 0 else "Engineered for maximum daily performance"
    b2 = bullets[1] if len(bullets) > 1 else "Built with premium, sustainable materials"
    b3 = bullets[2] if len(bullets) > 2 else "Designed to simplify your daily routine"

    templates = {
        "linkedin": {
            "post": (
                f"Sustainable daily performance is defined by the tools we choose to integrate into our workflow.\n\n"
                f"When evaluating high-utility everyday design, three factors determine whether a product actually creates lasting impact:\n\n"
                f"• {b1}\n"
                f"• {b2}\n"
                f"• {b3}\n\n"
                f"The {p_name} was developed around these exact principles — stripping away daily friction while elevating durability and sustainable habits.\n\n"
                f"How is your team rethinking everyday lifestyle upgrades this quarter?{link_cta}"
            ),
            "hashtags": tags + ["ProductDesign", "Innovation", "SustainableLiving"],
            "call_to_action": "Join the discussion in the comments below.",
        },
        "instagram": {
            "post": (
                f"Hydration and lifestyle, elevated. ✨💧\n\n"
                f"Meet the all-new {p_name} — crafted for those who refuse to choose between sleek aesthetics and heavy-duty daily performance.\n\n"
                f"From morning commutes to late-night studio sessions:\n"
                f"❄️ {b1}\n"
                f"🔒 {b2}\n"
                f"🌿 {b3}\n\n"
                f"Built to move with you wherever you go.{link_bio}"
            ),
            "hashtags": tags + ["aesthetic", "dailydrop", "lifestyleessentials", "minimaldesign"],
            "call_to_action": "Double tap and tap the link in bio for full specs.",
        },
        "x": {
            "post": (
                f"Say goodbye to cheap gear that fails when you need it most.\n\n"
                f"Introducing {p_name} 🧵\n"
                f"→ {b1}\n"
                f"→ {b2}\n"
                f"→ {b3}\n\n"
                f"Full breakdown below 👇{link_cta}"
            ),
            "hashtags": tags[:2],
            "call_to_action": "Drop a reply with your take!",
        },
        "tiktok": {
            "post": (
                f"POV: You finally stopped buying cheap essentials that fall apart after 2 weeks 😭🔥\n\n"
                f"[Video Concept: Aesthetic fast-cut morning routine. Close-up on the sleek finish of {p_name}, testing {b1}, quick drop test for durability, smooth sound effects.]\n\n"
                f"Link in bio before this batch sells out! ⚡"
            ),
            "hashtags": tags + ["fyp", "tiktokmademebuyit", "upgrade", "unboxing"],
            "call_to_action": "Follow for daily product deep dives and check bio!",
        },
        "threads": {
            "post": (
                f"Unpopular opinion: If a daily essential leaks, breaks, or underperforms even once, it's immediately disqualified.\n\n"
                f"We spent the last few weeks testing {p_name} across commute, gym, and desk setups:\n"
                f"- {b1}\n"
                f"- {b2}\n\n"
                f"The verdict? It actually delivers where others cut corners.\n\n"
                f"What's your biggest pet peeve with current alternatives?"
            ),
            "hashtags": tags[:3],
            "call_to_action": "Drop your thoughts below.",
        },
        "facebook": {
            "post": (
                f"Looking for an upgrade you'll actually use every single day? 🌟\n\n"
                f"We're excited to introduce the {p_name}! Designed for work, workouts, and travel, it solves everyday annoyances:\n\n"
                f"✅ {b1}\n"
                f"✅ {b2}\n"
                f"✅ {b3}\n\n"
                f"Say hello to better habits and zero compromise.{link_cta}"
            ),
            "hashtags": tags + ["community", "productreview", "dailyessentials"],
            "call_to_action": "Tag a friend who needs this upgrade!",
        },
        "bluesky": {
            "post": (
                f"Deep dive into {p_name}: no corporate fluff, just solid engineering.\n\n"
                f"Key highlights:\n"
                f"• {b1}\n"
                f"• {b2}\n\n"
                f"Curious to hear what the community thinks.{link_cta}"
            ),
            "hashtags": tags[:2],
            "call_to_action": "What are your thoughts on this?",
        },
        "mastodon": {
            "post": (
                f"Reflecting on sustainable hardware and intentional design: {p_name}.\n\n"
                f"Rather than disposable culture, the focus is on long-term durability:\n"
                f"• {b1}\n"
                f"• {b2}\n\n"
                f"Open discussions on sustainable consumer choices are always welcome.{link_cta}"
            ),
            "hashtags": tags + ["Sustainability", "ProductDesign", "OpenWeb"],
            "call_to_action": "Boosts and replies appreciated!",
        },
        "youtube_shorts": {
            "post": (
                f"Does {p_name} Actually Live Up to the Hype?\n\n"
                f"[Video Concept: Fast 60-second test putting {b1} and {b2} through real-world stress tests. Split screen comparison with budget alternatives. Dynamic hook in the first 3 seconds.]"
            ),
            "hashtags": tags[:3] + ["shorts", "test", "review"],
            "call_to_action": "Subscribe for more rapid product breakdowns!",
        },
    }

    platform_posts = {}
    for p in platforms:
        if p in templates:
            platform_posts[p] = templates[p]
        else:
            platform_posts[p] = {
                "post": f"Introducing {p_name}: {b1}.{link_cta}",
                "hashtags": tags,
                "call_to_action": "Learn more.",
            }

    return {
        "name": f"{p_name[:30]} Campaign",
        "image_description": f"Cinematic minimalist product photography of {p_name}, dramatic studio lighting, ultra high detail",
        "platform_posts": platform_posts,
    }


def generate_content(topic: str, keywords: str | None, link: str | None, platforms: list[str]) -> dict:
    if not settings.llm_api_key:
        return _mock_generate_content(topic, keywords, link, platforms)

    client = get_client()
    user_prompt = (
        f"CAMPAIGN BRIEF / PRODUCT INPUT:\n{topic}\n\n"
        f"FOCUS KEYWORDS: {keywords or 'extract from brief'}\n"
        f"TARGET LINK: {link or 'none'}\n"
        f"GENERATE BESPOKE POSTS FOR EXACTLY THESE PLATFORMS: {', '.join(platforms)}\n\n"
        f"REMINDER: Do NOT regurgitate the raw input text. Rewrite and synthesize native copy tailored to each platform!"
    )
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)
