from scp.core.types import ExecutionState, SignedInvocation
from scp.utils.hashing import H
from scp.policy.default_policy import DEFAULT_POLICY


class SCPRuntime:
    def __init__(self, sentinel, agent_pk, policy=None):
        self.sentinel = sentinel
        self.agent_pk = agent_pk
        self.policy = policy or DEFAULT_POLICY

    def new_session(self) -> ExecutionState:
        return ExecutionState(contexts={}, seq=0)

    def add_context(self, state: ExecutionState, ctx):
        if not self.sentinel.verify_context(ctx):
            raise ValueError("Invalid context signature")
        state.contexts[ctx.id] = ctx

    def verify_invocation(self, inv: SignedInvocation) -> bool:
        msg = H(
            f"{inv.id}|{inv.ctx_ids}|{inv.op}|{inv.args}|{inv.seq}|{inv.principal}"
        ).encode()
        return self.agent_pk.verify(inv.sigma, msg)

    def compute_label(self, state, ctx_ids):
        labels = [state.contexts[c].L for c in ctx_ids]
        return "C_low" if "C_low" in labels else "C_high"

    def execute(self, state: ExecutionState, inv: SignedInvocation):

        if not self.verify_invocation(inv):
            return {"status": "REJECTED", "reason": "Invalid signature"}

        if inv.seq != state.seq:
            return {"status": "REJECTED", "reason": "Bad sequence"}

        for cid in inv.ctx_ids:
            if cid not in state.contexts:
                return {"status": "REJECTED", "reason": "Unknown context"}

        L = self.compute_label(state, inv.ctx_ids)

        if L not in self.policy.get(inv.op, []):
            return {
                "status": "REJECTED",
                "reason": f"{L} cannot execute {inv.op}"
            }

        state.seq += 1
        return {"status": "ALLOWED", "label": L}