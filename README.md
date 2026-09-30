# DEX ⚡

> **Autonomous AI-Powered Social Media Content Studio & Multi-Platform Dispatch Engine**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

---

## 🌟 Overview

**Post Agent** is a full-stack social media automation engine designed to transform a single campaign brief, article, or topic into highly tailored, platform-compliant posts across **9 major social networks** in seconds.

Each generated variant respects the target platform's strict length constraints, formatting rules, hashtag conventions, tone of voice, and call-to-action dynamics — paired with an automatically generated high-resolution visual asset and a mandatory **Human-in-the-Loop** approval workflow.

```
                                  ┌────────────────────────┐
                                  │   Campaign Brief /     │
                                  │    Topic + Keywords    │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                             ┌──────────────────────────────────┐
                             │    AI Multi-Channel Engine       │
                             │  (Gemini / OpenAI / Custom LLM)  │
                             └────────┬────────────────┬────────┘
                                      │                │
            ┌─────────────────────────┴────┐      ┌────┴────────────────────────┐
            │   Platform-Tailored Posts    │      │  Visual Art Generation Engine│
            │ (9 Channel Optimized Drafts) │      │      (Pollinations AI)       │
            └─────────────────────────┬────┘      └────┬────────────────────────┘
                                      │                │
                                      ▼                ▼
                             ┌──────────────────────────────────┐
                             │     Human-in-the-Loop Staging    │
                             │         & Approval Queue         │
                             └────────────────┬─────────────────┘
                                              │
                                              ▼
                             ┌──────────────────────────────────┐
                             │    Direct Publishing Dispatch    │
                             │  (Bluesky, Mastodon, X, Meta...) │
                             └──────────────────────────────────┘
```

---

## 🚀 Key Features

### 1. 🧠 Intelligent Multi-Platform Voice Calibration
- **One input, 9 bespoke variants**: Generates tailored copy for LinkedIn, Instagram, Facebook, X (Twitter), Bluesky, Mastodon, TikTok, Threads, and YouTube Shorts.
- **Channel-aware formatting**: Respects character ceilings (e.g., 280 for X, 300 for Bluesky, 500 for Mastodon), tone adjustments (conversational, professional, viral), and native hashtag densities.
- **Dynamic Call-to-Action**: Tailors CTAs to platform ergonomics (e.g., *"Link in bio"* on Instagram, *"Drop a reply"* on X, *"Share your thoughts below"* on LinkedIn).

### 2. 🎨 AI Visual Asset Synthesis
- Instant generation of relevant, high-resolution campaign visuals tailored to the topic description.
- Built-in multi-aspect ratio preview (16:9 Landscape for desktop/feeds, 1:1 Square for Instagram/mobile).

### 3. 🛡️ Human-in-the-Loop Governance
- Strict staging pipeline: generated content enters the `pending_approval` state by default.
- Prevents accidental automated broadcasts with explicit manual **Approve** or **Reject** workflows.
- Full revision history and campaign logging.

### 4. 🔌 Native Social Connector Architecture
- **Direct AT Protocol Integration** for real-time Bluesky posting.
- **Federated ActivityPub / Mastodon REST API** integration.
- Extensible connectors for X API v2, LinkedIn REST API, and Meta Graph API (Facebook Pages & Instagram Professional).
- Safe credential containment: all API tokens remain securely isolated in backend environment variables.

---

## 📊 Supported Platforms & Specifications

| Platform | Style & Tone | Length Limit | Visual Target | Publishing Engine |
|---|---|---|---|---|
| **LinkedIn** | Professional, insightful, industry discussion | 3–4 sentences | 16:9 Landscape | LinkedIn REST API |
| **X (Twitter)** | Punchy, concise, thread hook | < 280 chars | 16:9 Landscape | X API v2 (Tweepy) |
| **Bluesky** | Conversational, open-web community tone | < 300 chars | 16:9 Landscape | AT Protocol SDK |
| **Mastodon** | Community-driven, open standards | < 500 chars | 16:9 Landscape | Mastodon REST API |
| **Instagram** | Visual storytelling, emoji accents | 2–3 sentences | 1:1 Square | Meta Graph API |
| **Facebook** | Friendly, community discussion | 2–3 sentences | 16:9 Landscape | Meta Graph API |
| **Threads** | Casual dialogue, interactive question | 1–2 paragraphs | 1:1 Square | Meta Graph API |
| **TikTok** | High-energy video concept & caption | 1–2 sentences | 9:16 Vertical | Concept Generator |
| **YouTube Shorts**| Catchy title (< 60 chars) + hook concept | 1–2 sentences | 9:16 Vertical | Concept Generator |

