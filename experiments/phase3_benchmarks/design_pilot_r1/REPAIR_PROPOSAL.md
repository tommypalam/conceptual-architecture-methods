# Offline proposal: separate task wording from engine scheduling

Status: local proposal only. The generated original and independent revise verdict
remain unchanged. This proposal is neither reviewed nor released for paid testing.

## Participant-facing task text

Imagine two strangers are paired in a one-time, anonymous online task about dividing
100 identical research tokens, each worth the same to the recipient as to the
proposer. One person is the proposer and chooses an integer number from0 to100 to
offer the other person; the proposer keeps the remaining tokens. The other person
is the responder and chooses accept or reject. Acceptance implements the proposed
split. Rejection gives both people zero tokens. There is no prior entitlement,
later interaction, or ability to override rejection.

This retains the original candidate's allocation rule while removing its ambiguous
schedule sentence. It does not solve the separate problem of a minimally changed,
easily recognisable research-token setting.

## Engine-only role schedule, supplied separately to structural review

Each profile is used in exactly six isolated conversations, with no cross-role
history or other conversation's answer visible:

1. One proposer conversation: choose any integer offer to the other person from0
   through100. The proposer keeps100 minus that offer. The offer is not restricted
   to10,20,30,40 or50.
2. Five responder conversations: receive a fixed offer of10,20,30,40 or50 tokens,
   respectively. Accept implements that particular split; reject gives both zero.

The five fixed amounts are responder offers, not five proposer choices or share
pairs. The engine supplies the role and, for responders, that conversation's offer.
Response schemas and role isolation remain those of the frozen canonical kernel.

## Before future paid work

The next generator contract should return distinct task-text, role-instruction and
engine-metadata fields; an independent reviewer must assess all three together.
Recognition inputs must remain faithful to the actual proposed task and disclose
their information scope. Do not selectively hide diagnostic causal rules from the
judge or claim this formatting repair improves recognition without testing it.

The next runner should also validate both bare JSON and a complete JSON Markdown
fence before its source freeze, using the same strict semantic schema. Test both
forms, incomplete fences and surrounding prose offline; retain raw provider text.
This prospective parser fix must not overwrite the stopped runner or its records.
