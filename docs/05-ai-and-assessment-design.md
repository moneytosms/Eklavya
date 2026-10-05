# 05 · AI & Assessment Design

## 0. Principle: *AI can help, AI cannot certify*
Every AI output is typed as **Suggestion** (with confidence, rationale, citations). Only a human assessor can create a **Decision**. The API physically has no endpoint where an AI actor can write a final outcome; decision records require an authenticated assessor identity + e-sign.

## 1. Pipeline overview
```
Voice/Text → STT → Normalise → Experience Extraction (LLM, JSON schema)
   → Retrieval over NOS (hybrid) → LLM re-rank + justification → QP candidates
   → Evidence tagging (OCR/VLM) → Coverage map per NOS/PC (what is evidenced, what is not)
   → Question generation targeted at uncovered/low-confidence PCs
   → Adaptive testing → Rubric pre-score → Assessor review → Final decision
```

## 2. Experience extraction
- **Input**: transcript (any supported language; translate to English internally while keeping original).
- **Output schema** (validated with Pydantic; retry on schema failure):
```json
{ "occupation_guess": "AC technician",
  "years_experience": 8,
  "tasks": [{"verb":"charge","object":"refrigerant gas","tool":"manifold gauge","context":"split AC"}],
  "tools": ["manifold gauge","vacuum pump"], "materials": ["R32"],
  "work_settings": ["residential"], "supervision_level": "independent",
  "uncertain": ["electrical diagnosis depth"] }
```
- Guardrails: no inference of protected attributes; claims are labelled *self-declared* until evidenced.

## 3. QP/NOS mapping (RAG)
1. Index each NOS performance criterion (PC), knowledge item and skill as chunks with metadata (QP, NOS id, core/non-core, NSQF level).
2. Retrieve top-k by hybrid BM25 + embedding similarity for each extracted task.
3. LLM re-ranks and outputs `{qp, nsqf_level, matched_nos[], matched_pc[], confidence, rationale}`; **must cite chunk ids — outputs with uncited claims are rejected**.
4. Candidate QP score = coverage-weighted aggregate (core NOS weighted 70, non-core 30) → ranked list; assessor/candidate confirms.
5. Also suggest a **level-appropriate** alternative (e.g., L3 vs L4) based on responsibility/autonomy signals.

## 4. Evidence analysis
| Evidence | Processing | Output |
|---|---|---|
| Documents (letters, certs, invoices) | OCR → LLM field extraction → authenticity heuristics (format, dates, duplicates) | Verified-fields + flags |
| Photos | VLM: describe work, tools, safety gear → map to PC | PC tags + confidence |
| Video (practical) | Keyframe sampling + audio STT → step detection vs rubric | Timestamped rubric suggestions |
| Attestation | Employer OTP confirm of role, duration | Trust weight ↑ |
**Integrity checks**: SHA-256 hash at capture, EXIF/GPS/time consistency, perceptual-hash duplicate detection across candidates, basic synthetic-media/screen-recapture heuristics → raise **flags**, never auto-reject.
Evidence weight = source reliability × recency × specificity.

## 5. Adaptive assessment engine
- **Item bank**: per PC, items tagged with difficulty (1–5), type (MCQ, image-ID, scenario, ordering, voice-answer, numeric), language variants, audio. Seeded from curated + LLM-generated items **reviewed by SME before activation** (no live-generated high-stakes items without review).
- **Selection**: Start at difficulty 3 for each NOS. Maintain ability estimate θ per NOS (Elo/1-PL IRT-style update). Next item maximises information near θ among PCs with lowest evidence coverage. Stop when SE(θ) < threshold or max items (≈8–12 per NOS).
- **Open answers (voice/text)**: LLM grades against a **reference answer + rubric keypoints**, returns matched/missed keypoints + confidence; low confidence → routed to assessor.
- **Anti-cheating**: randomised item variants, time-boxing, session proctoring signals (tab/focus, repeated voice), assessor-led viva for high-stakes items.

## 6. Practical assessment & rubric scoring
- Rubric auto-generated from NOS PCs into a checklist (critical safety steps flagged **must-pass**).
- Scoring scale per criterion: 0 Not demonstrated · 1 Partial · 2 Competent · 3 Proficient.
- AI pre-fills from video/photos with timestamps; assessor confirms per row. **Critical-criteria failure ⇒ NOS cannot be Competent regardless of total.**

## 7. Scoring & outcome (all weights config-driven)
```
NOS_score = w_t·Theory + w_p·Practical + w_e·Evidence         (default 0.25 / 0.50 / 0.25)  [Assumption]
QP_score  = 0.70·mean(core NOS) + 0.30·mean(non-core NOS)       (per RPL guidelines)
Outcome   = Certified | Bridge-needed(list of gap NOS) | Reassess   (thresholds per SSC)  [Verify]
```
Gap analysis → map each gap PC to bridge modules (68-hr bridge reference) with estimated hours.

## 8. Human-in-the-loop UX
- Side-by-side: *AI suggestion + rationale + citations + confidence* vs. *assessor decision*.
- Override requires structured reason; overrides feed calibration analytics (not auto-training without governance review).
- Confidence thresholds: high (>0.85) pre-selected but still needs confirm; low (<0.6) highlighted for deep review.

## 9. Fairness, quality & safety
- **Bias monitoring**: score/flag parity by language, gender, region, dialect, STT word-error-rate; dashboards + alerts.
- **Language robustness**: evaluate STT/LLM on code-mixed (Hinglish) speech; fallback to assessor-led oral.
- **Calibration**: golden-set candidates scored by experts; inter-rater κ/ICC; assessor drift detection; moderation sampling (e.g., 10%).
- **Evaluation suite** (offline): mapping top-3 accuracy vs expert labels, extraction F1, rubric-suggestion agreement with assessors, hallucination/citation-failure rate. Targets for MVP: top-3 QP accuracy ≥ 85%, rationale-citation validity 100%.
- **Prompt-injection defence**: treat candidate text/docs as untrusted data; delimited inputs; JSON-schema outputs; no tool access for extraction prompts.
- **Fail-safe**: if AI unavailable → assessment proceeds with static rules/item bank + manual assessor flow.
- **Privacy**: PII minimised before LLM calls; option to run self-hosted models; no training on candidate data without consent.

## 10. Offline AI strategy
| Capability | Online | Offline fallback |
|---|---|---|
| STT | Cloud/Bhashini | Small on-device Whisper-class (WASM) or record-now-transcribe-later |
| Mapping | Cloud LLM + RAG | Keyword/TF-IDF match against cached NOS index → refine on sync |
| Adaptive Q | Server | Client-side selector over cached item bank |
| Grading open answers | LLM | Queue; MCQ/structured graded locally; open answers graded on sync |
| Rubric pre-fill | VLM | Assessor manual; AI suggestions arrive later |
