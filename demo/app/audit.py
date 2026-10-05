"""Hash-chained audit log (SHA-256). Each event hash covers the previous hash + canonical body."""
import hashlib, json
from . import db

GENESIS = "0" * 64


def canon(o) -> str:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _body(ts, actor_id, actor_role, action, entity, entity_id, payload) -> str:
    return canon({"ts": ts, "actor_id": actor_id, "actor_role": actor_role, "action": action,
                  "entity": entity, "entity_id": entity_id, "payload": payload})


def append(c, actor, action: str, entity: str = "", entity_id: str = "", payload=None, ts: str | None = None) -> dict:
    """actor: user dict {id, role} or None (system)."""
    row = c.execute("SELECT hash FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
    prev = row["hash"] if row else GENESIS
    ts = ts or db.now()
    aid = actor["id"] if actor else "system"
    arole = actor["role"] if actor else "system"
    payload = payload or {}
    h = hashlib.sha256((prev + _body(ts, aid, arole, action, entity, entity_id, payload)).encode()).hexdigest()
    cur = c.execute("INSERT INTO audit(ts,actor_id,actor_role,action,entity,entity_id,payload,prev_hash,hash) VALUES(?,?,?,?,?,?,?,?,?)",
                    (ts, aid, arole, action, entity, entity_id, canon(payload), prev, h))
    return {"seq": cur.lastrowid, "hash": h}


def row_to_event(r) -> dict:
    return {"seq": r["seq"], "ts": r["ts"], "actor_id": r["actor_id"], "actor_role": r["actor_role"], "action": r["action"],
            "entity": r["entity"], "entity_id": r["entity_id"], "payload": json.loads(r["payload"] or "{}"),
            "prev_hash": r["prev_hash"], "hash": r["hash"]}


def list_events(c, limit: int = 100, offset: int = 0) -> list[dict]:
    rows = c.execute("SELECT * FROM audit ORDER BY seq DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    return [row_to_event(r) for r in rows]


def head(c) -> tuple[str, int]:
    r = c.execute("SELECT hash, seq FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
    n = c.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
    return (r["hash"] if r else GENESIS), n


def verify(c) -> dict:
    prev = GENESIS
    n = 0
    for r in c.execute("SELECT * FROM audit ORDER BY seq ASC"):
        n += 1
        payload = json.loads(r["payload"] or "{}")
        exp = hashlib.sha256((prev + _body(r["ts"], r["actor_id"], r["actor_role"], r["action"], r["entity"], r["entity_id"], payload)).encode()).hexdigest()
        if r["prev_hash"] != prev or r["hash"] != exp:
            return {"ok": False, "head_hash": prev, "length": n, "broken_at": r["seq"],
                    "reason": "hash mismatch (event altered or chain re-ordered)"}
        prev = r["hash"]
    return {"ok": True, "head_hash": prev, "length": n, "broken_at": None}
