    
code 
    
```python

    from scp.crypto.ed25519 import Ed25519Signer
    from scp.sentinel.sentinel import Sentinel
    from scp.runtime.runtime import SCPRuntime
    from scp.core.invocation import SignedInvocation
    
    # Setup
    ctx_signer = Ed25519Signer.generate()
    agent_signer = Ed25519Signer.generate()
    
    sentinel = Sentinel(ctx_signer)
    runtime = SCPRuntime(sentinel)
    
    state = runtime.new_session()
    
    # Ingest external document (LOW)
    doc_ctx = sentinel.ingest("malicious instruction...", "drive")
    runtime.add_context(state, doc_ctx)
    
    # Agent proposes action
    inv = SignedInvocation(
        ctx_ids=[doc_ctx.id],
        op="send_email",
        args={"to": "attacker"},
        seq=state.seq,
        principal="agent",
        signer=agent_signer
    )
    
    # Execute
    result = runtime.execute(state, inv)
    print(result)
```


