# Platform Connector & Style Specifications

> **Channel Adaptation Rules & Integration Protocols**

Post Agent applies custom tone, length constraints, hashtag density, and call-to-action strategies across 9 target platforms.

---

## 1. Platform Matrix & Style Guide

### LinkedIn (`linkedin`)
- **Tone**: Professional, insightful, industry-oriented, analytical.
- **Length**: 3–4 concise paragraphs/sentences.
- **Hashtags**: 3–5 targeted industry tags (e.g., `#AI #Productivity #Engineering`).
- **Call-to-Action**: Prompts peer discussion or comments (*"What strategies have worked best for your team?"*).
- **Connector**: LinkedIn REST API (`POST /v2/ugcPosts`).
- **Required Env Vars**: `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`.

---

### X / Twitter (`x`)
- **Tone**: Concise, punchy, conversational, hook-oriented.
- **Length**: Strict < 280 characters (including hashtags and URLs).
- **Hashtags**: 1–2 high-velocity topic tags.
- **Call-to-Action**: Retweet / reply engagement (*"Drop your take below 🧵"*).
- **Connector**: X API v2 via Tweepy Client.
- **Required Env Vars**: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`.

---

### Bluesky (`bluesky`)
- **Tone**: Casual, community-first, anti-corporate, witty.
- **Length**: Strict < 300 characters.
- **Hashtags**: 1–2 tags.
- **Call-to-Action**: Conversational prompt without corporate jargon.
- **Connector**: AT Protocol (`app.bsky.feed.post`).
- **Required Env Vars**: `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` (App Passwords created at `bsky.app/settings/app-passwords`).

---

### Mastodon (`mastodon`)
- **Tone**: Open-web, tech/academic focus, community-driven.
- **Length**: < 500 characters.
- **Hashtags**: 3–5 camelCase hashtags for accessibility (e.g., `#SocialAgent #TechTrends`).
- **Call-to-Action**: Boosts and replies friendly.
- **Connector**: Mastodon REST API (`POST /api/v1/statuses`).
- **Required Env Vars**: `MASTODON_INSTANCE_URL`, `MASTODON_ACCESS_TOKEN`.

---

### Instagram (`instagram`)
- **Tone**: Visual storytelling, inspirational, emoji accents.
- **Length**: 2–3 sentences followed by hashtag block.
- **Hashtags**: 5–10 relevant discovery tags.
- **Call-to-Action**: *"Swipe to learn more"*, *"Link in bio"*, or *"Save this for later"*.
- **Connector**: Meta Graph API for Instagram Professional (`POST /{ig-user-id}/media`).
- **Required Env Vars**: `META_PAGE_ACCESS_TOKEN`, `META_IG_USER_ID`.

---

### Facebook (`facebook`)
- **Tone**: Accessible, engaging, community-oriented.
- **Length**: 2–3 sentences.
- **Hashtags**: 2–3 tags.
- **Call-to-Action**: *"Share with your community"* or *"Let us know your experience in the comments"*.
- **Connector**: Meta Graph API Page Feed (`POST /{page-id}/feed`).
- **Required Env Vars**: `META_PAGE_ACCESS_TOKEN`, `META_PAGE_ID`.

---

### Threads (`threads`)
- **Tone**: Unfiltered, authentic, casual question or perspective.
- **Length**: 1–2 short paragraphs.
- **Hashtags**: 1–2 tags.
- **Call-to-Action**: Discussion question designed to spark replies.
- **Connector**: Meta Graph API / Content Studio.

---

### TikTok (`tiktok`)
- **Tone**: Energetic, trend-conscious, fast hook.
- **Output**: 1–2 sentence caption + structured visual concept idea.
- **Hashtags**: `#fyp` + trending niche tags.
- **Call-to-Action**: *"Follow for part 2"*, *"Save this tip"*.

---

### YouTube Shorts (`youtube_shorts`)
- **Tone**: High curiosity, retention-optimized.
- **Output**: Punchy title (< 60 chars) + description + fast-paced video concept.
- **Hashtags**: `#shorts` + 2–3 content tags.
- **Call-to-Action**: *"Subscribe for daily deep dives"*.

---

## 2. Connector Authentication Setup

| Channel | Setup URL | Credentials Needed |
|---|---|---|
| **Bluesky** | [bsky.app/settings/app-passwords](https://bsky.app/settings/app-passwords) | Handle + App Password (Instant) |
| **Mastodon** | `https://<your-instance>/settings/applications` | Instance URL + Access Token (Instant) |
| **X (Twitter)** | [developer.x.com](https://developer.x.com/) | API Key, Secret, Access Token & Secret |
| **LinkedIn** | [linkedin.com/developers/apps](https://www.linkedin.com/developers/apps) | Access Token with `w_member_social`, Person URN |
| **Meta** | [developers.facebook.com](https://developers.facebook.com/) | Page Token, Page ID, Instagram Business ID |
