from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


class Ed25519Signer:
    def __init__(self, sk):
        self.sk = sk
        self.pk = sk.public_key()

    @staticmethod
    def generate():
        return Ed25519Signer(Ed25519PrivateKey.generate())

    def sign(self, msg: bytes) -> bytes:
        return self.sk.sign(msg)

    def verify(self, sig: bytes, msg: bytes) -> bool:
        try:
            self.pk.verify(sig, msg)
            return True
        except Exception:
            return False