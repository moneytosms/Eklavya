"""Simulated permissioned anchoring ledger: append-only blocks, Merkle root over audit head + credential hashes."""
import hashlib, json
from . import audit, db

NETWORK = "Eklavya-Anchor (simulated; pluggable Polygon/Amoy testnet)"


def _h(a: str, b: str) -> str:
    return hashlib.sha256((a + b).encode()).hexdigest()


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return hashlib.sha256(b"").hexdigest()
    level = list(leaves)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [_h(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def merkle_proof(leaves: list[str], idx: int) -> list[dict]:
    proof, level = [], list(leaves)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        sib = idx ^ 1
        proof.append({"hash": level[sib], "side": "right" if sib > idx else "left"})
        level = [_h(level[i], level[i + 1]) for i in range(0, len(level), 2)]
        idx //= 2
    return proof


def verify_proof(leaf: str, proof: list[dict], root: str) -> bool:
    cur = leaf
    for p in proof:
        cur = _h(cur, p["hash"]) if p["side"] == "right" else _h(p["hash"], cur)
    return cur == root


def run(c, actor=None, ts: str | None = None) -> dict:
    head, length = audit.head(c)
    pending = c.execute("SELECT id, hash FROM credentials WHERE id NOT IN (SELECT ref FROM anchor_leaves WHERE kind='credential') ORDER BY issued_at, id").fetchall()
    leaves = [{"kind": "audit_head", "ref": f"audit#{length}", "hash": head}] + [{"kind": "credential", "ref": r["id"], "hash": r["hash"]} for r in pending]
    root = merkle_root([l["hash"] for l in leaves])
    last = c.execute("SELECT block_no, block_hash FROM anchor_blocks ORDER BY block_no DESC LIMIT 1").fetchone()
    block_no = (last["block_no"] + 1) if last else 1
    prev = last["block_hash"] if last else "0" * 64
    ts = ts or db.now()
    block_hash = hashlib.sha256((prev + root + ts + str(block_no)).encode()).hexdigest()
    tx = "0x" + hashlib.sha256((block_hash + "tx").encode()).hexdigest()
    c.execute("INSERT INTO anchor_blocks VALUES(?,?,?,?,?,?,?,?,?,?)",
              (block_no, ts, root, tx, NETWORK, json.dumps(leaves), head, length, prev, block_hash))
    for l in leaves:
        c.execute("INSERT INTO anchor_leaves VALUES(?,?,?,?)", (l["hash"], l["kind"], l["ref"], block_no))
    audit.append(c, actor, "anchor.run", "anchor_block", str(block_no), {"root": root, "tx": tx, "leaves": len(leaves)}, ts=ts)
    return {"block": block_no, "root": root, "tx": tx, "network": NETWORK, "anchored_at": ts, "audit_head": head, "audit_length": length,
            "leaves": leaves, "credentials_anchored": len(pending), "prev_block_hash": prev, "block_hash": block_hash}


def block_view(r) -> dict:
    return {"block": r["block_no"], "ts": r["ts"], "root": r["merkle_root"], "tx": r["tx"], "network": r["network"],
            "audit_head": r["audit_head"], "audit_length": r["audit_len"], "leaves": json.loads(r["leaves_json"]),
            "prev_hash": r["prev_hash"], "block_hash": r["block_hash"]}


def ledger(c) -> list[dict]:
    return [block_view(r) for r in c.execute("SELECT * FROM anchor_blocks ORDER BY block_no DESC")]


def credential_anchor(c, cred_hash: str) -> dict:
    row = c.execute("SELECT block_no FROM anchor_leaves WHERE leaf_hash=? AND kind='credential'", (cred_hash,)).fetchone()
    if not row:
        return {"status": "pending", "tx": None, "block": None, "network": NETWORK, "root": None, "proof_ok": None}
    b = c.execute("SELECT * FROM anchor_blocks WHERE block_no=?", (row["block_no"],)).fetchone()
    leaves = [l["hash"] for l in json.loads(b["leaves_json"])]
    idx = leaves.index(cred_hash)
    proof = merkle_proof(leaves, idx)
    return {"status": "anchored", "tx": b["tx"], "block": b["block_no"], "network": b["network"], "root": b["merkle_root"],
            "anchored_at": b["ts"], "proof": proof, "proof_ok": verify_proof(cred_hash, proof, b["merkle_root"]) and merkle_root(leaves) == b["merkle_root"]}
