# 09 · SIH Submission Content & Judge Q&A

## 1. Slide-by-slide content (typical SIH template)
**Slide 1 – Title:** Team, PS ID SIH26242, Problem title, Theme *Smart Education*, Category *Software*. Tagline: *Transforming experience into recognized skill.*

**Slide 2 – Problem understanding:** Millions of skilled workers lack certification; RPL assessment is manual, assessor-dependent, inconsistent, hard to schedule, language/connectivity-challenged. (See doc 01 table.)

**Slide 3 – Proposed solution:** Eklavya — 5-step journey Declare → Evidence → Assess → Verify → Recognize. AI assists, human decides. (Diagram from doc 02.)

**Slide 4 – Innovation & uniqueness:** NOS-grounded RAG with citations; explainable rubric pre-scoring; assessor calibration analytics; voice-first Indic UX; true offline-first; evidence integrity; gap → bridge pathway; governance by design.

**Slide 5 – Technical approach:** Architecture diagram (doc 04), AI pipeline (doc 05), tech stack table.

**Slide 6 – Feasibility & viability:** Built on open/standard tech; pluggable AI (hosted or self-hosted); phased pilot; low cost per candidate; uses existing SSC/NSQF structures — no new certification authority needed.

**Slide 7 – Impact & benefits:** Candidates (access, dignity, pathway); assessors (2× capacity, consistency); SSC/NSDC (quality analytics, auditability); employers (verifiable credentials); economy (formalising informal workforce). Metrics from doc 08.

**Slide 8 – Offline & security & ethics:** Offline sync design, DPDP compliance, human final authority, bias monitoring, audit.

**Slide 9 – Scalability & roadmap:** Pilot → integration → scale (doc 08).

**Slide 10 – Research & references:** Sources in doc 01.

## 2. 60-second pitch
"Ramesh has repaired air conditioners for eight years, but without a certificate he's treated as unskilled. Eklavya lets him describe his work in Hindi, upload photos and employer proof, and take an adaptive test — even without internet. Our AI maps his experience to the right NSQF Qualification Pack, cites the exact National Occupational Standards, and pre-scores his evidence with explanations. But AI never certifies: a human assessor reviews every score, overrides where needed, and signs. The result is a consistent, auditable competency profile, a gap-to-bridge-course plan, and a verifiable digital credential. Eklavya turns experience into recognized skill — at scale, fairly, and in every language."

## 3. Anticipated judge questions
| Question | Answer |
|---|---|
| Can AI certify? | No. Enforced in API: decisions require authenticated, accredited human assessor + e-sign. AI outputs are labelled suggestions. |
| How do you stop hallucinated standards? | RAG over ingested QP/NOS; outputs must cite chunk IDs or are rejected; golden-set regression tests. |
| How is consistency improved? | NOS-derived rubrics, AI pre-scores as common anchor, moderation sampling, κ/ICC dashboards, drift alerts. |
| What about low connectivity? | PWA + IndexedDB outbox, resumable uploads, client-side adaptive selector, on-device/queued STT, optional local edge kiosk. |
| Low literacy / languages? | Voice-first, audio prompts, image-based items, Indic STT/TTS (Bhashini), assessor oral fallback. |
| Fraud / impersonation? | Hashes, geo/time stamps, duplicate detection, employer attestation, optional liveness, hash-chained audit, collusion analytics. |
| Data privacy? | DPDP-aligned consent, minimisation, India-region storage, no Aadhaar storage, self-hosted AI option. |
| Why will SSCs adopt it? | Works within existing QP/NOS & assessor model; reduces cost/time; provides audit + quality analytics. |
| How does it integrate? | Skill India Digital Hub/SDMS, DigiLocker, NQR, Bhashini via adapters (proposed; APIs to be confirmed). |
| Cost? | Tiered AI models + caching; target ≈ ₹10–15 AI cost/candidate [estimate]; open-source stack. |
| Bias? | Parity monitoring across language/gender/region; STT WER tracking; human review; appeals. |
| What if AI is down? | Graceful degradation: static item bank + manual assessor flow. |

## 4. Submission checklist
- [ ] PPT (10 slides) from section 1 · [ ] 3–5 min demo video (script in doc 08) · [ ] GitHub repo link (this repo) · [ ] Architecture & flow diagrams exported as images · [ ] Team details & PS ID · [ ] Deployed demo link (if available)
