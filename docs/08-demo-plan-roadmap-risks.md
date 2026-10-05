# 08 · Demo Plan, Roadmap & Risks

## 1. Hackathon demo MVP (what to build next)
**Goal:** a convincing end-to-end vertical slice in one sitting; real where it matters (mapping, adaptive Q, assessor review, offline), mocked where it doesn't (ID, scheme APIs).

### Demo scope
| Area | Demo implementation |
|---|---|
| QP/NOS corpus | 3–4 QPs hand-curated from public NSQF sources (e.g., AC technician, electrician, tailor/sewing machine operator, plumber) with NOS/PC and core/non-core flags |
| Candidate PWA | Language toggle (EN/HI), voice declaration (Web Speech API; text fallback), AI QP suggestions with citations |
| Evidence | Photo/doc upload with hash + geo/time stamp; AI tags to PCs (VLM) |
| Adaptive test | ~10 items/NOS item bank, client-side adaptive selector, audio prompts via browser TTS |
| Offline | Airplane-mode demo: complete test + capture evidence; reconnect → sync with status chips |
| Assessor console | Review packet, AI rationale + confidence, accept/override with reason, viva suggestions, e-sign final decision |
| Output | Competency profile (per-NOS radar/bars), gap + bridge plan, QR credential + public verify page |
| Admin | Mini dashboard: assessor agreement, score distributions, audit log viewer |

### Suggested stack for speed
React + Vite + TS PWA · FastAPI + SQLite/Postgres · pgvector (or FAISS) · Claude/other LLM behind a provider interface · browser STT/TTS · Docker Compose · seed data + scripted personas.

### 6–8 minute demo script
1. **Problem (30 s):** Ramesh, 8 yrs AC repair, no certificate.
2. **Declare (60 s):** speaks in Hindi → structured skills → QP suggestions with NOS citations.
3. **Evidence (60 s):** snaps photo of work → auto-tagged to NOS PC; employer OTP attestation.
4. **Offline (60 s):** switch to airplane mode; take adaptive test; show "Saved on phone".
5. **Sync (30 s):** back online → synced.
6. **Assessor (120 s):** AI pre-score with rationale; flag on inconsistent claim; override one item with reason; viva follow-up; e-sign.
7. **Result (45 s):** NSQF profile, gap → bridge plan, QR credential verified live.
8. **Governance/analytics (45 s):** audit chain, "AI cannot certify" enforcement, inter-assessor agreement.

### Demo risk mitigation
Pre-seeded fallback responses if API/LLM down; recorded backup video; deterministic seeds; cached embeddings; test on a real low-end phone; offline mode rehearsed.

## 2. Roadmap
| Phase | Timeline | Deliverables |
|---|---|---|
| 0. Hackathon MVP | Day 0–1 | Vertical slice above |
| 1. Pilot-ready | 0–3 months | 10–15 QPs from 2 SSCs, 3 languages, SME-reviewed item banks, assessor field app, security hardening, DPDP review |
| 2. Pilot | 3–6 months | 2 districts, ~1,000 candidates; measure time-to-certify, assessor agreement, candidate NPS; calibrate AI vs experts |
| 3. Integration | 6–12 months | SIDH/SDMS, DigiLocker, NQR sync, Bhashini, SSC credential issuance |
| 4. Scale | 12–24 months | 100+ QPs, kiosks, on-prem models, employer verification network, bridge-course LMS linkage |

## 3. Success metrics
- Time to certification ↓ ≥ 50%; assessor capacity (candidates/assessor/week) ↑ ≥ 2×
- Inter-assessor agreement κ ≥ 0.75
- QP mapping top-3 accuracy ≥ 85%; citation validity 100%
- Offline sync success ≥ 99%; candidate completion rate ≥ 90%
- Candidate satisfaction ≥ 4/5; zero AI-only certifications (invariant)

## 4. Risks & mitigations
| Risk | Mitigation |
|---|---|
| LLM hallucination of standards | RAG with citation enforcement; reject uncited output |
| STT errors on dialects | Editable transcript; assessor oral fallback; WER monitoring by language |
| Official QP/NOS data access | Ingest public docs; seek SSC/NSDC data-sharing MoU |
| Assessor resistance | Position as time-saver; override always available; training |
| Bias against low-literacy/regional users | Voice-first, parity dashboards, human review |
| Fraud / impersonation | Hash/geo/time evidence, dedupe, attestation, optional liveness, audit |
| Connectivity/hardware limits | PWA, small payloads, local edge kiosk |
| Regulatory acceptance | Human final authority; audit; align with SSC/NCVET guidelines |
| AI cost | Tiered models, caching, self-hosted option |

## 5. Team & task split (suggested for a 6-person SIH team)
Frontend candidate PWA · Assessor/Admin UI · Backend/API & sync · AI/RAG & prompts · Data (QP/NOS curation, item bank) · Design/PPT/demo video.
