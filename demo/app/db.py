"""SQLite access: one shared connection guarded by a lock (demo scale)."""
import json, os, secrets, sqlite3, threading
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = os.environ.get("EKLAVYA_DB") or str(Path(__file__).resolve().parent.parent / "data" / "eklavya.db")

lock = threading.Lock()
_conn: sqlite3.Connection | None = None

TABLES = ["users", "tokens", "assessments", "responses", "theta", "evidence", "attestations", "rubric", "decisions",
          "credentials", "audit", "anchor_blocks", "anchor_leaves", "sync_log", "config"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, role TEXT, name TEXT, lang TEXT, gender TEXT, region TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS tokens(token TEXT PRIMARY KEY, user_id TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS assessments(id TEXT PRIMARY KEY, candidate_id TEXT, qp_id TEXT, status TEXT, lang TEXT,
  profile_json TEXT, created_at TEXT, updated_at TEXT, decided_at TEXT, synthetic INTEGER DEFAULT 0, summary_json TEXT, assessor_id TEXT);
CREATE TABLE IF NOT EXISTS responses(id TEXT PRIMARY KEY, assessment_id TEXT, item_id TEXT, nos_id TEXT, response_json TEXT,
  correct INTEGER, score REAL, latency_ms INTEGER, idem_key TEXT, theta_after REAL, created_at TEXT, UNIQUE(assessment_id, idem_key));
CREATE TABLE IF NOT EXISTS theta(assessment_id TEXT, nos_id TEXT, theta REAL, n INTEGER, PRIMARY KEY(assessment_id, nos_id));
CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY, assessment_id TEXT, kind TEXT, filename TEXT, mime TEXT, sha256 TEXT, size INTEGER,
  caption TEXT, geo_json TEXT, captured_at TEXT, tags_json TEXT, flags_json TEXT, data BLOB, created_at TEXT);
CREATE TABLE IF NOT EXISTS attestations(id TEXT PRIMARY KEY, assessment_id TEXT, employer_name TEXT, phone TEXT, otp TEXT, status TEXT, created_at TEXT, confirmed_at TEXT);
CREATE TABLE IF NOT EXISTS rubric(assessment_id TEXT, pc_id TEXT, nos_id TEXT, ai_score REAL, ai_conf REAL, ai_rationale TEXT, citations_json TEXT,
  final_score REAL, override_reason TEXT, updated_by TEXT, updated_at TEXT, PRIMARY KEY(assessment_id, pc_id));
CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY, assessment_id TEXT, outcome TEXT, note TEXT, signature_name TEXT, assessor_id TEXT, qp_score REAL, created_at TEXT, hash TEXT);
CREATE TABLE IF NOT EXISTS credentials(id TEXT PRIMARY KEY, assessment_id TEXT, vc_json TEXT, hash TEXT, issued_at TEXT, revoked INTEGER DEFAULT 0, revoked_at TEXT);
CREATE TABLE IF NOT EXISTS audit(seq INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, actor_id TEXT, actor_role TEXT, action TEXT, entity TEXT, entity_id TEXT,
  payload TEXT, prev_hash TEXT, hash TEXT);
CREATE TABLE IF NOT EXISTS anchor_blocks(block_no INTEGER PRIMARY KEY, ts TEXT, merkle_root TEXT, tx TEXT, network TEXT, leaves_json TEXT, audit_head TEXT, audit_len INTEGER, prev_hash TEXT, block_hash TEXT);
CREATE TABLE IF NOT EXISTS anchor_leaves(leaf_hash TEXT, kind TEXT, ref TEXT, block_no INTEGER);
CREATE TABLE IF NOT EXISTS sync_log(seq INTEGER PRIMARY KEY AUTOINCREMENT, idem_key TEXT UNIQUE, user_id TEXT, type TEXT, status TEXT, result_json TEXT, client_ts TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS config(k TEXT PRIMARY KEY, v TEXT);
CREATE INDEX IF NOT EXISTS ix_resp_a ON responses(assessment_id);
CREATE INDEX IF NOT EXISTS ix_ev_a ON evidence(assessment_id);
CREATE INDEX IF NOT EXISTS ix_ev_sha ON evidence(sha256);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(5)}"


def connect(path: str | None = None) -> sqlite3.Connection:
    global _conn
    path = path or DB_PATH
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL") if path != ":memory:" else None
    c.execute("PRAGMA foreign_keys=OFF")
    c.executescript(SCHEMA)
    _conn = c
    return c


def conn() -> sqlite3.Connection:
    return _conn if _conn is not None else connect()


def wipe(c: sqlite3.Connection) -> None:
    for t in TABLES:
        c.execute(f"DELETE FROM {t}")
    c.execute("DELETE FROM sqlite_sequence")


def jl(s):
    return json.loads(s) if s else None


def jd(o) -> str:
    return json.dumps(o, ensure_ascii=False, sort_keys=True)
