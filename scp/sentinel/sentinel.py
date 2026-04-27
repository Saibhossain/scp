import uuid
from scp.core.types import SignedContext
from scp.utils.hashing import H


class Sentinel:
    def __init__(self, signer):
        self.signer = signer

    def label(self, source: str) -> str:
        return "C_high" if source == "user" else "C_low"

    def ingest(self, data: str, source: str, meta=None) -> SignedContext:
        ctx_id = str(uuid.uuid4())
        L = self.label(source)
        meta = meta or {}

        msg = H(f"{ctx_id}|{data}|{L}|{source}|{meta}").encode()
        sig = self.signer.sign(msg)

        return SignedContext(
            id=ctx_id,
            D=data,
            L=L,
            src=source,
            meta=meta,
            sigma=sig
        )

    def verify_context(self, ctx: SignedContext) -> bool:
        msg = H(f"{ctx.id}|{ctx.D}|{ctx.L}|{ctx.src}|{ctx.meta}").encode()
        return self.signer.verify(ctx.sigma, msg)