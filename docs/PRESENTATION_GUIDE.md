# DEX // Complete Project Presentation & System Walkthrough Guide ⚡

> **Official Step-by-Step Technical & Architectural Walkthrough for Hackathon Demonstrations, Pitches, and System Evaluations**

---

## 🎯 Executive Pitch (30-Second Elevator Pitch)

> *"Writing social media content across 9 platforms is tedious, repetitive, and inconsistent. Each platform demands unique character limits, tones, and hashtag conventions. **DEX** is an autonomous AI-powered content studio and dispatch engine that turns a single campaign brief into 9 platform-perfect posts and tailored visual artwork in seconds — while enforcing a strict **Human-in-the-Loop** approval workflow so that nothing ever gets published without explicit human authorization."*

---

## 🏛️ End-to-End System Architecture

```
                                  ┌───────────────────────────┐
                                  │   Step 1: Campaign Input  │
                                  │   Topic + Keywords + URL  │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │   Step 2: AI Core Engine  │
                                  │   Structured JSON Parser  │
                                  │ (Gemini / OpenAI / Local) │
                                  └──────┬─────────────┬──────┘
                                         │             │
                 ┌───────────────────────┴─┐         ┌─┴───────────────────────┐
                 │ 9 Channel Post Variants │         │ AI Visual Concept Prompt│
                 │   (Platform Tailored)   │         │ (Pollinations AI Engine)│
                 └──────────────┬──────────┘         └─────────┬───────────────┘
                                │                              │
                                └──────────────┬───────────────┘
                                               │
                                               ▼
                                  ┌───────────────────────────┐
                                  │ Step 3: Showroom & Canvas │
                                  │ Multi-Aspect Ratio Preview│
                                  └────────────┬──────────────┘
                                               │
                                               ▼
                                  ┌───────────────────────────┐
                                  │ Step 4: Staging Queue     │
                                  │   status: pending_review  │
                                  └────────────┬──────────────┘
                                               │
                                  ┌────────────┴────────────┐
                                  ▼                         ▼
                           [ APPROVE ]                 [ REJECT ]
                                  │                         │
                                  ▼                         ▼
                      ┌───────────────────────┐       ┌───────────┐
                      │ Unlocked for Dispatch │       │ Dismissed │
                      └───────────┬───────────┘       └───────────┘
                                  │
                                  ▼
                      ┌───────────────────────┐
                      │ Step 5: Direct Post   │
                      │  Social API Connectors│
                      │ (Bluesky, Mastodon...)│
                      └───────────────────────┘
```

---

## 🔍 Step-by-Step Workflow & How Each Module Works

### Step 1: Campaign Brief & Studio Ingestion
- **Where**: Frontend `/` (Compose Panel)
- **User Action**: The operator inputs:
  1. `Topic / Story Focus`: The core message, product announcement, or story (e.g. *"Launching our AI engine"*).
  2. `Keywords & Hashtags`: Optional focus terms (e.g. *"AI, productivity, automation"*).
  3. `Target Link`: Optional URL destination to embed.
  4. `Platform Selector`: Checkbox matrix selecting any of the 9 target channels.
- **Under the Hood**:
  - The frontend validates form inputs.
  - Sends a `POST` request to `/api/posts/generate` with a JSON payload containing `topic`, `keywords`, `link`, and `platforms`.

---

### Step 2: Intelligent Multi-Platform Voice Calibration
- **Where**: Backend `backend/app/services/content_factory.py`
- **How it Works**:
  - The system utilizes a specialized **System Prompt** enforcing platform-specific editorial rules and a strict JSON schema.
  - **OpenAI-Compatible Orchestration**: Connects to Google Gemini (`gemini-flash-latest`), OpenAI, or Groq via standard client protocol.
  - **Local Fallback Engine**: If no API key is configured, an intelligent deterministic mock generator dynamically generates tailored copy, ensuring the application is 100% testable out-of-the-box.

#### The 9 Platform Optimization Rules:
| Platform | Tone of Voice | Character Bounds | Hashtag Density | Call to Action |
|---|---|---|---|---|
| **LinkedIn** | Professional, analytical, industry leadership | 3–4 sentences | 3–4 business tags | Prompts peer discussion & comments |
| **X (Twitter)** | Punchy, viral hook, high-velocity | < 280 characters | 1–2 focused tags | "Drop your take below 🧵" |
| **Bluesky** | Conversational, open-web, witty | < 300 characters | 1–2 tags | Open community question |
| **Mastodon** | Community-driven, technical, accessible | < 500 characters | 3–5 CamelCase tags | Encourages boosts and replies |
| **Instagram** | Visual storytelling, inspirational, emoji accents | 2–3 sentences | 5–8 discovery tags | "Link in bio" / "Swipe to explore" |
| **Facebook** | Friendly, relatable, community discussion | 2–3 sentences | 2–3 community tags | Invites likes and shares |
| **Threads** | Casual question, conversational hook | 1–2 paragraphs | 1–2 tags | Sparks reply chains |
| **TikTok** | High-energy, trend-conscious script | 1–2 sentences + B-roll | Viral tags (`#fyp`) | "Follow for daily insights" |
| **YouTube Shorts**| Curiosity hook, fast retention | Title (< 60 chars) + script | `#shorts` + 2 tags | "Subscribe for more short deep dives"|

---

### Step 3: AI Visual Art Generation Pipeline
- **Where**: Backend `backend/app/services/image_gen.py`
- **How it Works**:
  1. The LLM generates a dedicated `image_description` tailored specifically to the tone and aesthetic of the campaign.
  2. The backend cleans and URL-encodes this prompt into a zero-latency CDN request via Pollinations.ai.
  3. No API key or heavy GPU cluster is required on the user's machine; high-resolution visuals load instantly.
  4. The frontend canvas provides dynamic **16:9 Landscape** (for LinkedIn/X/Web) and **1:1 Square** (for Instagram/mobile) aspect ratio toggles.

