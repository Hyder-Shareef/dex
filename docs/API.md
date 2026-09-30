# REST API Reference

> **Post Agent Backend API Specification**

Base URL: `http://localhost:8020` (Local) / Custom Deployment URL  
Interactive Docs: `/docs` (Swagger UI) & `/redoc` (ReDoc)

---

## Authentication

If `SITE_PASSWORD` is configured in `backend/.env`, all API requests (except `/api/health`) require either:
- **Header**: `X-Site-Password: <your_password>`
- **Query Parameter**: `?site_password=<your_password>`

---

## Endpoints

### 1. Health Check

Checks system availability and service health.

- **Method**: `GET`
- **Path**: `/api/health`
- **Auth Required**: No

#### Response (`200 OK`)
```json
{
  "status": "ok"
}
```

---

### 2. Generate Campaign Posts

Processes a campaign brief and generates platform-tailored post drafts and visual prompts.

- **Method**: `POST`
- **Path**: `/api/posts/generate`
- **Auth Required**: If enabled

#### Request Body
```json
{
  "topic": "Launching our next-generation AI marketing analytics suite",
  "keywords": "AI, analytics, growth, SaaS",
  "link": "https://example.com/launch",
  "platforms": ["linkedin", "x", "bluesky", "instagram"]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | Yes | Core concept, announcement, or article summary |
| `keywords` | string | No | Comma-separated focus keywords or tags |
| `link` | string | No | Canonical link or landing page URL |
| `platforms` | string[] | No | Target platform keys (defaults to all supported platforms) |

#### Response (`200 OK`)
```json
{
  "id": 1,
  "topic": "Launching our next-generation AI marketing analytics suite",
  "keywords": "AI, analytics, growth, SaaS",
  "link": "https://example.com/launch",
  "status": "pending_approval",
  "image_url": "https://image.pollinations.ai/prompt/Modern-minimalist-illustration...",
  "platform_posts": "{\"linkedin\": {\"post\": \"...\", \"hashtags\": [\"ai\"], \"call_to_action\": \"...\"}}",
  "publish_results": "{}",
  "created_at": "2026-09-30T10:00:00.000000",
  "updated_at": "2026-09-30T10:00:00.000000"
}
```

---

### 3. List Posts & History

Retrieves all recorded campaigns sorted by creation date descending.

- **Method**: `GET`
- **Path**: `/api/posts`
- **Auth Required**: If enabled

#### Response (`200 OK`)
```json
[
  {
    "id": 1,
    "topic": "Launching our next-generation AI marketing analytics suite",
    "status": "pending_approval",
    "created_at": "2026-09-30T10:00:00.000000",
    "image_url": "https://image.pollinations.ai/prompt/...",
    "platform_posts": "{...}",
    "publish_results": "{...}"
  }
]
```

---

### 4. Update Post Status (Approval Workflow)

Updates the approval state of a post (`pending_approval`, `approved`, `rejected`).

- **Method**: `PATCH`
- **Path**: `/api/posts/{post_id}/status`
- **Auth Required**: If enabled

#### Request Body
```json
{
  "status": "approved"
}
```

#### Response (`200 OK`)
```json
{
  "id": 1,
  "status": "approved",
  "updated_at": "2026-09-30T10:05:00.000000"
}
```

---

### 5. Publish to Platform

Dispatches an approved post to a specific social platform connector.

- **Method**: `POST`
- **Path**: `/api/posts/{post_id}/publish/{platform}`
- **Auth Required**: If enabled

#### Parameters
- `post_id` (integer): ID of the post
- `platform` (string): Platform key (`bluesky`, `mastodon`, `x`, `linkedin`, `facebook`, `instagram`)

#### Response (`200 OK`)
```json
{
  "id": 1,
  "status": "approved",
  "publish_results": "{\"bluesky\": {\"status\": \"success\", \"url\": \"https://bsky.app/profile/.../post/...\"}}"
}
```

---

### 6. Platform Connection Status

Returns real-time status of configured platform credentials.

- **Method**: `GET`
- **Path**: `/api/posts/meta/platform-status`
- **Auth Required**: If enabled

#### Response (`200 OK`)
```json
{
  "bluesky": true,
  "mastodon": true,
  "x": false,
  "linkedin": false,
  "facebook": false,
  "instagram": false
}
```
