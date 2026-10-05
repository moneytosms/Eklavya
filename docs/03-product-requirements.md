# 03 · Product Requirements (PRD)

## 1. Personas
| Persona | Description | Key needs |
|---|---|---|
| **Ramesh – Candidate** | 38, AC technician, 8 yrs experience, Class 8, Hindi/regional, budget Android, patchy network | Speak instead of type, quick, no lost data, understandable result |
| **Priya – Assessor** | SSC-accredited, assesses 10–15 candidates/week, travels | Evidence at a glance, consistent rubric, less paperwork, offline field use |
| **Lead Assessor / Moderator** | Quality owner at assessment body | Spot-check, agreement metrics, appeals |
| **Training Partner / Coordinator** | Mobilises batches | Batch scheduling, status, bridge-course allocation |
| **SSC / NSDC Admin** | Governs QPs and quality | QP/NOS management, analytics, audit |
| **Employer / Verifier** | Attests experience, verifies credentials | Simple OTP attestation, QR verification |

## 2. Functional requirements (MoSCoW)
### Candidate
- **M** F1 Register (mobile OTP; Aadhaar/DigiLocker optional [proposed]), consent capture
- **M** F2 Language choice; voice-first experience declaration (speech-to-text) with text fallback
- **M** F3 AI QP suggestions with matched NOS and confidence; manual override
- **M** F4 Evidence upload/capture (image, video, audio, PDF) with timestamp & geotag, works offline
- **M** F5 Adaptive assessment with audio prompts, image-based and scenario questions
- **S** F6 Employer/peer attestation by OTP link/SMS
- **M** F7 Results: competency profile, gaps, bridge-course suggestions, QR credential
- **C** F8 Appeal/re-assessment request

### Assessor
- **M** A1 Assigned-candidate queue (offline cache)
- **M** A2 Review workspace: experience summary, evidence per NOS, AI rationale & confidence, flags
- **M** A3 Practical rubric scoring (NOS-derived checklist), accept/override AI suggestions with mandatory reason on override
- **M** A4 Viva assistant: suggested follow-ups from evidence gaps
- **M** A5 Final decision & e-signature; AI cannot finalise
- **S** A6 Calibration view: own scores vs. peer/moderator benchmarks

### Admin / Moderator
- **M** M1 QP/NOS repository (ingest, version, weightings, thresholds)
- **S** M2 Moderation sampling, inter-rater agreement (Cohen's κ / ICC), drift alerts
- **S** M3 Dashboards: throughput, pass rates by QP/region/assessor, time-to-certify, bias metrics
- **M** M4 Immutable audit log, export

### Platform
- **M** P1 Offline-first capture + background sync with conflict resolution
- **M** P2 Role-based access, per-candidate consent, data minimisation
- **S** P3 Multilingual UI (Hindi, English + 2–3 regional at demo; extensible via i18n/Bhashini)
- **S** P4 Verifiable credential issuance/verification endpoint

## 3. Non-functional requirements
| Area | Target |
|---|---|
| Performance | Candidate app first load < 3 s on 3G (PWA, < 300 KB critical path); question render < 300 ms offline |
| Offline | Full assessment + evidence capture for ≥ 72 h without network; resumable uploads |
| Devices | Android 8+ low-end (2 GB RAM), Chrome PWA; desktop for assessor |
| Accessibility | WCAG 2.1 AA, audio prompts, large touch targets, high contrast |
| Security | TLS 1.3, AES-256 at rest, encrypted local store, RBAC, signed audit chain |
| Privacy | DPDP Act 2023 aligned: consent, purpose limitation, erasure, breach process |
| Reliability | 99.5% sync success; idempotent APIs |
| Explainability | 100% of AI scores carry rationale + NOS/PC citation |
| Fairness | Monitor score parity across language, gender, region; flag drift |

## 4. Sample user stories & acceptance criteria
- *As Ramesh, I speak about my work in Hindi so the system understands my skills.* **AC:** transcript shown for edit; ≥ 5 structured tasks extracted; works offline using queued transcription [fallback: text].
- *As Priya, I see why the AI scored an item so I can trust or override it.* **AC:** each item shows rationale, cited NOS/PC, confidence; override requires reason; both stored.
- *As a moderator, I see where assessors disagree.* **AC:** per-NOS agreement metric and flagged outliers.
- *As Ramesh, I lose network mid-test and nothing is lost.* **AC:** answers persisted locally per question; resume to same item; sync on reconnect without duplicates.

## 5. Assessment & scoring rules (configurable per QP)
- Theory/viva + practical + evidence score per NOS; NOS score = weighted blend (e.g., theory 25 / practical 50 / evidence 25) **[Assumption – configurable]**.
- QP total: core NOS 70% + non-core NOS 30%. Pass thresholds per SSC **[Verify]**.
- Outcome per NOS: Competent / Not-yet-competent; QP outcome: Certified / Bridge training required / Re-assess.
- Level recommendation: highest NSQF level QP for which thresholds are met.
