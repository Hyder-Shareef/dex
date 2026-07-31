# Post Agent

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=flat&logo=reactrouter&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![OpenAI SDK](https://img.shields.io/badge/OpenAI_SDK-412991?style=flat&logo=openai&logoColor=white)
![Bluesky](https://img.shields.io/badge/Bluesky-0285FF?style=flat&logo=bluesky&logoColor=white)
![Mastodon](https://img.shields.io/badge/Mastodon-6364FF?style=flat&logo=mastodon&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat&logo=railway&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white)

Post Agent is an AI content studio for social media. You describe a topic once, and it drafts a tailored post for every platform you pick — LinkedIn, X, Bluesky, Mastodon, Facebook, Instagram, Threads, TikTok, YouTube Shorts — complete with hashtags, a call to action, and a generated visual. Every draft goes through a human approval step before it can be published anywhere.

## Why it exists

Writing the same idea nine different ways for nine different platforms is repetitive, and each platform has its own tone, length, and hashtag conventions. Post Agent automates that adaptation while keeping a human in control of what actually goes out — nothing is published without an explicit approval and an explicit publish click.

## Features

### Content generation
- One topic in, one tailored draft out per platform, each respecting that platform's real conventions (length limits, tone, hashtag style, CTA phrasing).
- Structured JSON generation via an LLM (OpenAI-compatible — the deployed instance uses Google Gemini, swappable to OpenAI/Groq by changing one environment variable).
- Automatic visual generation for every draft (via Pollinations.ai, no API key required).

### Approval workflow
- Every generated draft starts as `pending_approval` — nothing is publishable until a human explicitly approves or rejects it.
- Rejected drafts are excluded from publishing entirely.

### Multi-platform publishing
- Real, working publishers for **Bluesky** and **Mastodon** — both free, both active with no external approval process.
- Publishers for **X, LinkedIn, Facebook, and Instagram** are fully implemented but require credentials from an app approved by that platform (see [Accounts](#accounts) below) — until then, they fail gracefully with a clear message instead of blocking the rest of the app.
- Per-platform publish status and a direct link to the live post once published.

### Accounts
- A status page shows which platforms are actively connected, with a direct link to where to get each credential.
- Credentials live only in backend environment variables — never in the browser, never in the database, never committed to the repository.

## How it works

```
Topic + keywords + link ──► AI drafts one post per selected platform (structured JSON)
                                            │
                              generated visual (Pollinations.ai)
                                            │
                                   human approval (Approve queue)
                                            │
                              publish per platform (Bluesky, Mastodon live;
                              X/LinkedIn/Facebook/Instagram once credentials exist)
```

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | SQLite (local), PostgreSQL (production) |
| AI | OpenAI-compatible SDK (Google Gemini in production, swappable for OpenAI/Groq) |
| Image generation | Pollinations.ai (free, no API key) |
| Publishing | AT Protocol (Bluesky), Mastodon REST API, X API v2 (tweepy), LinkedIn REST API, Meta Graph API |
| Frontend | React, React Router, Vite, JavaScript, CSS |
| Hosting | Railway (backend + PostgreSQL), Vercel (frontend) |

## Run locally

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate   # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8020
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Deployment

Same pattern as any FastAPI + React project: deploy `backend/` to Railway (with a PostgreSQL add-on and `DATABASE_URL` wired automatically), deploy `frontend/` to Vercel with `VITE_API_URL` pointing at the Railway backend URL, and update `CORS_ORIGINS` on the backend once the Vercel URL is known.

**Deliberate choice on credentials**: publishing credentials (Bluesky, Mastodon, etc.) are kept in the *local* `.env` only, never set on the public Railway deployment. This means the live public demo shows the full generation and approval flow working for real, while the "Publish" button stays safely inactive for anonymous visitors — only the project owner, running the backend locally with their own credentials, can actually publish to real accounts.

## What Post Agent will not do

- Will not publish anything without an explicit human approval and an explicit publish action.
- Will not fabricate platform access — a platform without valid credentials fails with a clear message rather than pretending to succeed.
- Does not generate actual video — video platforms (TikTok, YouTube Shorts) get a text caption and a suggested video concept, not a rendered video file.
