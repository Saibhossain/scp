import uuid
from scp.core.types import SignedInvocation
from scp.utils.hashing import H


def create_invocation(agent_signer, ctx_ids, op, args, seq, principal):
    inv_id = str(uuid.uuid4())

    msg = H(
        f"{inv_id}|{ctx_ids}|{op}|{args}|{seq}|{principal}"
    ).encode()

    sig = agent_signer.sign(msg)

    return SignedInvocation(
        id=inv_id,
        ctx_ids=ctx_ids,
        op=op,
        args=args,
        seq=seq,
        principal=principal,
        sigma=sig
    )