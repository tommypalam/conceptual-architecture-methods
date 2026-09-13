# Perceptual stimulus competence check

Frozen before responses, 2026-09-13. This prerequisite addresses the independent
Claude design review: an incorrect visual judgment must not be mistaken for
conformity. It is part of scenario/structural validation, not the Phase 3 population
study, recognition probe or ethical-profile evaluation.

Create 18 line comparison PNGs and 18 colour comparison PNGs, each 512 by 384
pixels. Six reference examples per family each appear with the correct answer
at A, B and C. Line lengths are measured in pixels; screen millimetres are not
defined for a model input. Each colour target has an exact RGB match and two
distinct alternatives. Ground truth stays outside the request text. All images
have only Reference/A/B/C labels. Freeze image hashes and the Arial font hash.

Run each image once in a fresh request to gpt-5.4-mini-2026-03-17, temperature 1,
reasoning none, max output 64, image detail high. No peers, profile, normative
context, majority answer, research title or canonical experiment name is supplied.
N=36 independent calls, N=0 sampled profiles, config=null. Root seed 2026091305
fixes the shuffled schedule, not provider determinism. No outcome-dependent retries.

The engineering acceptance rule is **18/18 correct per family**. Any incorrect
answer remains in the data and blocks that family from immediate reuse. A malformed
response or API/integrity failure is preserved and stops dispatch. A correct set
does not establish equal psychological difficulty, human competence, invariance
across prompts/profiles, or conformity under group pressure. No inferential claim
about a population is made from this fixed stimulus set.

Budget: the complete schedule must reserve less than $0.20, inside the shared $2
structural-validation allocation and the $10/$30/$100 caps. Reserve the documented
high-detail image maximum of 2,500 patches times 1.2 (plus rounding margin), text
bytes, 1,024 framing tokens and 64 output tokens, at $0.75/$4.50 per million plus
10%. Settle at full uncached usage; unknown charges retain the reservation. One
nightly ledger also accounts for the preceding $0.0793452 Claude review.

Canonical context: Asch's 1955 account specifies 18 judgments with 12 incorrect-
majority critical trials. This prerequisite's 18 stimuli per family are newly
constructed diagnostic images; they are not claimed to reproduce his exact cards
or constitute a peer-pressure schedule. A later canonical sequence and its
modulators require a separate freeze; product colours remain a proposed alternative
domain requiring independent equivalence and recognition review.

Sources checked 2026-09-13:
- https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/Asch_1955_Opinions_and_social_pressure.pdf
- https://developers.openai.com/api/docs/guides/images-vision
- https://developers.openai.com/api/docs/models/gpt-5.4-mini

Synthetic review: Linden limits inference to perceptual competence; Osei separates
wrong perception from conformity; Tanaka requires all fixed-set results rather
than repeated attempts until success; Renna keeps normative profiles out of this
baseline; Okafor supports a sub-$0.20 check. Disagreement: equal exact-match accuracy
does not equate line and colour psychology. Resolution: passing permits further
stimulus review, not automatic variant equivalence or a human-validity claim.
