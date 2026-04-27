import hashlib

def H(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()