import json

def serialize(obj) -> bytes:
    return json.dumps(obj, sort_keys=True).encode()