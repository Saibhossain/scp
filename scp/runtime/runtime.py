from scp.core.state import ExecutionState


class SCPRuntime:
    def __init__(self, sentinel):
        self.sentinel = sentinel

    def new_session(self):
        return ExecutionState()

    def add_context(self, state, ctx):
        state.contexts[ctx.id] = ctx

    def execute(self, state, invocation):
        allowed, result = self.sentinel.authorize(state, invocation)

        if not allowed:
            return {
                "status": "REJECTED",
                "reason": result
            }

        state.seq += 1

        return {
            "status": "EXECUTED",
            "label": result,
            "op": invocation.op
        }