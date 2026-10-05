"""Ed25519-signed Verifiable Credential (JSON) issuance + verification."""
import base64, hashlib, json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from . import db
from .audit import canon

ISSUER_ID = "did:web:eklavya.demo"
VM = ISSUER_ID + "#key-1"


def _b64(b: bytes) -> str: return base64.urlsafe_b64encode(b).decode().rstrip("=")
def _unb64(s: str) -> bytes: return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def private_key(c) -> Ed25519PrivateKey:
    r = c.execute("SELECT v FROM meta WHERE k='issuer_key'").fetchone()
    if r:
        return Ed25519PrivateKey.from_private_bytes(_unb64(r["v"]))
    k = Ed25519PrivateKey.generate()
    raw = k.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
    c.execute("INSERT OR REPLACE INTO meta(k,v) VALUES('issuer_key',?)", (_b64(raw),))
    return k


def public_key_b64(c) -> str:
    pub = private_key(c).public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return _b64(pub)


def vc_hash(vc: dict) -> str:
    return hashlib.sha256(canon(vc).encode()).hexdigest()


def issue(c, cred_id: str, assessment: dict, candidate: dict, qp: dict, result: dict, decision: dict, assessor: dict, issued_at: str | None = None) -> dict:
    issued_at = issued_at or db.now()
    vc = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "id": f"urn:eklavya:credential:{cred_id}",
        "type": ["VerifiableCredential", "SkillCredential"],
        "issuer": {"id": ISSUER_ID, "name": "Eklavya Assessment Authority (demo)"},
        "issuanceDate": issued_at,
        "credentialSubject": {
            "id": f"did:eklavya:{candidate['id']}",
            "name": candidate["name"],
            "qualificationPack": {"id": qp["id"], "code": qp["code"], "title": qp["title"], "nsqfLevel": result["nsqf_level"]},
            "qpScore": result["qp_score"],
            "nosResults": [{"nos": n["nos_id"], "title": n["title"], "score": n["score"], "core": n["core"]} for n in result["nos_results"]],
            "outcome": decision["outcome"],
        },
        "evidence": [{"type": "CertifiedByHumanAssessor", "assessmentId": assessment["id"], "assessor": assessor["name"],
                      "decisionHash": decision["hash"], "note": "Final decision made by a human assessor; AI outputs are advisory only."}],
        "disclaimer": "Demo credential. Illustrative content modelled on public NSQF QPs.",
    }
    sig = private_key(c).sign(canon(vc).encode())
    vc["proof"] = {"type": "Ed25519Signature2020", "created": issued_at, "verificationMethod": VM,
                   "proofPurpose": "assertionMethod", "proofValue": _b64(sig)}
    h = vc_hash(vc)
    c.execute("INSERT INTO credentials(id,assessment_id,vc_json,hash,issued_at,revoked) VALUES(?,?,?,?,?,0)",
              (cred_id, assessment["id"], json.dumps(vc, ensure_ascii=False), h, issued_at))
    return {"id": cred_id, "vc": vc, "hash": h, "issued_at": issued_at}


def signature_ok(c, vc: dict) -> bool:
    try:
        body = {k: v for k, v in vc.items() if k != "proof"}
        sig = _unb64(vc["proof"]["proofValue"])
        private_key(c).public_key().verify(sig, canon(body).encode())
        return True
    except (InvalidSignature, KeyError, ValueError, TypeError):
        return False
