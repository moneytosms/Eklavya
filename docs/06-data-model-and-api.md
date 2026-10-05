# 06 · Data Model & API

## 1. Entity overview
```
User(role) ─┬─ Candidate ── ExperienceProfile
            │        └──── Assessment ──┬─ AssessmentNOS ── ItemResponse
            └─ Assessor ───────────────┤          └──── RubricScore
                                       ├─ Evidence ── EvidenceTag(NOS/PC)
                                       ├─ AISuggestion
                                       ├─ Decision (human, e-signed)
                                       └─ Credential
QP ── NOS ── PerformanceCriterion ;  Item ── ItemPC ; AuditEvent (hash chain) ; Consent
```

## 2. Core tables (PostgreSQL, abbreviated)
```sql
qp(id, code, title, sector, nsqf_level, version, status)
nos(id, qp_id, code, title, is_core, weight)
performance_criterion(id, nos_id, code, text, is_critical)
user_account(id, role, name, phone_hash, lang, created_at)
candidate(id, user_id, dob, gender, district, consent_id)
experience_profile(id, candidate_id, transcript, lang, structured jsonb, created_at)
assessment(id, candidate_id, qp_id, assessor_id, mode, status, started_at, synced_at)
item(id, nos_id, pc_id, type, difficulty, lang_variants jsonb, key jsonb, status)
item_response(id, assessment_id, item_id, response jsonb, score, graded_by, latency_ms, client_ts)
evidence(id, assessment_id, kind, uri, sha256, captured_at, geo, device_id, meta jsonb)
evidence_tag(id, evidence_id, pc_id, confidence, source)       -- source: ai|assessor
rubric_score(id, assessment_id, pc_id, ai_score, ai_conf, ai_rationale, final_score, override_reason, scored_by)
ai_suggestion(id, assessment_id, type, payload jsonb, model, prompt_version, confidence, created_at)
decision(id, assessment_id, assessor_id, outcome, nos_results jsonb, signature, signed_at)
credential(id, decision_id, vc jsonb, status, issued_at)
audit_event(id, actor, action, entity, payload jsonb, prev_hash, hash, ts)
consent(id, candidate_id, purposes jsonb, version, given_at, withdrawn_at)
```
Embeddings: `nos_chunk(id, nos_id, pc_id, text, embedding vector(768))` with HNSW index.

## 3. REST API (v1) — key endpoints
| Method | Path | Description | Actor |
|---|---|---|---|
| POST | `/auth/otp/request`, `/auth/otp/verify` | Mobile OTP login | Candidate |
| POST | `/candidates/{id}/consent` | Record consent | Candidate |
| POST | `/experience/transcribe` | Audio → transcript | Candidate |
| POST | `/experience/extract` | Transcript → structured profile (AI) | Candidate |
| POST | `/mapping/suggest` | Profile → ranked QPs w/ citations (AI) | Candidate/Assessor |
| POST | `/assessments` | Create assessment for confirmed QP | Coordinator |
| GET | `/assessments/{id}/next-item` | Adaptive next item | Candidate |
| POST | `/assessments/{id}/responses` | Submit response(s) (idempotent) | Candidate |
| POST | `/evidence` (tus resumable) | Upload evidence | Candidate/Assessor |
| POST | `/evidence/{id}/analyze` | OCR/VLM tagging | System |
| POST | `/evidence/attest` | Employer OTP attestation | Employer |
| GET | `/assessments/{id}/review` | Aggregate review packet (profile, evidence, AI rationale) | Assessor |
| PUT | `/assessments/{id}/rubric/{pc}` | Accept/override score | Assessor |
| GET | `/assessments/{id}/viva-suggestions` | AI follow-up questions | Assessor |
| POST | `/assessments/{id}/decision` | **Final decision + e-sign** | Assessor only |
| GET | `/credentials/{id}/verify` | Public verification | Anyone |
| GET | `/analytics/moderation` | κ/ICC, drift | Moderator |
| POST | `/sync/push`, GET `/sync/pull?since=` | Offline sync | Clients |

AuthZ: JWT with role claims; `decision` endpoint rejects any token not issued to a human assessor with active accreditation.

## 4. Sync protocol (offline-first)
- Client generates UUIDv7 ids and an **idempotency key** per mutation; mutations stored in an outbox (IndexedDB) with `client_ts`, `device_id`.
- `POST /sync/push` accepts batch; server applies idempotently, returns per-item status + server versions.
- `GET /sync/pull?since=<cursor>` returns changes (QP/NOS/item bank updates, assignments, AI results that completed late).
- **Conflict rules**: append-only data (responses, evidence, audit) never conflicts; mutable fields use *server-authoritative for decisions*, *last-writer-wins with version check* for profile edits, with conflict surfaced to assessor if both edited.
- Large media: **tus** chunked resumable upload with SHA-256 verification; resumes after network loss; Wi-Fi/priority policy configurable.
- Local storage encrypted with a key derived from user PIN/device (WebCrypto); wipe after sync + TTL.

## 5. Verifiable credential (sketch)
```json
{ "@context": ["https://www.w3.org/ns/credentials/v2"],
  "type": ["VerifiableCredential","RPLCompetencyCredential"],
  "issuer": "did:web:eklavya.example",
  "credentialSubject": {"id":"urn:candidate:…","qp":"<QP code>","nsqf_level":4,
     "nos_results":[{"nos":"…","result":"Competent","score":78}],
     "assessor":"<id>","decision_ts":"…"},
  "proof": {"type":"Ed25519Signature2020", "...": "..."} }
```
QR encodes the verify URL; verification checks signature + revocation status. Final issuing authority (SSC/NSDC) governance **[Verify]** — Eklavya produces the recommendation/credential payload under that authority's keys.

## 6. Audit hash chain
`hash_n = SHA256(hash_{n-1} || canonical_json(event_n))`; periodic anchor of head hash to external store for tamper-evidence.
