import uuid
from scp.utils.hashing import H
from scp.utils.serialization import serialize


class SignedContext:
    def __init__(self, D, src, label, meta, signer):
        self.id = str(uuid.uuid4())
        self.D = D
        self.src = src
        self.L = label
        self.meta = meta

        payload = H(serialize({
            "id": self.id,
            "D": self.D,
            "L": self.L,
            "src": self.src,
            "meta": self.meta
        }))

        self.signature = signer.sign(payload)
        self.public_key = signer.public_bytes()

    def verify(self):
        from scp.crypto.ed25519 import Ed25519Verifier

        verifier = Ed25519Verifier(self.public_key)

        payload = H(serialize({
            "id": self.id,
            "D": self.D,
            "L": self.L,
            "src": self.src,
            "meta": self.meta
        }))

        return verifier.verify(payload, self.signature)