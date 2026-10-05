# 07 · Offline, Security & Compliance

## 1. Offline / low-connectivity design
| Concern | Approach |
|---|---|
| App availability | PWA with Service Worker precache (app shell, i18n bundles, item bank for assigned QP, NOS index) |
| Data capture | All forms/answers write to IndexedDB first; UI never blocks on network |
| Media | Client-side compression (image ≤ 1280 px, video ≤ 480p/short clips), resumable chunk upload |
| Sync | Outbox + background sync; exponential backoff; batch + delta; per-record status shown ("Saved on phone · Waiting to sync · Synced") |
| Assessor field mode | Pre-download assigned candidates + review packets; sign decisions offline (queued, device-bound key), counter-signed server-side on sync |
| Time integrity | Capture device time + monotonic offset; server records receive time; large skew flagged |
| Storage limits | Quota monitoring; LRU eviction only of synced media |
| Bandwidth | Text-first payloads, gzip/brotli, AI results optional/deferred |
| Air-gapped option | Local edge server at training centre with sync to cloud |
| SMS fallback | OTP/attestation via SMS (no data needed on verifier's side beyond a link/short code) |

## 2. Security controls
- **Transport/rest**: TLS 1.3; AES-256 at rest; envelope encryption for evidence; KMS-managed keys.
- **Identity**: OTP (rate-limited), staff MFA, optional DigiLocker/Aadhaar eKYC; device binding for assessors.
- **AuthZ**: RBAC + attribute rules (assessor sees only assigned candidates; moderator sees sampled sets); least privilege service accounts.
- **Integrity**: hash-chained audit; SHA-256 evidence hashes; signed credentials; immutable decision records.
- **Application**: OWASP ASVS L2, input validation, CSP, dependency scanning, secrets in vault, pen-test before launch.
- **AI-specific**: prompt-injection isolation, output schema validation, PII minimisation/redaction before external model calls, model/prompt version logged per suggestion, content filtering on generated items, human review for item bank.
- **Abuse resistance**: impersonation (liveness/selfie match with consented ID **[optional]**), duplicate-evidence detection, assessor-collusion analytics (anomalous pass rates).

## 3. Privacy & legal compliance (India)
- **DPDP Act 2023** alignment: notice & explicit consent (multilingual, audio-read option), purpose limitation (assessment/certification only), data minimisation, retention schedule, right to access/correction/erasure, grievance officer, breach notification process, children's data not targeted.
- **Data residency**: store in India region; self-hosted AI option for sovereign deployment.
- **Aadhaar**: no storage of Aadhaar number; use tokenised/masked references per UIDAI norms.
- **Accessibility**: WCAG 2.1 AA; GIGW guidelines for government web.
- **Retention**: raw media retained for appeal window (e.g., 12 months **[Assumption]**), then deleted/aggregated; audit logs retained per policy.

## 4. Responsible-AI governance
1. Human final authority (enforced in code, not policy alone).
2. Transparency: candidates told where AI is used; assessor sees rationale.
3. Contestability: appeal → independent re-assessment by another assessor.
4. Monitoring: bias, drift, hallucination/citation-failure dashboards; quarterly review board.
5. Change control: model/prompt versions pinned; golden-set regression tests before rollout.
6. No automated decisions with legal effect without human review.

## 5. Reliability & operations
Backups (PITR), multi-AZ, health checks, queue dead-letter handling, graceful AI degradation, SLOs (API p95 < 500 ms excluding AI; sync success ≥ 99.5%), runbooks.
