# 01 · Research & Problem Analysis

## 1. What is RPL?
Recognition of Prior Learning (RPL) is an assessment process that evaluates a person's existing skills, knowledge and experience gained through formal, non-formal or informal learning, and certifies them against a national standard. In India it is anchored to the **National Skills Qualification Framework (NSQF)** and delivered under Skill India (e.g., the RPL component of PMKVY) through **Sector Skill Councils (SSCs)** and their accredited **assessment bodies**.

## 2. How RPL works today (as publicly documented)
- **NSQF**: 10 levels (1–10) describing outcomes by knowledge, skills, responsibility. Each job role is defined by a **Qualification Pack (QP)** composed of **National Occupational Standards (NOS)** — each NOS lists performance criteria, knowledge & understanding, and skills.
- **Process** (typical): candidate mobilization → registration → orientation (documented as ~12 hours: skill orientation, assessment process, soft skills, basic entrepreneurship) → assessment (documentary evidence + self-assessment + theory/viva + practical demonstration) → certification → **bridge training** if gaps exist (documented as ~68 hours) → re-assessment.
- **Scoring**: candidates are assessed on core and non-core NOS; core NOS carry **70%** weightage, non-core **30%**. Pass thresholds are set by the SSC/assessment guidelines **[Verify per QP]**.
- **Assessors** from SSC-accredited assessment bodies conduct the evaluation, typically on-site.

## 3. Pain points (problem statement + analysis)
| # | Problem | Consequence |
|---|---------|-------------|
| 1 | Assessment is heavily manual and assessor-dependent | Slow to scale; throughput capped by assessor availability |
| 2 | Inconsistent judgments across assessors/locations | Fairness and certification credibility suffer |
| 3 | Workers can't take days off for scheduled assessments | Drop-off, especially daily-wage workers |
| 4 | Experience is oral and undocumented | Hard to evidence years of work; paper-heavy proofs |
| 5 | Language & literacy barriers | Written tests exclude capable workers |
| 6 | Poor connectivity in rural/peri-urban areas | Cloud-only tools fail where RPL is needed most |
| 7 | QP/NOS mapping is a manual expert task | Candidates mapped to wrong or too-low a QP |
| 8 | No structured gap → training linkage | Failed candidates get no actionable path |
| 9 | Fraud/impersonation risk, weak audit trail | Integrity concerns |

## 4. Stakeholders
Candidate (worker) · Assessor · Assessment body / Training partner · Sector Skill Council · NSDC / MSDE / NCVET (regulatory) · Employers · Government scheme administrators.

## 5. Landscape & lessons
- Many SIH-26242 teams are converging on: evidence-based multi-modal assessment, offline-first PWA, human-governed AI. **Differentiation therefore must come from execution quality**: real QP/NOS grounding (RAG), explainable & auditable scoring, assessor calibration analytics, voice-first Indic UX, and a polished end-to-end working demo.
- Global practice (ILO, UNESCO, Australia/South Africa RPL systems) stresses: evidence triangulation, assessor moderation, appeals, and clear learner pathways — all incorporated here.

## 6. Design principles derived from research
1. **Human final authority** — AI is decision support only; legally and ethically required for certification integrity.
2. **Evidence triangulation** — combine documents, structured Q&A, practical media, and third-party attestation.
3. **Standards-grounded** — every question, score and recommendation traces to a specific NOS performance criterion.
4. **Inclusive** — voice/vernacular first, low-literacy friendly, low-bandwidth, low-end Android.
5. **Offline-first** — capture anywhere, sync later, conflict-safe.
6. **Auditable & fair** — immutable audit logs, explanations, bias monitoring, appeal path.

## 7. Sources
- ILO — [Recognition of Prior Learning: Background and Proposal for a Pilot in India](https://www.ilo.org/media/446091/download)
- NSDC — [Recognition of Prior Learning](https://worldskills.nsdcindia.org/public/recognition-of-prior-learning)
- PSSCIVE — [Guidelines for Recognition of Prior Learning (RPL)](https://www.psscive.ac.in/storage/uploads/documents/1709540278_Guidelines%20for%20Recognition%20of%20Prior%20Learning%20(RPL).pdf)
- PIB — [Skill India Mission: RPL](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2022/apr/doc202242548301.pdf)
- Vikaspedia — [Recognition of Prior Learning](https://en.vikaspedia.in/viewcontent/social-welfare/skill-development/best-practices-on-skill-development/recognition-of-prior-learning-rpl?lgn=en)
- FICSI, THSC (sector council RPL pages): [FICSI](https://www.ficsi.in/recognition-of-prior-learning), [THSC](https://thsc.in/recognition-of-prior-learning/)
- Other public SIH26242 repositories (for landscape awareness only; no code reused).
