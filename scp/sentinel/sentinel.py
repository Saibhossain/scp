from scp.core.context import SignedContext
from scp.core.policy import Policy, C_HIGH, C_LOW
from scp.core.composition import compose_labels


class Sentinel:
    def __init__(self, context_signer):
        self.context_signer = context_signer
        self.policy = Policy()

    def ingest(self, data, source):
        label = C_HIGH if source == "user" else C_LOW
        return SignedContext(data, source, label, {}, self.context_signer)

    def authorize(self, state, invocation):
        # Verify invocation
        if not invocation.verify():
            return False, "Invalid invocation signature"

        # Sequence check
        if invocation.seq != state.seq:
            return False, "Sequence mismatch"

        labels = []

        for cid in invocation.ctx_ids:
            if cid not in state.contexts:
                return False, "Unknown context"

            ctx = state.contexts[cid]

            if not ctx.verify():
                return False, "Invalid context signature"

            labels.append(ctx.L)

        L = compose_labels(labels)

        if not self.policy.allowed(invocation.op, L):
            return False, f"Policy violation: {L} cannot call {invocation.op}"

        return True, L