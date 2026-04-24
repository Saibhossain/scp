from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization


class Ed25519Signer:
    def __init__(self, private_key: Ed25519PrivateKey):
        self.sk = private_key
        self.pk = private_key.public_key()

    @staticmethod
    def generate():
        sk = Ed25519PrivateKey.generate()
        return Ed25519Signer(sk)

    def sign(self, message: bytes) -> bytes:
        return self.sk.sign(message)

    def public_bytes(self) -> bytes:
        return self.pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )


class Ed25519Verifier:
    def __init__(self, public_key_bytes: bytes):
        self.pk = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            self.pk.verify(signature, message)
            return True
        except:
            return False