---

### Step 4: Human-in-the-Loop Governance & Staging
- **Where**: Frontend `/approve` & Backend `/api/posts/{id}/status`
- **The Philosophy**:
  - Pure autonomous posting without human oversight is dangerous for brand reputation.
  - Every draft generated by DEX begins with status: `pending_approval`.
- **The Workflow**:
  1. The operator opens the **Approve Queue**.
  2. Each draft displays the generated image and tabbed variations across all selected platforms.
  3. The reviewer can:
     - **Approve**: Transitions status to `approved`, immediately unlocking the publish dispatch.
     - **Reject**: Transitions status to `rejected`, locking the post from any outbound broadcast.

---

### Step 5: Multi-Platform Publishing Engine
- **Where**: Backend `backend/app/services/` & `/api/posts/{id}/publish/{platform}`
- **How it Works**:
  - Each social network has an isolated connector module:
    - **Bluesky** (`bluesky.py`): Authentic AT Protocol session creation (`com.atproto.server.createSession`) and record creation (`app.bsky.feed.post`).
    - **Mastodon** (`mastodon.py`): ActivityPub REST API status creation (`POST /api/v1/statuses`).
    - **X / Twitter** (`x_platform.py`): X API v2 tweet creation via Tweepy OAuth 1.0a / 2.0.
    - **LinkedIn** (`linkedin.py`): User-generated content endpoint (`/v2/ugcPosts`).
    - **Meta** (`meta.py`): Facebook Page feed publish & Instagram Professional Graph container publish.
  - **Fault Isolation**: If one platform fails (e.g. invalid credentials or network timeout), the error is isolated to that specific platform's result object without failing the campaign.

---

### Step 6: Security & Zero Client Secret Leakage
- **No Client Secrets**: API keys (Gemini, Bluesky, Twitter, etc.) are strictly kept in the backend `.env` and never transmitted to the browser.
- **Site Gate**: Optional header-based protection (`X-Site-Password`) gates internal corporate installations.
- **Indexed Schema Sync**: Dynamic database table and column auto-migration (`sync_schema()`) supports SQLite locally and PostgreSQL in production without manual migration scripts.

---

## 💻 Tech Stack Summary

| Layer | Technologies Used | Key Responsibilities |
|---|---|---|
| **Frontend** | React 18, React Router v6, Vite, Vanilla CSS | Interactive studio canvas, aspect ratio controls, approval queue |
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic v2 | Async REST API, input validation, connector isolation |
| **Database** | SQLAlchemy 2.0, SQLite (Local), PostgreSQL (Production) | Dynamic schema synchronization, campaign persistence |
| **AI Layer** | OpenAI SDK, Google Gemini (`gemini-flash-latest`), Groq | Multi-platform structured JSON post calibration |
| **Imaging** | Pollinations AI Engine | On-the-fly zero-configuration campaign artwork |
| **Publishing**| AT Protocol (Bluesky), Mastodon REST, Tweepy, Meta Graph | Real-time social broadcast and error containment |

---

## 🎤 Presentation & Demo Script (Follow this during the Presentation)

### Phase 1: The Problem (1 minute)
- *"Today, social teams spend hours adapting one campaign into multiple formats. LinkedIn needs professional depth, Twitter needs under 280 characters, Instagram needs visual captions, and TikTok needs video hooks."*
- *"Companies either do this manually (slow) or use naive bots that post the same plain text everywhere (looks spammy and performs poorly)."*

### Phase 2: The Solution & Live Demo (3 minutes)
1. **Show the UI**: Open [http://localhost:5173](http://localhost:5173). Highlight the sleek, cyberpunk **DEX** aesthetic.
2. **Enter a Campaign Brief**:
   - Type a topic: *"Announcing our revolutionary AI productivity agent"*.
   - Add keywords: *"AI, future of work, productivity"*.
   - Keep all platforms selected.
   - Click **Generate Content**.
3. **Show the Output Canvas**:
   - Highlight how LinkedIn is formatted with professional prose and an insightful discussion prompt.
   - Point out that X is strictly under 280 characters with a thread hook.
   - Show TikTok with a 30-second video concept.
   - Switch the generated visual between **16:9 Landscape** and **1:1 Square**.
4. **Demonstrate Human-in-the-Loop**:
   - Navigate to **Approve**.
   - Show that the post is in `pending_approval` state.
   - Explain why this prevents hallucinations or rogue automated posts.
   - Click **Approve**.
5. **Show History & Accounts**:
   - Navigate to **History** to show approved posts ready for publishing.
   - Navigate to **Accounts** to demonstrate real-time connector status.

---

## ❓ Common Judge Questions & Winning Answers

**Q1: How do you prevent hallucinations or made-up statistics in the posts?**  
*A: Our system prompt strictly constrains the LLM to only state facts and claims implied by the operator's topic. Additionally, because every draft must pass through the mandatory Human-in-the-Loop Approve Queue, no post can go live without human sign-off.*

**Q2: What happens if an API key expires or a social network rate-limits?**  
*A: Our connector architecture isolates every channel. A failure on X or LinkedIn is captured gracefully in the database with a clear error detail, leaving the rest of the campaign intact.*

**Q3: Can we swap the underlying AI model?**  
*A: Yes. The backend uses the universal OpenAI client standard. By changing `LLM_MODEL` and `LLM_BASE_URL` in `.env`, you can swap between Google Gemini, OpenAI GPT-4o, Groq LLaMA-3.3, or self-hosted Ollama models without modifying code.*
