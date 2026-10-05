# Eklavya Demo — Build Spec (source of truth for all agents)

Stack: **uv** project in `demo/` · **FastAPI** + SQLite (stdlib sqlite3) · static frontend served by FastAPI from `demo/app/static` (hash-routed multi-page SPA, **vanilla ES modules + Alpine.js**, handwritten CSS design system, **Lucide** SVG icons, no build step). Everything vendored locally in `static/vendor` (no runtime CDN). Run: `cd demo && uv run eklavya` (or `uv run uvicorn app.main:app --port 8000`). Works with NO API keys (deterministic engine); optional `ANTHROPIC_API_KEY` upgrades mapping/rationale text.

Layout
```
demo/pyproject.toml          (uv; script `eklavya`)
demo/app/main.py             FastAPI app, mounts /static, serves index.html at /
demo/app/db.py seed.py engine.py audit.py credential.py anchor.py
demo/app/data/qps.json items.json demo_candidates.json
demo/app/static/index.html css/eklavya.css js/{app,api,ui,i18n,store,sync}.js js/pages/*.js vendor/*
demo/tests/test_api.py
```
Content: 4 QPs (AC Technician, Electrician Domestic, Sewing Machine Operator, Plumber General) each with 4-5 NOS (core/non-core), PCs (some critical), ~8 items/NOS (mcq, image-id, scenario, ordering) in EN + HI. Mark all as "illustrative, modelled on public NSQF QPs".

## API (JSON, prefix /api)
- POST /auth/login {role:"candidate"|"assessor"|"admin", name?} -> {token,user}  (demo auth; token = opaque bearer)
- GET /qps ; GET /qps/{id}  -> QP with nos[], pcs[]
- POST /experience/extract {transcript, lang} -> {profile:{occupation_guess,years,tasks[],tools[],materials[],uncertain[]}}
- POST /mapping/suggest {profile|transcript} -> {suggestions:[{qp_id,title,nsqf_level,confidence,matched_nos:[{nos_id,title,pcs:[..],cited:[chunk ids]}],rationale}]}
- POST /assessments {candidate_id?, qp_id, profile} -> assessment {id,status,qp,...}
- GET /assessments?role-scoped ; GET /assessments/{id}
- GET /assessments/{id}/next-item -> {item|null, progress:{answered,total_est,nos_id,theta}}
- POST /assessments/{id}/responses {item_id,response,latency_ms,idem_key} -> {correct,score,theta} (idempotent on idem_key)
- POST /evidence (multipart: assessment_id, kind, file, geo?, captured_at?) -> {id,sha256,tags:[{pc_id,confidence,source:"ai"}],flags:[]}
- POST /evidence/attest {assessment_id, employer_name, phone} -> {status:"otp_sent", demo_otp}; POST /evidence/attest/confirm {…,otp}
- GET /assessments/{id}/review -> packet: profile, nos_summaries[{nos,theta,theory,practical,evidence,coverage}], evidence[], rubric[{pc_id,text,critical,ai_score,ai_conf,ai_rationale,citations,final_score,override_reason}], flags[], viva_suggestions[]
- PUT /assessments/{id}/rubric/{pc_id} {final_score,override_reason?} (assessor)
- POST /assessments/{id}/decision {outcome,note,signature_name} (assessor ONLY; 403 for others; AI cannot call) -> decision + credential
- GET /assessments/{id}/result -> competency profile {nos_results[], qp_score, nsqf_level, outcome, gaps[], bridge_plan[{module,hours}]}
- GET /credentials/{id} ; GET /credentials/{id}/verify (public) -> {valid, signature_ok, anchor:{status,tx,block,network}, revoked}
- POST /sync/push {mutations:[{idem_key,type,payload,client_ts}]} -> per-item status ; GET /sync/pull?since=
- GET /admin/analytics -> {throughput, pass_rate_by_qp, assessor_agreement:{kappa,per_nos}, override_rate, score_distribution, bias_parity:[…], ai_vs_human}
- GET /audit?limit= ; GET /audit/verify -> {ok,head_hash,length}  (SHA256 hash chain)
- POST /anchor/run -> anchors audit head + credential hashes to a **simulated permissioned ledger** (local append-only chain with Merkle root, fake tx ids, block no.); response shows root, tx, network "Eklavya-Anchor (simulated; pluggable Polygon/Amoy testnet)".
- POST /demo/reset ; GET /health

Rules: AI outputs are `AISuggestion`s; `/decision` requires assessor role + signature_name. Every mutation appends an audit event. Credential = Ed25519-signed VC JSON (use `cryptography`), QR payload = verify URL.

## Screens (hash routes)
Landing `#/` (role picker: Candidate / Assessor / Admin, "Reset demo") ·
Candidate: `#/c/start` voice/text declare (Web Speech API w/ sample-phrase chips fallback, EN/HI toggle) → `#/c/mapping` QP suggestions with NOS citations → `#/c/evidence` camera/upload, auto tags, employer attest → `#/c/assess` adaptive test w/ audio prompt (speechSynthesis), progress ring, **offline banner + airplane toggle** (simulate offline; answers go to IndexedDB outbox; sync chips Saved/Waiting/Synced) → `#/c/result` NSQF profile, gaps, bridge plan, QR credential.
Assessor: `#/a/queue` → `#/a/review/:id` (evidence gallery, AI rationale+confidence+citations, accept/override w/ reason, flags, viva suggestions, "AI cannot certify" banner, e-sign) .
Admin: `#/m/dashboard` (agreement κ, distributions, bias parity, override rate), `#/m/audit` (chain viewer + Verify button + Anchor now), `#/m/qps`.
Public: `#/verify/:id` credential verification page (signature ✓, anchor ✓).

## Design direction
NON-PURPLE. Palette: deep teal/ink primary, warm saffron accent, soft off-white surfaces, green/amber/red semantic. Inter (vendored woff2 or system stack). Radius 14-18px, soft shadows, generous spacing, subtle motion, Lucide icons everywhere, mobile-first candidate app (phone frame on desktop), dense-but-clean desktop assessor/admin console with sidebar. Dark mode via prefers-color-scheme tokens. Must look like a polished product, not a prototype.
