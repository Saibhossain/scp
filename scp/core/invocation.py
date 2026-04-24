import uuid
from scp.utils.hashing import H
from scp.utils.serialization import serialize


class SignedInvocation:
    def __init__(self, ctx_ids, op, args, seq, principal, signer):
        self.id = str(uuid.uuid4())
        self.ctx_ids = ctx_ids
        self.op = op
        self.args = args
        self.seq = seq
        self.principal = principal

        payload = H(serialize({
            "id": self.id,
            "ctx_ids": self.ctx_ids,
            "op": self.op,
            "args": self.args,
            "seq": self.seq,
            "principal": self.principal
        }))

        self.signature = signer.sign(payload)
        self.public_key = signer.public_bytes()

    def verify(self):
        from scp.crypto.ed25519 import Ed25519Verifier

        verifier = Ed25519Verifier(self.public_key)

        payload = H(serialize({
            "id": self.id,
            "ctx_ids": self.ctx_ids,
            "op": self.op,
            "args": self.args,
            "seq": self.seq,
            "principal": self.principal
        }))

        return verifier.verify(payload, self.signature)