# Disposition of the independent Claude design review

The single cross-provider review completed for $0.0793452 (conservative usage
accounting including 10%). All five drafts were assessed as needing revision.
Raw output is preserved locally; the full derived review is in
canonical_audit_result.json. Offline replay produced zero new calls.

The review is advice from an LLM, not an authority or human sign-off. Its input
was the operational drafts, registry and erratum. It did not receive the whole
repository or retrieve source papers. Claims that something is absent refer only
to that limited packet unless independently verified below.

| Finding | Disposition and concrete action |
|---|---|
| Escalation events, prods and stopping rules need specification | Accepted. Preserve the 1963 remote-feedback condition separately from later voice-feedback variants; source extraction and exact implemented transition rules remain prerequisites. |
| Perceptual images and no-peer competence are missing | Accepted and addressed by the separately frozen perception_20260913 check. Pixel geometry and RGB ground truth stay outside model text. |
| At least six images and millimetre equivalents should be used | Six reference examples per family are useful for the engineering screen. Millimetre equivalents are inapplicable without a defined physical display; use measured pixels and image hashes. |
| Trial count and counterbalancing need definition | The newly accessed Asch 1955 primary account specifies 18 trials, 12 critical. The no-peer screen uses new stimuli, not an invented reproduction of the historical cards. A peer-pressure schedule still needs its own freeze. |
| Justice high/low labels are inverted | The reviewer conflates high **predicted response rate** with the Justice axis. The spec explicitly predicts higher rejection in Justice=0. Keep that pre-data hypothesis visible; do not reverse it to fit intuition or later outcomes. Exact context wording and rationale still need review. |
| Freedom contrast is internally inconsistent | Rejected as stated: holding Authority=1 while changing Freedom=0 to 1 is an internally consistent isolation contrast. Its predicted direction is a hypothesis about context, not a rename or reversal of an individual parameter. |
| UG roles and outcome denominators need separation | Accepted. Separate fresh conversations for proposer and each offered responder share; report conditional 20% rejection separately from mean offer and any threshold estimate. |
| Bystander paradigm/window must be selected | Accepted. Smoke and seizure paradigms cannot be pooled; an individual intervention probability differs from the probability that anyone in a group helps. |
| Reactance adjacency, restriction and control must be defined | Accepted. Keep the proposed binary endpoint distinct from ranking change; no unsupported conversion from standardized effect to probability difference. |
| Impossible choices should be excluded from the denominator | Not adopted. Preserve invalid choices and their original assigned denominator; freeze invalidity handling and bounds instead of silently dropping records. |
| Missing modulators in the other three benchmarks are necessarily blockers | Not adopted as a new requirement. Spec section 7.5 mandates additional modulator retrodiction for Milgram and Asch. Other benchmark-specific conditions still need explicit procedures. |
| Recognition procedure is absent | It was not in the review input. The existing protocol requires 500 judge calls, two raters, adjudication and a greater-than-30% rejection threshold for alternatives. Do not remove that requirement based on the review. |
| A new no-peer Milgram baseline is mandatory | Treat as a suggested control, not an existing spec requirement. Additional controls must be justified and costed prospectively. |
| Freeze individual text strings before all other work | Not adopted as a workflow restriction. Complete mutually dependent scenario, state and analysis definitions together before release. |

The source-to-measure corrections remain valid. The review does not validate any
human rate, canonical/alternative pair or population collector. Its status is a
design-readiness result, not failed ethical encoding or a failed human benchmark.

Primary source newly inspected:
https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/Asch_1955_Opinions_and_social_pressure.pdf
