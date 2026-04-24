import hashlib

def H(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()