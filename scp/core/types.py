from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class SignedContext:
    id: str
    D: str
    L: str
    src: str
    meta: Dict[str, Any]
    sigma: bytes


@dataclass
class SignedInvocation:
    id: str
    ctx_ids: List[str]
    op: str
    args: Dict[str, Any]
    seq: int
    principal: str
    sigma: bytes


@dataclass
class ExecutionState:
    contexts: Dict[str, SignedContext]
    seq: int