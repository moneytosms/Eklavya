# Eklavya — *Transforming experience into recognized skill*

**SIH 2026 · Problem Statement SIH26242** · Ministry of Skill Development and Entrepreneurship (MSDE)
**Theme:** Smart Education · **Category:** Software
**Title:** AI-Assisted Skill Assessment Tool for Recognition of Prior Learning (RPL)

Eklavya is an offline-first, AI-assisted RPL assessment platform that converts a worker's real-world experience into a structured, evidence-backed, **NSQF-aligned competency profile** mapped to Qualification Packs (QPs) and National Occupational Standards (NOS).

> **Governance invariant: AI assists, the human assessor decides.** AI never issues a pass/fail. It produces recommendations, consistency checks and evidence summaries; the assessor reviews, overrides if needed, and signs the final outcome.

## Document index

| # | Document | Purpose |
|---|----------|---------|
| 01 | [Research & problem analysis](docs/01-research-and-problem-analysis.md) | RPL landscape in India, gaps, stakeholders, existing approaches |
| 02 | [Solution overview](docs/02-solution-overview.md) | Vision, end-to-end journey, differentiators |
| 03 | [Product requirements (PRD)](docs/03-product-requirements.md) | Personas, functional and non-functional requirements, user stories |
| 04 | [System architecture](docs/04-system-architecture.md) | Components, tech stack, integrations, deployment |
| 05 | [AI & assessment design](docs/05-ai-and-assessment-design.md) | Skill extraction, QP mapping, adaptive questions, scoring, human-in-the-loop, fairness |
| 06 | [Data model & API](docs/06-data-model-and-api.md) | Entities, schema, REST endpoints, sync protocol |
| 07 | [Offline, security & compliance](docs/07-offline-security-compliance.md) | Low-connectivity design, DPDP Act, audit, integrity |
| 08 | [Demo plan, roadmap & risks](docs/08-demo-plan-roadmap-risks.md) | Hackathon demo script, MVP scope, roadmap, risks, metrics |
| 09 | [SIH submission content & judge Q&A](docs/09-submission-content-and-qna.md) | Slide-by-slide PPT content, 1-minute pitch, anticipated questions |

## One-paragraph pitch

India has tens of millions of skilled workers — electricians, plumbers, tailors, mechanics, masons — with years of experience and no certificate. Today's RPL assessment relies on slow, assessor-dependent practical evaluation that is inconsistent across locations. Eklavya lets a worker describe their experience in their own language (voice or text), upload evidence (photos, videos, employer letters), and take an adaptive, QP-specific assessment — even offline. AI structures the evidence, maps it to NOS, generates adaptive questions and a rubric-based pre-score with explanations; a human assessor verifies and certifies. The result is a consistent, auditable, NSQF-level competency profile, a gap analysis with bridge-course recommendations, and a verifiable digital credential.

## Status

Documentation complete (this repo). Demo implementation is the next step; see [08](docs/08-demo-plan-roadmap-risks.md) for the MVP scope.

> Note: figures and scheme details cited in the docs come from public sources listed in doc 01. Items marked **[Assumption]** or **[Verify]** are design choices or details to confirm with MSDE/NSDC/SSC before production.