---

## 🏗️ System Architecture

```
post-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry & CORS middleware
│   │   ├── config.py            # Pydantic Settings & environment validation
│   │   ├── database.py          # SQLAlchemy engine & dynamic schema synchronization
│   │   ├── models.py            # Post database entities & status enum
│   │   ├── schemas.py           # Pydantic request/response validation contracts
│   │   ├── auth.py              # Site access control & header verification
│   │   ├── routers/
│   │   │   └── posts.py         # REST API endpoints (generate, status, publish)
│   │   └── services/
│   │       ├── content_factory.py # Multi-channel prompt & generation pipeline
│   │       ├── llm_client.py     # OpenAI-compatible LLM client factory
│   │       ├── image_gen.py      # Visual prompt synthesis engine
│   │       ├── bluesky.py        # Bluesky AT Protocol connector
│   │       ├── mastodon.py       # Mastodon API connector
│   │       ├── x_platform.py     # X (Twitter) API v2 connector
│   │       ├── linkedin.py       # LinkedIn REST API connector
│   │       └── meta.py           # Facebook & Instagram Graph API connector
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Backend configuration & API keys
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # App layout, shell & routing
│   │   ├── App.css              # Custom styling system & design tokens
│   │   ├── api.js               # Typed client-side API communication layer
│   │   ├── constants.js         # Platform definitions & global constants
│   │   ├── components/
│   │   │   ├── Nav.jsx          # Header navigation bar
│   │   │   └── Icons.jsx        # Optimized SVG social platform iconography
│   │   └── pages/
│   │       ├── Generate.jsx     # Campaign studio & visual showroom
│   │       ├── Approve.jsx      # Multi-post inspection & approval queue
│   │       ├── History.jsx      # Campaign logs & published post records
│   │       └── Accounts.jsx     # Platform connection status & developer guidance
│   ├── package.json             # Frontend package definitions
│   ├── vite.config.js           # Vite build & proxy configuration
│   └── .env                     # Frontend environment configuration
│
└── docs/
    ├── ARCHITECTURE.md          # In-depth architectural blueprint
    ├── API.md                   # REST API endpoint reference
    ├── PLATFORMS.md             # Social network integration specifications
    └── SETUP_GUIDE.md           # Developer onboarding & deployment manual
```

---

## ⚙️ Quick Start Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** & npm

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start FastAPI backend server
uvicorn app.main:app --reload --port 8020
```

The backend server will initialize and listen on `http://localhost:8020`.
API documentation is automatically available at `http://localhost:8020/docs`.

### 2. Frontend Setup

```bash
# In a separate terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start Vite dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 🔑 Environment Configuration

Configure `backend/.env` according to your preferred AI provider and social accounts:

```env
# Database (Defaults to local SQLite)
DATABASE_URL=sqlite:///./social_agent.db

# LLM Provider Configuration
# 1. Google Gemini:
LLM_API_KEY=your_gemini_api_key
LLM_MODEL=gemini-flash-latest
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# 2. OpenAI:
# LLM_API_KEY=sk-...
# LLM_MODEL=gpt-4o-mini
# LLM_BASE_URL=

# 3. Groq:
# LLM_API_KEY=gsk_...
# LLM_MODEL=llama-3.3-70b-versatile
# LLM_BASE_URL=https://api.groq.com/openai/v1

# Security & CORS
CORS_ORIGINS=["http://localhost:5173"]
SITE_PASSWORD=

# Optional: Social Media Publishing Keys
BLUESKY_HANDLE=
BLUESKY_APP_PASSWORD=
MASTODON_INSTANCE_URL=
MASTODON_ACCESS_TOKEN=
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_SECRET=
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_PERSON_URN=
META_PAGE_ACCESS_TOKEN=
META_PAGE_ID=
META_IG_USER_ID=
```

---

## 📖 Documentation Index

- [🎤 Presentation & System Walkthrough Guide](docs/PRESENTATION_GUIDE.md) *(Essential for Demos & Pitches)*
- [Architecture & Design Details](docs/ARCHITECTURE.md)
- [REST API Reference](docs/API.md)
- [Platform Integration Specs](docs/PLATFORMS.md)
- [Setup & Deployment Guide](docs/SETUP_GUIDE.md)

---

## 🔒 Security & Privacy

- **Zero Client-Side Secrets**: All credentials and API tokens live strictly within the server environment.
- **Human Safeguard**: Automated actions never execute direct broadcasts without an explicit human approval trigger.
- **Fail-Safe Connector Isolation**: Missing credentials on any platform will not interrupt or degrade content generation for other channels.
