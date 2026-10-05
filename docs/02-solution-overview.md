# 02 · Solution Overview

## Vision
Turn *experience into recognized skill* — consistently, fairly, in the candidate's language, and without needing a network.

## Core idea in five steps
```
 1 DECLARE      2 EVIDENCE      3 ASSESS            4 VERIFY            5 RECOGNIZE
 Voice/text  →  Photos, video,  → Adaptive Q&A +  → Human assessor   → NSQF-level profile,
 experience     docs, employer    practical task     reviews AI         gap report, bridge
 + AI→QP map    attestation       rubric pre-score   pre-score, signs   plan, digital cert
```

### 1. Declare (Experience intake)
Candidate speaks/types: *"8 saal se AC repair karta hoon, gas charging, compressor badalna..."* (any supported language). Speech-to-text → LLM extracts **tasks, tools, materials, years, context** into a structured experience profile. The system **suggests ranked candidate QPs** (e.g., *Field Technician – Air Conditioner*, NSQF L4) with confidence and matched NOS; candidate/assessor confirms.

### 2. Evidence
Capture documents (employer letters, invoices, certificates), photos/videos of work, GPS/time-stamped captures, and **third-party attestations** (employer/peer OTP-confirmed). OCR + vision models extract and tag evidence to NOS performance criteria (e.g., photo of brazed joint → NOS "joining refrigerant lines"). Everything works offline.

### 3. Assess (Adaptive)
- **Adaptive question engine**: starts at mid-difficulty per NOS, adapts up/down (IRT-inspired); voice/image/MCQ/scenario formats; low-literacy mode with audio prompts.
- **Practical assessment**: assessor (or video submission) evaluates a task against a **NOS-derived rubric checklist** (safety, tool use, procedure, finish, time). AI pre-fills rubric items from video/photos with evidence timestamps — as *suggestions*.
- **Viva support**: AI proposes probing follow-ups based on evidence gaps and inconsistencies.

### 4. Verify (Human-in-the-loop)
Assessor dashboard shows: AI-extracted profile, evidence per NOS, auto-scored items with rationale, confidence & flags (inconsistency, possible copied/synthetic media, low confidence). Assessor accepts/overrides each item (override reason mandatory), conducts viva, and **e-signs** final result. Every action is hash-chained in an audit log. Moderation sampling by a lead assessor measures inter-assessor agreement.

### 5. Recognize
Output: **NSQF-aligned Competency Profile** (per NOS: Competent / Gap with scores), overall level recommendation using the 70/30 core/non-core weighting [config per QP], **gap analysis → bridge-course recommendations**, and a **verifiable credential** (QR + signed JSON-LD/W3C VC), shareable to DigiLocker/Skill India Digital **[proposed integration]**.

## Differentiators
| Differentiator | Why it matters |
|---|---|
| **NOS-grounded RAG** (QP/NOS corpus) | No hallucinated standards; every output cites NOS/PC IDs |
| **Explainable pre-scoring** | Assessor trust; legally defensible |
| **Assessor calibration & moderation analytics** | Directly attacks inconsistency (core PS ask) |
| **Voice-first Indic UX** | Reaches low-literacy workers |
| **True offline-first (PWA + local queue + on-device fallbacks)** | Works in low connectivity |
| **Evidence integrity** (hashes, geo/time stamps, deepfake/duplicate checks) | Fraud resistance |
| **Pathway, not just a verdict** | Gap → bridge course → re-assessment loop |
| **Governance by design** | AI cannot certify; consent, audit, appeals |

## Scope boundaries
In scope: intake, mapping, evidence, adaptive assessment, rubric scoring, assessor workflow, profile & credential, offline sync, analytics.
Out of scope (future): payment/scheme disbursal, full LMS for bridge courses, employer job-matching marketplace.
