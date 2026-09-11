"""Optional, fixed-specification delivery. No sampling or behavioural rules.

This module has no dependency on the simulation engine or provider SDK. The
caller binds one immutable specification to one decision; the model cannot
select a profile, change a number, or request a redraw.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Specification:
    text: str
    sha256: str

    def __post_init__(self):
        if not self.text or sha256(self.text.encode('utf-8')).hexdigest() != self.sha256:
            raise ValueError('Specification integrity mismatch')


class SpecificationProvider(Protocol):
    """Repeated reads return the same immutable, prevalidated specification."""
    def read(self) -> Specification: ...


@dataclass(frozen=True)
class FixedSpecificationProvider:
    specification: Specification

    def read(self) -> Specification:
        return self.specification


class JsonSpecificationProvider:
    """Read a caller-selected, hash-pinned file once, then serve its snapshot."""
    def __init__(self, path: Path, expected_file_hash: str):
        raw = path.read_bytes()
        if sha256(raw).hexdigest() != expected_file_hash:
            raise ValueError('Specification file mismatch')
        self._specification = Specification(**json.loads(raw))

    def read(self) -> Specification:
        return self._specification


BRIDGE = (
    'You are participating in a decision-making simulation. '
    'Call read_agent_specification before making your decision. '
    'Its result is your assigned decision-making specification, including your '
    'profile, normative context, and task instructions. Apply that specification '
    'to the decision and follow the response format in the user message.'
)


def tool_schema():
    return {'type': 'function', 'function': {
        'name': 'read_agent_specification',
        'description': 'Read the fixed decision-making specification assigned to this agent.',
        'strict': True,
        'parameters': {'type': 'object', 'properties': {}, 'required': [],
                       'additionalProperties': False}}}


def tool_result(provider: SpecificationProvider, name: str, arguments: str) -> str:
    if name != 'read_agent_specification' or json.loads(arguments) != {}:
        raise ValueError('Unexpected tool call; no execution or profile substitution')
    return provider.read().text


def decision_messages(initial: list, assistant: dict, provider: SpecificationProvider) -> list:
    calls = assistant.get('tool_calls') or []
    if (assistant.get('role') != 'assistant' or len(calls) != 1
            or assistant.get('content') not in (None, '') or assistant.get('refusal')):
        raise ValueError('Expected one tool call without an early answer')
    call = calls[0]
    if call.get('type') != 'function' or not call.get('id'):
        raise ValueError('Invalid function call')
    content = tool_result(provider, call['function']['name'], call['function']['arguments'])
    # Keep the actual returned call/arguments/ID; do not fabricate a model turn.
    turn = {'role': 'assistant', 'content': assistant.get('content'), 'tool_calls': calls}
    if len(json.dumps(turn, ensure_ascii=False).encode('utf-8')) > 1024:
        raise ValueError('Tool-call framing exceeds frozen 1024-byte bound')
    return [*initial, turn, {'role': 'tool', 'tool_call_id': call['id'], 'content': content}]
