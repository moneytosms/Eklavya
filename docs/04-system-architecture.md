# 04 · System Architecture

## 1. High-level view
```
┌───────────────────────── Clients (offline-first PWAs) ─────────────────────────┐
│ Candidate PWA          Assessor PWA / Desktop        Admin & Moderator Console │
│ IndexedDB/SQLite-WASM  Service Worker cache          Dashboards, QP manager    │
│ Local queue, on-device STT/TTS fallback, encrypted store (WebCrypto)           │
└───────────────┬───────────────────────────────┬────────────────────────────────┘
                │ HTTPS, resumable uploads (tus)│ Sync (delta, idempotent)
        ┌───────▼───────────────────────────────▼────────┐
        │               API Gateway (FastAPI/NGINX)       │ Auth (OIDC/JWT), RBAC, rate limit
        └───┬──────────┬───────────┬──────────┬──────────┘
            │          │           │          │
   ┌────────▼───┐ ┌────▼─────┐ ┌───▼──────┐ ┌─▼────────────┐
   │ Core svc   │ │ Assess   │ │ Evidence │ │ Credential & │
   │ users,     │ │ engine   │ │ svc      │ │ audit svc    │
   │ QP/NOS,    │ │ adaptive,│ │ upload,  │ │ VC signing,  │
   │ workflow   │ │ scoring  │ │ OCR,     │ │ hash-chain   │
   └─────┬──────┘ └────┬─────┘ │ vision   │ └──────┬───────┘
         │             │       └────┬─────┘        │
   ┌─────▼─────────────▼────────────▼──────────────▼──────┐
   │  AI Service Layer (model-agnostic)                    │
   │  LLM (extraction, mapping, Q-gen, rationale) · RAG    │
   │  STT/TTS (Indic) · Vision · OCR · Embeddings          │
   │  Guardrails: schema-validated JSON, citation check    │
   └─────┬───────────────────────────────┬────────────────┘
         │                               │
 ┌───────▼────────┐  ┌──────────────┐  ┌─▼─────────────┐  ┌───────────┐
 │ PostgreSQL     │  │ pgvector     │  │ Object store  │  │ Redis /   │
 │ (system of     │  │ (NOS/QP      │  │ (S3/MinIO)    │  │ queue     │
 │  record)       │  │  embeddings) │  │ evidence media│  │ (Celery)  │
 └────────────────┘  └──────────────┘  └───────────────┘  └───────────┘
```

## 2. Technology choices
| Layer | Choice | Rationale |
|---|---|---|
| Frontend | React + TypeScript, Vite, PWA (Workbox), Tailwind, i18next | Fast, offline-capable, installable on low-end Android |
| Local storage | IndexedDB (Dexie) + WebCrypto-encrypted blobs | Offline queue, resumable state |
| Backend | Python FastAPI (async), Pydantic, Celery workers | AI ecosystem fit, typed contracts |
| DB | PostgreSQL + pgvector | One store for relational + vector RAG |
| Object storage | MinIO / S3-compatible (India region) | Evidence media; data residency |
| AI | Pluggable provider interface: hosted LLM (e.g., Claude API) for demo; self-hostable open models (Llama/Qwen class) for sovereign deployment | Avoid lock-in; data-residency option |
| Speech | Bhashini / open Whisper-class STT, IndicTTS | Indic language coverage |
| Vision/OCR | VLM for evidence tagging; Tesseract/PaddleOCR for docs | Low-cost doc parsing |
| Auth | OTP login (mobile) for candidates; OIDC for staff; optional DigiLocker/Aadhaar-eKYC | Low-friction + trusted ID |
| Infra | Docker Compose (demo) → Kubernetes on MeghRaj/NIC or Indian cloud region | Gov-friendly deployment |
| Observability | OpenTelemetry, Prometheus/Grafana, Sentry | Ops + AI quality telemetry |

## 3. Key components
1. **QP/NOS Knowledge Base** — ingest official QP/NOS documents (Skill India/NSQF registers, SSC portals) → chunk by NOS/PC → embeddings + structured tables (core/non-core, NSQF level, weights). Versioned.
2. **Experience Mapper** — transcript → structured profile (tasks, tools, materials, duration) → hybrid retrieval (BM25 + vector) over NOS → LLM re-rank with citations → ranked QPs.
3. **Assessment Engine** — item bank (curated + LLM-generated, reviewed), adaptive selector, rubric engine, score aggregator with configurable weights.
4. **Evidence Service** — upload, hash (SHA-256), EXIF/GPS/time checks, perceptual-hash dedupe, OCR, vision tagging to PC, tamper/synthetic-media heuristics.
5. **Assessor Workspace** — evidence viewer, AI rationale, override logging, viva assistant, e-sign.
6. **Sync Service** — change-feed with per-record version vectors; idempotency keys.
7. **Credential Service** — signs W3C Verifiable Credential; public verify endpoint via QR.
8. **Audit Service** — append-only, hash-chained events (each event includes hash of previous).
9. **Analytics & Moderation** — κ/ICC, score distributions, bias dashboards.

## 4. Integration map
| System | Purpose | Status |
|---|---|---|
| NSQF / National Qualifications Register (NQR), SSC QP/NOS repositories | Authoritative QP/NOS source | Ingest (bulk); API **[Verify availability]** |
| Skill India Digital Hub (SIDH) / SDMS | Candidate & certification records | Proposed API integration |
| DigiLocker | Store/verify credentials, fetch documents | Proposed (OAuth + Issuer API) |
| Aadhaar eKYC / APAAR-style IDs | Identity (optional, consented) | Proposed |
| Bhashini | Indic STT/TTS/translation | Integrated/pluggable |
| SMS/WhatsApp gateway | OTP, attestation links, reminders | Pluggable |
| PMKVY/RPL scheme MIS | Batch & payment status | Future |
| Employer verification | OTP attestation | In MVP |

## 5. Deployment topology
- **Cloud/central**: API, DB, object store, AI services (or private AI endpoint).
- **Edge (optional) "Assessment Kiosk"**: laptop/mini-server at training centre running core services + local models for fully air-gapped sessions; syncs to central.
- **Mobile**: PWA with local cache; background sync via Service Worker / Periodic Sync.

## 6. Scalability & cost
Stateless API (horizontal scale), async AI jobs via queue, media to object store with lifecycle policies, per-candidate AI cost bounded by caching QP/NOS retrieval and using small models for routine steps; large model only for mapping/rationale. Target: < ₹10–15 AI cost per candidate **[Estimate]**.
