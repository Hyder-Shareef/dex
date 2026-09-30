# Architecture & Technical Design

> **Post Agent Architecture Specification**

---

## 1. System Topology

Post Agent is structured as a decoupled client-server architecture with an asynchronous backend API layer, an AI transformation engine, dynamic schema synchronization, and an interactive React-based campaign workstation.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          User Web Workstation                          │
│                                                                        │
│   ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────┐   │
│   │   Campaign Studio   │  │   Approval Queue    │  │ Platform Hub │   │
│   │   (Generate.jsx)    │  │    (Approve.jsx)    │  │(Accounts.jsx)│   │
│   └──────────┬──────────┘  └──────────┬──────────┘  └──────┬───────┘   │
└──────────────┼────────────────────────┼────────────────────┼───────────┘
               │                        │                    │
               ▼                        ▼                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        API Client Layer (api.js)                       │
│           • Custom Auth Headers  • JSON Payload Serialization          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST (JSON)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend Framework                        │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │             CORS Middleware & Authentication Guard             │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
│                                   │                                    │
│   ┌───────────────────────────────▼────────────────────────────────┐   │
│   │                 Posts Router (`app/routers/posts.py`)          │   │
│   │  • /api/posts/generate     • /api/posts/{id}/status            │   │
│   │  • /api/posts              • /api/posts/{id}/publish/{platform}│   │
│   └───────┬───────────────────────────────┬────────────────────────┘   │
│           │                               │                            │
│           ▼                               ▼                            │
│   ┌─────────────────────────┐   ┌──────────────────────────────────┐   │
│   │ Content Factory Engine  │   │  Social Media Connectors         │   │
│   │ • Multi-channel prompt  │   │  • Bluesky (AT Protocol)         │   │
│   │ • Structured JSON parse │   │  • Mastodon (ActivityPub/REST)   │   │
│   │ • Visual prompt synth   │   │  • X / LinkedIn / Meta APIs      │   │
│   └───────────┬─────────────┘   └──────────────────┬───────────────┘   │
│               │                                    │                   │
│               ▼                                    ▼                   │
│   ┌─────────────────────────┐   ┌──────────────────────────────────┐   │
│   │  LLM Client Adapter     │   │     SQLAlchemy ORM + SQLite /    │   │
│   │  (OpenAI/Gemini/Groq)   │   │     PostgreSQL Schema Sync       │   │
│   └─────────────────────────┘   └──────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Subsystems

### 2.1 Content Factory & Voice Calibration Engine
The Content Factory ([content_factory.py](file:///c:/Users/share/OneDrive/Desktop/hackathon2/post-agent/backend/app/services/content_factory.py)) transforms campaign requirements into platform-specific copy by enforcing precise structural rules:

- **JSON Schema Enforcement**: Strict JSON contract parsing ensures consistent output formatting across all requested channels.
- **Rule Matrix**: Injects channel-specific stylistic rules (length bounds, emoji density, engagement triggers, and hashtags).
- **Graceful Fallback**: Automatically activates a local deterministic generator if no external API key is set, ensuring seamless testing.

### 2.2 Visual Art Synthesis Engine
The visual pipeline ([image_gen.py](file:///c:/Users/share/OneDrive/Desktop/hackathon2/post-agent/backend/app/services/image_gen.py)) processes the generated `image_description` into an optimized visual asset:
- Converts descriptive aesthetic concepts into sanitized image generation prompts.
- Delivers real-time artwork generation without requiring external API tokens or local GPU overhead.

### 2.3 State Machine & Approval Lifecycle
Every campaign item moves through an explicit state machine:

```
[ POST CREATION ] ──► (pending_approval)
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
        (approved)                        (rejected)
             │                                 │
             ▼                                 ▼
   [ Available for Publish ]              [ Archival ]
```

1. **`pending_approval`**: Initial generated state. Content is held in staging and cannot be dispatched to social platforms.
2. **`approved`**: The operator has reviewed and validated the copy and visual assets. The post is unlocked for single-click multi-channel publishing.
3. **`rejected`**: The post is dismissed and locked against accidental broadcast.

### 2.4 Database & Auto-Migration Layer
The database layer ([database.py](file:///c:/Users/share/OneDrive/Desktop/hackathon2/post-agent/backend/app/database.py)) utilizes SQLAlchemy 2.0:
- Supports zero-configuration local SQLite (`social_agent.db`) and production-grade PostgreSQL.
- Includes a dynamic schema synchronizer (`sync_schema()`) that introspects existing tables upon startup and dynamically executes column additions to prevent migration desyncs.

---

## 3. Security & Isolation Model

- **Zero Client Credential Exposure**: Client applications never receive, store, or transmit third-party API tokens.
- **Header-Based Site Gate**: Supports optional `X-Site-Password` authentication header validation for restricted internal deployments.
- **Isolated Failures**: If one social platform connector fails due to network or authentication errors, other channel publications remain entirely unaffected.
