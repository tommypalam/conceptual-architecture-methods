# CLAUDE.md — Concepts-as-Architecture Project Constitution

## Paper publication revision (2026-09-23)

The live paper on `paper-20260922` is now *Which Part of a Prompt Carries
Behaviour?*, built from `docs/paper/paper_draft.md` to
`docs/paper/arxiv/preprint.pdf`. See `docs/paper/REVISION_20260923.md` for the
verified correction record and `docs/paper/arxiv/SUBMISSION.md` for the local
publication package. No submission or remote publication has been performed.

For this paper, distinguish a verified PD field contribution from attribution
of the whole profile effect. CANON-minus-FLIP was prespecified in the frozen
semantics protocol; its item-level robustness checks were post-hoc. The floor-lift
test returned mixed and does not establish PD as a pure status-quo construct.
AW was pinned in the later paper evidence; the thesis's earlier statement that
it was never pinned remains correct for the submitted document. No frozen
evidence or thesis file was changed. All 36 stored robustness results reproduce
exactly offline. The user's next research direction is open models, but no new
collection or spend is authorised by this publication revision.

## Project reorganised around the submitted thesis (2026-09-19, evening)

**The thesis is `docs/thesis/LF3262767.pdf`. It is the single canonical PDF.** The
byte-identical twin `docs/thesis.pdf` was removed so there is exactly one thesis
file. Everything about the thesis now lives in `docs/thesis/`.

| Was | Is |
|---|---|
| `docs/LF3262767.pdf`, `docs/thesis.pdf` | `docs/thesis/LF3262767.pdf` (twin removed) |
| `docs/thesis.md` | `docs/thesis/thesis.md` |
| `docs/thesis_abstract.txt` | `docs/thesis/abstract.txt` |
| `docs/figures/` | `docs/thesis/figures/` |
| `docs/thesis_build/` | `docs/thesis/build/` |
| `docs/thesis_BACKUP_pre_edits_20260916.md` (untracked) | `docs/thesis/history/thesis_20260916_pre_edits.md` (tracked) |
| `docs/paper_draft.md`, `docs/citation_verification.md` | `docs/paper/` |
| `docs/publication_2026091*.md` | `docs/publications/` |
| `docs/NEXT_CHAT_HANDOFF.md`, `docs/desktop_handoff.md`, `docs/desktop_transfer.json` | `docs/handoffs/` |

**The PDF was MOVED, never rebuilt.** Its SHA-256 is
`52df1c5aa6201cc12a53f06a7dd868826c4367b36b530228efa36a16119ff1a3` before and
after, matching the recorded verification. **Rebuilding changes the bytes even
when the text is identical, so do not rebuild a copy that has been submitted.**
The relocated build was proven by building to a dummy filename
(`-StudentId 0000000`), comparing extracted text page by page against the real
PDF - 35 pages, identical on every one - and deleting the test file.

**What may NOT be moved, and why - these are rules, not leftovers:**

  - **Nothing in `code/` is renamed or moved.** 109 of its 271 modules are
    SHA-256-pinned by the frozen release chain and import one another by flat
    module name. `code/README.md` now maps each thesis result to its design
    module, collector, evidence folder and offline analysis instead. After this
    reorganisation all 195 pinned sources were re-checked: present and
    byte-identical.
  - **Seven documents stay at the top of `docs/`** - `abstract.md`,
    `variables.json`, `project_layout.md`, `pre_analysis_plan.md`,
    `phase1_5_results.md`, `research_programme.md` and the two `phase1_5_*`
    redirect stubs - because frozen reports in `archive/` and `experiments/` link
    to those exact paths and frozen reports are never edited. Inbound links were
    counted before anything moved; only files with ZERO frozen references moved.
  - `archive/`, `experiments/` and `prompts/` were not touched.

**Several pinned collectors carry a WRONG first docstring line** ("Prospective PD
discriminant test on crossed no-clean-hands dilemmas"), inherited from the module
they were adapted from: `phase5_coordinate_sweep_r2.py`,
`phase5_label_semantics_r1.py` and `_r2.py`, `phase5_pd_prospective_r1.py`. They
cannot be corrected without breaking `verify()`. The file name and its design
module are authoritative. **Do not "fix" these docstrings.**

**Moving a file silently breaks relative links.** The moves broke 46 of 293
relative links in the live documents and nothing would have reported it.
`tests/check_doc_links.py` found every one, attributed each to a specific move,
repaired them, and found zero that were NOT explained by a move - so the live
documents had no broken links beforehand. It now checks 339 and passes. **Run it
after moving or renaming any document.** It deliberately skips frozen areas: a
dead link inside a frozen report is part of the record, not a defect.

**The verifier was brittle across pypdf versions, and is hardened.** It failed on
the marker `no finite SE` although the PDF was byte-identical to the verified
one. Not a ligature: pypdf 6.19 extracts that phrase from a tightly kerned
compact-type table cell as `nofinite SE`. Marker matching now strips whitespace
from both sides - every character must still be present and in order. It also
asserts that `docs/abstract.md` contains the portal abstract verbatim, replacing
the removed twin-PDF identity check, so the two abstracts cannot drift. Every
measured property of the PDF matched the recorded run exactly.

**Two stale passages in the root README contradicted the thesis and the
README's own table**: that ID "passed" its swap control and is "the second of ten
coordinates whose label carries its effect", and that "AW is a label and it is
inert". Both were the withdrawn significance-versus-non-significance inference.
Corrected to the direct test (ID +0.064 [-0.014, +0.146]; PD +0.375
[+0.286, +0.464]). The README, `docs/README.md` and the thesis now state the same
boundary.

**Previously untracked work is now tracked, unmodified**: the thesis explorer
(`viewer/explore.*`, `viewer/thesis-evidence.json`, `viewer/EXPLORER_DESIGN.md`,
`code/build_thesis_explorer.py`, `code/open_visualiser.ps1`,
`tests/check_thesis_explorer.cjs`) and `code/phase3_crossmodel_pilot_images.py`.
The explorer reflects 15 September data; its evidence file makes no headline
coordinate claims, so it is dated rather than wrong. The one unrecoverable file
was the thesis backup, which matched no version in git history (closest 99.2%).

No experiment, frozen record, result, figure or analysis changed. No API call.
Accounting unchanged: Claude $22.247448300/$32, OpenAI $12.741596175/$40,
package $34.989044/$100.

## Bocconi submission revision (2026-09-19)

The researcher confirmed that **Prof. Arnaldo Camuffo is the sole supervisor**.
The README has been corrected. `docs/thesis/thesis.md` is now the concise submission
source; the current abstract is `docs/thesis/abstract.txt` (also in
`docs/abstract.md`). The upload artifact is `docs/thesis/LF3262767.pdf`, the single canonical
thesis PDF. See `docs/thesis/build/COMPLIANCE.md` for the university rules,
changes and verification.

Objective corrections: the GPT E/G/U comparison used eight items and 320 pairs;
later GPT coordinate studies used seven. Appendix B now contains all nine unique
items, including `sample_draw`. The PD swap included TRUE arms. Independent
background sampling does not establish robustness to the copula. Power does not
guarantee detection, and the six equivalence bounds are post-hoc, individual
unit-bootstrap bounds conditional on the tested items. The full slope refit has
16 contrasts, 15 usable standard errors and two ID disagreements; PD swap TRUE
has no usable slope-model standard error. No experiment, frozen result, analysis
module or figure was changed, and no API call was made.

The submission PDF follows the 2025–26 undergraduate rules: four unnumbered
opening blank pages; no title page, student details or abstract; A4, 12-point
Arial body, 2.5 cm side margins and approximately 29 body lines per full page.
Tables, captions and verbatim materials use compact type. Abstract and title
information belong in the portal separately. The previous layout's page counts
and supervisor discrepancy below are historical and superseded.

## Consistency pass after the second review (2026-09-19, later)

Seven leftovers from the supervisor's second round, all wording, all applied:
"inert" is retired outside §7.4 (use "partner field", qualified); §5.4 now says
the analyses DO disagree on ID and that this changes ID's reading; the PD
slope-model sentence carries the PD swap TRUE exception explicitly; §6 says "no
effect is detected relative to the unprofiled baseline"; the conclusion no
longer says "two parameters survived" or "signature of a genuine label effect";
"position-independent" became "persists at both tested positions" because
position modulates magnitude; the blank page after the abstract is gone
(`\clearpage`, rule removed). **Rule for future edits: abstract, §5.4, §8.1
and §11 must state the same boundary: PD verified, ID candidate, LL withdrawn
and unresolved, AW never pinned.**

## Reviewer round: ID demoted to a candidate; PD verified under every test (2026-09-19)

A supervisor review raised four methodological points. All were correct and all
were answerable offline, zero API calls (`code/phase6_review_tests.py`,
`code/phase6_mixed_slopes.py`, output `experiments/phase5_analysis/review_tests.json`).

**1. Random intercepts do not address treatment-effect heterogeneity.** A crossed
model with a random slope of condition by item was written, validated on
simulated data, and fitted to every primary contrast plus E-G and the sweep's
ID/LL rows. **Twelve of fourteen agree with the sign test; the two that do not
are both ID**: swap TRUE p 0.0033 -> 0.061, cross-provider 0.0330 -> 0.095.
PD swap TRUE returned no finite SE from four starts (seven items, near
saturation); it rests on the sign test, bootstrap and intercept model.

**2. Significant TRUE beside non-significant SWAP is not a test of the
difference** (Gelman and Stern). The within-unit difference of differences was
computed for every swap. **PD: +0.375 [+0.286, +0.464], p ~ 0, 6+/1-. ID: +0.064
[-0.014, +0.146], sign p = 0.149, 3+/2-.** ID's field binding is NOT
established. The earlier reading "null - the label carries it" was the
significance-versus-non-significance inference and is withdrawn.

**3. The designs isolate the labelled AND GLOSSED field, not the label string.**
Every entry moves with its two-line gloss. "Label" now means the pair
throughout; separating name from gloss is future-work item two.

**4. Headline sentences overreached** in four places, all fixed: "detects its own
false positives" -> "exposes its own unconfirmed findings"; the deterministic
baseline makes detection one-directional, not impossible; E > G is over this
instruction on these items; §7.7 "better aggregate outcome" contradicted the
tied totals. Also fixed: §7.3 said the cross-provider runs used the swap (they
pinned only); the final map bounded "seven others" when AW was never pinned;
the abstract claimed every headline contrast was refitted while E-G were blank
(now refitted: gpt +1.199, haiku +1.010 under intercepts).

**The headline is now ONE of ten verified (PD), one candidate (ID), six
bounded below 0.20, one withdrawn (LL), one never pinned (AW).** This is a
demotion the project's own method demanded. Do not restore "two of ten".

Two references were added at the reviewer's citation: Barr et al. 2013 (JML
68(3):255-278) and Gelman & Stern 2006 (Am. Stat. 60(4):328-331). Both are
standard and written from knowledge; tick them in `docs/paper/citation_verification.md`.

Accounting unchanged.

## Thesis rebuilt for submission: intervals, equivalence bounds, figures, verbatim prompts (2026-09-19)

Work on branch `thesis-final-20260919`, zero API calls, no frozen record touched.
`docs/thesis/thesis.md` was rewritten and `docs/thesis.pdf` rebuilt with a reproducible
toolchain (`docs/thesis/build/build.ps1`; pandoc from RStudio's quarto, xelatex from
TinyTeX installed this session). **Body is 24 pages (numbered 4-27) plus 2 appendix
pages**, inside the researcher's 30-page bound excluding references.

**What was added, all from the frozen records** (`code/phase6_thesis_intervals.py`,
`code/phase6_thesis_figures.py`, output `experiments/phase5_analysis/thesis_intervals.json`):

  - Paired bootstrap 95% intervals over agent-item units for every headline contrast,
    plus a two-stage item-cluster bootstrap. Point estimates reproduce every published
    figure exactly. **Under the item-cluster bootstrap every PD contrast keeps its sign;
    the ID contrasts and the haiku E-G contrast include zero.** The mixed model keeps
    all three significant. The thesis states ID at that strength.
  - Equivalence bounds for the sweep's nulls: the smallest symmetric margin containing
    the 90% interval. All six non-LL nulls certify |effect| < 0.20; only RT and CS
    certify < 0.10. **TfA (-0.103) and MoR (-0.097) have uncorrected intervals that
    exclude zero**; they did not survive Holm and nothing is claimed, but "not
    load-bearing" for them means "below the certified threshold", not "flat". This was
    future-work item five and is now in §7.5 as a post-hoc analysis.
  - Four figures (E/G/U on both models; label vs position; sweep forest with bands;
    replication map across designations and providers).
  - The full E-arm system prompt for a real agent, its one-line diff, and the G
    instruction verbatim (§5.2); all eight items in Appendix B. The thesis no longer
    depends on the paper draft for its materials.
  - A "framework as designed vs exercised" table (§2.4); §1.1 rewritten to motivate the
    identification question rather than only the framework.

**Defects fixed**: the stale "position not excluded" paragraph in §3.3 that contradicted
the next paragraph; "von von Oswald"; "Three readings" listing four; 44 vs 45 studies;
two wrong cross-references (§7.3 for the sweep, §7.5 for the survivors); five
bibliography entries never cited in the body were removed (Kojima 2022, Nam 2025,
Wang 2026, Yang 2026, Wei 2021).

**Not changed, needs the researcher**: README names "Dr. Abhinav" as supervisor and
Camuffo as co-supervisor; the title page names Camuffo alone. One is wrong. The
explorer files (`viewer/explore.*`, 15 Sept) are untracked and reflect older data.

Accounting unchanged: Claude $22.247448300/$32, OpenAI $12.741596175/$40, package
$34.989044/$100.

## Position excluded: the effect is LABEL-bound, not line-bound (2026-09-18)

`position_counterbalance_r1` closed the last structural alternative to the
label-semantics reading. 2,241 calls, 2,240/2,240 valid, zero failures, $1.656796.
Review accept, zero blocking issues.

**The confound a reviewer identified.** In the rendered block PD is line 6 and AW
is line 10, so `label_semantics_r1`'s swap moved the label AND its position
together. A primacy effect over a numbered list would have produced its entire
result (+0.339 / -0.036) with no label reading. **This was a genuine gap in our
own claim, not a technicality, and it went unnamed until raised.**

**The 2x2**, crossing binding with line order, 40 agents x 7 items x 8 cells:

| Cell | Level on | At line | Effect | Holm | Items |
|---|---|---:|---:|---:|---|
| **A** | **PD** | **6** | **+0.393** | **~0** | **7+/0-** |
| **C** | **PD** | **10** | **+0.271** | **~0** | 5+/1- |
| B | AW | 10 | +0.061 | 0.157 | 6+/1- |
| D | AW | 6 | +0.004 | 1.000 | 3+/2- |

**LABEL factor +0.300. POSITION factor +0.032.**

**Cell D is the decisive one:** level at line 6 - the privileged position under any
primacy account - on the inert label, giving +0.004. Keep the label and move it
four lines down (C) and the effect survives at +0.271.

**Position is small, NOT zero.** The position contrast is +0.032 and A exceeds C by
+0.122, so a modest position component may ride on the label effect. Roughly an
order of magnitude smaller; does not account for the finding. **Do not round it to
"position is irrelevant".**

**Three of four candidate mechanisms are now excluded**: block presence and
verbosity by construction, free-floating extremity by the original swap, position
by this designation. **Field-weighted extremity remains, and no design in this
project separates salience from label semantics.**

**Scope limits that must NOT be silently inherited.** This counterbalanced PD on
GPT ONLY. `pd_crossmodel_r1` and `id_crossmodel_r1` ran no counterbalance, so
their claims stay at *field-bound* - label-plus-position. ID's swap control
(`label_semantics_r2`) carries the same position confound, unaddressed. And a
label-bound effect is still NOT semantic understanding.

**An invariant that earned its place.** `phase5_position_render.verify_render()`
requires that reordering by the IDENTITY permutation return the input
byte-for-byte. It failed on the first implementation: the template pads every
entry with a leading space including entry 10, so the periods align, and the first
version stripped it. Numeral multiset, line count, value and gloss preservation
all passed - only the identity test caught it. **When transforming a frozen
format, test the no-op.**

**A provenance guard fired and was obeyed.** `prepare()` refused with "Frozen
continuation source changed": the 18 September name removal had edited one
docstring line in `code/utils.py`, pinned by every release built on it. **The
pinned bytes were restored rather than the check loosened** - the guard cannot
distinguish a comment from a logic change, which is what makes it worth having.
`code/utils.py` therefore keeps the retired name in one docstring, a deliberate
exception on the same footing as the frozen archive files. **Do not "fix" it.**

Accounting: Claude $22.247448300/$32, OpenAI $12.741596175/$40, package
$34.989044/$100. Usage estimates, not verified provider balances.

## Phase 6 begun: paper drafted; name retired; repository consolidated (2026-09-18)

**The project name was retired** at the researcher's instruction. Live documents
now use **Concepts as Architecture**, with the full title - *Concepts as
Architecture: A Probabilistic Framework for Encoding Political-Ethical Concepts
in Normative AI Agents* - where a title belongs.

**Deliberately NOT renamed, and this is a rule rather than an oversight:**
`archive/**` (9 files) and five frozen `experiments/**` assessments keep the old
name. They are historical evidence; rewriting a dated closure document to remove
a name it actually used would make the record misdescribe what was written at the
time. `viewer/**` was excluded at the researcher's request, and four references
to `paria_desktop_data_20260912.zip` are a real filename inside copy-paste
commands. **Do not "finish the job" by editing frozen records.**

**Repository consolidated to `main` plus numbered backups.** Zero non-backup
branches on either side. `research-transfer-design-20260913`, previously named in
this file as the development branch, is retired to `backup-9` (remote) and
`backup-13` (local); three older local dev branches became `backup-10` to
`backup-12`. All were verified merged into HEAD first. **There is no development
branch: cut one before the next substantive work.**

**A paper draft exists** at `docs/paper/paper_draft.md`, framed as an identification
problem rather than an architecture writeup:

> *Which Parts of a Prompt Carry Behaviour? Label-Semantic Controls for
> Parameterised LLM Agents*

Ten sections and three appendices. It leads on the claim that four mechanisms -
label semantics, block presence, verbosity, numeric extremity - produce the same
observed behaviour change, and that the one-binding swap separates them. **The LL
withdrawal is positioned as the central result**, not the successes: a method
that can only confirm is weaker than one that kills its own findings.

**Every headline figure was verified against its `results.json`** while drafting,
which caught one error in the draft itself: a claimed 19,231 total calls against
a true **18,750** (the PD run had been double-counted). Verified correct: both
E/G/U pairs, PD prospective, both swap controls, the permutation control, and the
AW inertness figures.

**What drafting exposed, in priority order.** These are the paper's real
weaknesses and should drive any further collection:

  1. **Coverage is the principal limitation** - seven items on one model, six on
     the other, all workplace-resource vignettes with identical tied payoffs.
     No rewording fixes it. It is the venue critique's unaddressed second option.
  2. **Section 9 (Related Work) is WRITTEN, with citations supplied by the
     researcher's literature search on 18 September, but NOT VERIFIED.** The
     checklist is `docs/paper/citation_verification.md` and it must be worked through
     in a session with database access. Verify not only that each paper exists
     but that it makes the claim attributed to it - a real paper cited for the
     wrong finding is worse than a missing citation. **Do not remove the
     citation-status banner at the top of the section until every row is
     checked.** Still: do not fabricate citations, and do not add any the search
     did not supply.
  3. **"Not verified cross-model" appears three times** and is awkward each time.
     Swap controls on haiku (~$2.50) would delete all three hedges.
  4. **The configuration counterfactual's absence is conspicuous** once the setup
     explains the framework names it as the contamination discriminator.

**The thesis is a condensed version of the paper**, 30 pages maximum, per the
researcher. The paper is primary and has no page ceiling; the thesis compresses
a finished document rather than being written separately.

Accounting unchanged by this session's work: Claude $22.238957400/$32, OpenAI
$11.093290725/$40, package $33.332248/$100.

## Both load-bearing coordinates replicate on a second provider (2026-09-18)

`id_crossmodel_r1` and `pd_crossmodel_r1` pinned each verified coordinate to its
endpoints on `claude-haiku-4-5-20251001` over haiku's six dispersing items,
40 agents, nine other coordinates drawn once per agent and held identical. 481
calls each, 480/480 valid, zero failures, $1.266 and $1.245.

| Coordinate | gpt | haiku | p (haiku) | Items | Prediction |
|---|---:|---:|---:|---|---|
| **PD** Procedural Dependence | **+0.346** | **+0.133** | **0.00031** | 4+/1- | **one-sided, theory-derived** |
| **ID** Internalisation Dependence | +0.111 | **+0.075** | **0.0328** | 4+/2- | two-sided, descriptive |

**The coordinate-level result is no longer single-model.** That was the sharpest
scoping limitation on the coordinate map and it is removed.

**PD's is the stronger test.** Its direction was locked ONE-SIDED from the
coordinate definition before collection, and the derivation's premise - on every
item the option keeping the stated arrangement classifies `good` - is a property
of the ITEM SET, not the coordinate. `verify_direction()` re-checked it against
haiku's six items and GATED prepare(). Only the direction transferred from gpt,
never the magnitude.

**Both effects SHRINK on haiku**: PD to ~38% of its gpt effect, ID to ~68%. What
replicates is the direction and the decision rule. **Do not claim magnitude
stability across models.**

**Neither is verified cross-model.** Verification on gpt required the
numeral-identical swap control; no swap control ran on haiku, because a four-arm
design quadruples the Holm family and an underpowered TRUE arm would make the
SWAP arms uninterpretable by construction - the LL outcome, induced by design.
These license "the coordinate moves the outcome on haiku too" and nothing more.

**A correlation pointed at nothing and the manipulation found something.** PD's
post-hoc correlation on haiku was +0.089, near flat, and this project described
PD as "flat on haiku" on that basis. Pinned, it gives +0.133 at p=0.0003. LL ran
the other way: correlation +0.271, manipulation negative then null. **Post-hoc
correlations mislead in BOTH directions**; only manipulation settles a
coordinate.

**Item sets differ by model and that is forced.** Five of six haiku items overlap
gpt's seven; `ward_transfer` is haiku-only, `on_call` and `rest_break` gpt-only.
`haiku_screen_r4`'s six alternatives all returned modal share 1.00 - fully
deterministic, unable to show any arm difference.

**pd_crossmodel_r1's review returned REVISE**, advisory under the 16 September
amendment. Finding 1 (tied payoffs) describes the design correctly and reads it
as a defect: totals are tied at -3 deliberately so welfare-maximisation, minimax
and best-case are indifferent by construction. Finding 2 (`tool_library` carries
ownership+contract weight the other items lack) has a real point - and that item
is the ONE with a negative effect, so removing it strengthens the result to
+0.170. **All six items are reported as primary**; dropping one after seeing
results would be outcome-driven selection. These items have now been reviewed
five times: four accepts with zero blocking issues, one revise, on byte-identical
material.

**The empty-analysis defect is FIXED AT SOURCE.** `coordinate_sweep_r2` and
`id_crossmodel_r1` both set SCREEN_N=0 and then derived an empty usable-task list
from the absent screen, so every contrast returned None and both needed offline
rescoring. `pd_crossmodel_r1` carries a `declared_tasks()` fallback, verified
against an empty list before collection, and produced its own analysis. **A
defect diagnosed once must be fixed in the next collector built on it, not
rescored again.**

Accounting: Claude $22.238957400/$32, OpenAI $11.093290725/$40, package
$33.332248/$100. Usage estimates, not verified provider balances.

## Verified coordinate map: TWO of ten are label effects; LL withdrawn (2026-09-17)

`label_semantics_r2` ran the swap control for ID and LL at 40 agents - 2,241
calls, 2,240/2,240 valid, zero failures, Holm over all four contrasts as one
family. For an active coordinate A and the inert partner AW, TRUE puts the level
on A's label and SWAP puts the same numeral on AW's, so the blocks are
**numeral-identical** and only the label binding differs.

| Contrast | Effect | Holm | Items | Reading |
|---|---:|---:|---|---|
| **ID:TRUE** | **+0.111** | **0.00467** | 5+/1- | replicates the sweep |
| ID:SWAP | +0.046 | 0.408 | 5+/2- | **null - the label carries it** |
| LL:TRUE | **-0.014** | **0.708** | 4+/3- | **fails to replicate** |
| LL:SWAP | -0.046 | 0.408 | 1+/4- | uninterpretable, nothing claimed |

**The verified map:**

| Coordinate | Pinned effect | Swap control | Status |
|---|---:|---|---|
| **PD** Procedural Dependence | **+0.339** | **-0.036, n.s.** | **verified label effect** |
| **ID** Internalisation Dependence | **+0.111 to +0.143** | **+0.046, n.s.** | **verified label effect** |
| ~~LL Legitimacy Locus~~ | -0.131 then -0.014 | uninterpretable | **not replicated - WITHDRAWN** |
| TfA, MoR, MS, RE, RT, CS, AW | -0.10 to +0.05 | - | not load-bearing |

**Two of ten, not three.** `coordinate_sweep_r2`'s LL row is superseded and that
assessment carries a superseding note. Its data and its seven nulls stand.

**LL gave three different answers across three measurements: +0.271 post-hoc,
-0.131 pinned at 25 agents, -0.014 pinned at 40.** Positive, negative, null.
**This is not a power failure** - it failed on the LARGER sample, with power
17/20 at an effect of 0.131. **LL is unresolved, not inert**: it failed to
replicate, which is not the same as being measured flat. LL was NOT carried into
the cross-model runs; only PD and ID were. Do not describe LL as
load-bearing, and do not describe it as demonstrated inert.

**The replication gate is what caught it.** Had the swap control been run without
a TRUE arm, LL's null SWAP would have read as "the label carries it". Every swap
control must carry a TRUE arm that reproduces the effect it claims to explain.

**A bug caught before collection.** The first population draw gave agent 7
AW=0.102, which renders as "0.10" at the block's two decimals and **collides with
the LOW level**, making that agent's TRUE and SWAP byte-identical. The degeneracy
check tested the raw draw, not rendered precision. It now tests **rendered
precision and blocks**. The seed was changed before any call, on a property of
the draw alone. Test degeneracy at the precision that reaches the wire.

Accounting: Claude $19.728369100/$32, OpenAI $11.093290725/$40. Usage estimates,
not verified provider balances.

## Coordinate map as first measured, before verification (2026-09-17)

> **LL's row below is SUPERSEDED** by the swap control above: LL measured
> -0.014 at Holm 0.708 at 40 agents and is withdrawn. ID's row replicated
> and is now verified as a label effect. Kept as the record of what the
> sweep measured, and of the sign-reversal finding, which stands.

`coordinate_sweep_r2` pinned each coordinate to 0.1 and 0.9 with the other nine
drawn and held identical - 2,801 calls, 2,800/2,800 valid, zero failures, Holm
over all eight contrasts as one family. With PD and AW from `label_semantics_r1`:

| Coordinate | Effect | Holm | Items | Load-bearing |
|---|---:|---:|---|---|
| **PD** Procedural Dependence | **+0.339** | ~0 | 6+/1- | **YES** |
| **ID** Internalisation Dependence | **+0.143** | **0.00056** | 6+/1- | **YES** |
| **LL** Legitimacy Locus | **-0.131** | **0.00082** | **0+/6-** | **YES** |
| TfA, MoR, MS, RE, RT, CS, AW | -0.10 to +0.05 | n.s. | | no |

**Seven are not load-bearing** - a Holm-corrected null at adequate power (24/24
simulated at d>=0.20, 0/24 false positives), not absence of evidence.

**A methodological finding.** LL's post-hoc correlation and its manipulated
effect have OPPOSITE SIGNS: Phase 5's integrated analysis measured LL at r=+0.271
on the unmanipulated E arm; pinning LL to its endpoints gives -0.131. ID agrees
in sign; LL reverses. This is a concrete demonstration of why the Phase 2
reanalysis insisted post-hoc coordinate findings need prospective test before
confirmatory language.

**That distinction was the right one, and the swap control has since been run**
(see the verified map above). ID survived it; LL did not replicate.

Two operational notes recorded: `coordinate_sweep_r1` halted at 689/2801 on a
network TimeoutError and that slot is preserved unresolved and never retried, its
689 calls ($0.55) not reused; and r2's collector produced an EMPTY analysis
because dropping the screen arm left its usable-task list empty, corrected
offline in `code/phase5_sweep_rescore.py` rather than in the hash-pinned
collector.

Accounting: Claude $19.719300700/$32, OpenAI $9.446089125/$40.

## Provider ceiling amendment: OpenAI $40 (2026-09-17)

The researcher raised the OpenAI provider ceiling from $30 to **$40** to fund the
full coordinate sweep, stating: *"ill up the budget one last time as much as its
needed... but lets try to reduce cost and optimise as much as possible."*

Spent at the time of this amendment: $6.868692600, leaving $33.13 of headroom.
The sweep reserves $32.56 worst case.

The **$100 package cap is unchanged** and remains enforced, as does the $32
Anthropic ceiling. Cumulative totals do not reset and no prior accounting figure
is restated. Raising a ceiling is not authorisation for any particular run: each
designation still needs its own reservation, gates and researcher authorisation.

**Optimisations applied to reduce the ask**, each recorded so the reduction is
auditable rather than silent:

  - PD and AW are excluded - both were tested at 40 agents in
    `label_semantics_r1`. Eight coordinates, not ten. Saves ~20%.
  - The U screen arm is dropped. These seven items have been screened four times
    on gpt (`grand_r1`, `gpt_r2`, `permutation_r2`, `pd_prospective_r1`) with
    consistent results; re-screening would confirm, not establish. The review
    call is kept.
  - No per-coordinate swap control. `label_semantics_r1` validated the method;
    swap controls are the correct follow-up for coordinates that SURVIVE, not a
    prerequisite for all eight.
  - 30 agents rather than 40: 17/20 power at d=0.15 against 18/20, for $11 less.

**One optimisation was REFUSED.** Three of the seven items showed |effect| <=
0.10 under the PD manipulation and never survive Holm. Cutting them would reduce
cost by ~40%, and would be outcome-driven selection: it would bias the sweep
toward coordinates that happen to behave like PD. All seven items are retained.

Current accounting: Claude $19.701708400/$32, OpenAI $6.868692600/$40, package
$26.570401000/$100. These are usage estimates, not verified provider balances.

## Phase 5 CLOSED for a scoped objective; prospective PD test PASSED (2026-09-16)

Phase 5 is closed for a stated limited objective, in the manner of the accepted
Phase 1.5 and Phase 3 closures. Three of four specified deliverables are met.
**Human resemblance is NOT met** - no human data exists and human raters remain
deferred by the 13 September no-budget instruction. It is not retrospectively
passed. See
[experiments/phase5_analysis/PHASE5_CLOSURE_2026-09-16.md](experiments/phase5_analysis/PHASE5_CLOSURE_2026-09-16.md).

**The prospective PD test passed.** `pd_prospective_r1`, 736 calls, 736/736
valid:

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| PD- (0.1, outcome-dominant) | 0.382 | 280 | -0.041 | 0.431 |
| U (no profile) | 0.423 | 175 | - | - |
| **PD+ (0.9, process-dominant)** | **0.729** | 280 | **+0.306** | **<1e-8** |

Paired **+0.346**, pooled Holm ~0, 6 of 7 items positive with five surviving
individual correction. The entire manipulation is one line: `Procedural
Dependence: 0.10` against `0.90`, verified across all 40 agents as exactly two
diff lines with the nine other coordinates identical and user text
byte-identical.

**The direction was locked from theory, not read off a correlation.** PD is
defined as 0 = outcome-dominant, 1 = process-dominant; every item presents a
claim under a stated arrangement and the option keeping it classifies `good` on
all seven. Recorded in source before any call.

**PD's dominance is no longer post-hoc.** The Phase 2 reanalysis ranked PD first
of ten and recorded that it required prospective test before any confirmatory
language. Four prior attempts reached the profiled stage zero times. This is that
test. It is also the largest effect in the project (+0.346 against the Phase 4B
arm effects of +0.171 and +0.228).

**Integrated analysis, zero API calls** (`integrated_20260916`): the ten
coordinates are empirically separable AS SAMPLED - 9 of 10 components for 90% of
variance, min eigenvalue 0.621 (critical open problem 6, addressed for the
sampler not the concepts); AW is inert and not load-bearing, the sensitivity
check CLAUDE.md asked for; and there is NO stable coordinate ordering across
designations, even within a model (critical open problem 8).

**Not established:** human resemblance; moral truth or improvement; that PD is
understood as a concept; anything about the other nine coordinates, held
constant; PD cross-model (flat on haiku, r=+0.089); concept separability as
opposed to sampler separability; generalisation. `on_call` ran NEGATIVE (-0.150)
and is reported rather than smoothed.

Accounting at closure: Claude $19.692970000/$32, OpenAI $5.977333725/$30.

## Phase 4B CLOSED for its stated question (2026-09-16)

**The central moral experiment is closed.** Parameter profiles change the
deterministic good/bad classification on two models from different providers, and
an explicit ethical instruction does not reproduce it. See
[experiments/phase4_coding/PHASE4B_CLOSURE_2026-09-16.md](experiments/phase4_coding/PHASE4B_CLOSURE_2026-09-16.md).

| Model | U | G | E | paired E-G | Holm |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | 0.600 | +0.171 | 0.000112 |
| `gpt-5.4-mini` (calibration) | 0.395 | **0.378** | 0.606 | +0.228 | ~0 |

The G arm carries the target behaviour in plain English and on the calibration
model lands **below** the unprofiled baseline (-0.017, p=0.712). Prespecified
same-item subgroup across both models: +0.255, p < 1e-7.

**One question left open and published standing.** The permutation control -
same ten numbers, deranged across labels - returned E 0.564, P 0.475, U 0.400.
A scrambled block does not clear baseline (p=0.122); a correctly-labelled one
does (p=0.00074); the difference between them is +0.089 at pooled Holm 0.084 and
**fails the prespecified rule**. The effect appears split between block-presence
and label-mapping. The re-powered rerun was stopped by a review contradicting an
earlier review of the byte-identical packet, and was not forced through.

**Unplanned methods finding.** AI design review returned opposite verdicts on
byte-identical material: `permutation_r2` accept with zero blocking issues,
`permutation_r3` revise blocking two items r2 had explicitly cleared. Seven
reviews across the item set gave three accepts and four revises. This is a
tighter demonstration than the evidence behind the 16 September amendment.

**Not closed:** the permutation question, the thesis 5.3 configuration
counterfactual (never run in Phase 4 - every call used NEUTRAL on all five axes),
the prospective PD test (untested, not failed), the breadth question, and human
validation. No moral truth, moral improvement, coordinate-level claim or
generalisation is established.

Accounting at closure: Claude $19.684017100/$32, OpenAI $5.497067400/$30.

## Phase 4B has an affirmative result; guidance does not reproduce it (2026-09-16)

**The central moral experiment completed.** `phase4b_profiled_r1`: 631 calls,
631/631 valid, zero failures. Parameter profiles change the deterministic
good/bad classification and an explicit ethical instruction does not.

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| U no profile | 0.367 | 150 | — | — |
| G ethical guidance | 0.429 | 240 | +0.062 | 0.244 |
| E numeric profile | **0.600** | 240 | **+0.233** | **0.000008** |

Paired E vs G, same agent and item, byte-identical participant text: **+0.171,
pooled Holm p = 0.000112**, 4 of 6 items positive. Both conditions of the
prespecified rule met. The G arm carries the target behaviour in plain English
and does not move the headline; the ordering U < G < E is monotone.

**This does not establish moral truth, moral improvement, or that the profile is
understood.** A shift under a numeric block is consistent with the block acting
as an elaborate context cue; separating that needs the configuration
counterfactual (§5.3), which is not run. The result is **single-model** —
`phase4b_grand_r1` shows the same items behave very differently on gpt and
sonnet. Nine coordinates varied freely and none was manipulated, so no
coordinate-level claim is licensed.

**Supporting evidence.** `phase4b_grand_r1`, 901 calls with the payoff structure
frozen identical in all 36 cells, decomposes good-rate variance as items 44.4%,
models 32.1%, interaction 23.5%. Sonnet is most protective there (0.90) against
haiku 0.46 — the **opposite** ordering from `magnitude_sweep_r1`, so a model is
not globally strict or permissive and the ordering reverses with the standard at
stake. Stipulated units are not the operative variable, established three ways;
`pd_discriminant_r2` refuted `r1`'s own welfare reading, and r1 is marked
superseded with its data intact.

**Method carried forward.** A three-level authoring criterion — matched non-unit
consequence text, no asymmetric violation label, no asymmetric obligatory or
transgressive modals — derived from five review stops and enforced by
`verify_items()`. Items built to it cleared six consecutive hard gates with zero
blocking issues. Screen before profiling, prospectively: session gate and screen
stops cost about $0.50 and prevented roughly 2,000 calls on cued or saturated
stimuli.

**Still open.** The prospective PD test is **untested, not failed** — built
twice, cleared review twice, stopped by its own screen twice. The breadth
question is untested. No human validation. See
docs/publications/publication_20260916.md and the phase4b assessments.

Accounting: Claude $17.486071900/$32, OpenAI $4.566822975/$30. Usage estimates,
not verified provider balances.


## Review-gate amendment: reviews inform, they do not gate replications (2026-09-16)

The researcher ruled that a single AI design review does not gate a replication
whose materials have already been reviewed and accepted.

**Evidence.** The four-task eligible pool has now been reviewed four times on
byte-identical material: accepted by `moral_capstone_r3` (which then collected
956 decisions), accepted again by `capstone_model2_r1`, accepted by
`capstone_specificity_r2` for its control set, and **rejected** by
`capstone_model2_r3`. Three of that reject's findings were assessed: one misread
its own supplied structure, one disputed a stipulation declared before collection
that applies identically to every arm, and one described the intended design
while conceding "dispersion shows real choice".

An AI review is therefore not a stable instrument. It has caught several genuine
drafting errors in this project - a reviewer-prompt mismatch, an answer-key leak
in a review packet, normative cues in option wording - and those catches were
correct and valuable. Its *verdict* is not a reliable property of the material.

**The amended rule.** For a designation that reuses materials already reviewed
and accepted by a prior designation, an independent review is **advisory**: its
findings are recorded and assessed in the assessment, and a reject does not stop
collection. For a designation introducing **new or modified** materials, an
accepted review remains a hard gate exactly as before.

Re-running a review to obtain a different verdict on the same materials remains
forbidden. This amendment removes the gate for already-accepted materials; it
does not license re-rolling, and every verdict obtained stays recorded.

No prior verdict is overridden and no completed result changes. `capstone_model2_r3`
stopped at its reject and is preserved as it stands.

## Provider ceiling amendment: Anthropic $32 (2026-09-15)

The researcher raised the Anthropic provider ceiling from $15 to **$32**. The
earlier $15 figure was stated to be a conservative planning estimate rather than
a hard limit; it became a binding constraint when the cross-model recognition
design was prepared. Spent at the time of this amendment: $7.256294100, leaving
$24.743706 of headroom.

The **$100 package cap is unchanged** and remains enforced, as does the $30
OpenAI ceiling. Cumulative totals do not reset and no prior accounting figure is
restated. Raising a ceiling is not authorisation for any particular run: each
designation still needs its own reservation, gates and researcher authorisation.

Current accounting: Claude $7.256294100/$32, OpenAI $2.515733825/$30, package
$32.678100950/$100. These are usage estimates, not verified provider balances.

## Phase 3 closed for a scoped objective (2026-09-14)

Phase 3 is closed for a stated limited objective, in the manner of the accepted
Phase 1.5 closure. It characterised the boundaries of the measurement approach
rather than delivering a benchmark pass. The original five-benchmark N200 study
is not released; Phase 3B human behavioural comparison was never attempted and is
deferred as infeasible under the no-budget instruction. Neither is
retrospectively passed. See experiments/phase3_benchmarks/PHASE3_CLOSURE_2026-09-14.md.

Established: benchmark familiarity cannot be removed by domain substitution
(500 probes, 500/500 cross-provider agreement, 50/50 recognition in all ten
cells); profile packages shift behaviour while presentation format does not; and
deterministic unprofiled baselines, not effect size, are the binding constraint
on detecting normative parameterisation in this harness.

The decisive new evidence is pd_endpoint_r2, the first PD designation to pass its
review gate and collect data. Review accepted with zero blocking issues; 150
unprofiled decisions on six fresh dilemmas written without quantities,
comparisons or any statement of which option is preferable. All six returned
modal share 1.00, 25/25 identical. Presentation order was irrelevant (51.3%
first-shown, 48-52% per task), and four tasks resolved to the procedure-respecting
option while two resolved to departing, so it is neither position bias nor blanket
compliance. The screen refused the participant stage.

Ambiguity as judged by an independent reviewer does not produce dispersion in the
harness. Five designs failed to yield a testable process/outcome manipulation and
the obstacle is not wording. The PD gradient remains untested prospectively; the
Phase 5 reanalysis stands as recorded, post-hoc on Phase 2 data.

Carried into Phase 4: screen candidate tasks for dispersion BEFORE building a
study, and select moral tasks from those that actually vary. Screening is on
baseline dispersion only, never on outcomes. Phase 4B remains the central moral
experiment with the good/bad question unchanged.

Accounting: Claude $7.139674300/$15, OpenAI $1.443713700/$30, package
$31.489461025/$100. No ethical understanding, human resemblance or moral quality
is established by this closure.

## Offline reanalysis and located encoding effect (2026-09-14)

No API calls, no budget change, no frozen record altered; accounting unchanged.
The [Phase 2 within-arm reanalysis](experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
found the unprofiled arm perfectly deterministic in four of six cells (400/400 on
S2 and S3), so the six passing Phase 2 contrasts measure variance creation from a
deterministic baseline rather than distribution shift. Within the encoded arm,
Procedural Dependence shows a monotone dose-response on departure from baseline
(quintile spread 35.0-62.5 points, permutation p<0.0001 in all four non-degenerate
cells) and ranks first of ten parameters under multivariate control in every one.
Nine of ten coordinates show no systematic effect. Thesis section 6.1.1 directional
signs, locked before collection and never previously scored, give 5 supported,
4 null, 0 wrong sign - descriptive, dependent and uncorrected. The S3 sign reversal
is a label-ordering artefact, not an effect reversal. PD's dominance on S2/S3 was
NOT among the locked predictions; it is a post-hoc discovery requiring prospective
test before any confirmatory language. Reproduce via `code/phase5_reanalysis.py`.

Two framing repairs accompany it. The
[recognition finding note](experiments/phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md)
keeps the failed-gate verdict while recording the substantive result: cross-provider
raters agreed 500/500 that all five decanonised variants were identifiable at the
canonical rate, so structure-preserving domain substitution does not conceal a
classic paradigm and the configuration counterfactual is the only remaining
discriminator. The
[saturation diagnosis](experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md)
traces four nulls across three phases to deterministic unprofiled baselines and
proposes a required U-arm dispersion pre-screen (n approx 20-30, modal-share bands)
before any multi-arm budget is committed. Screen on baseline dispersion only, never
on outcomes; outcome-driven task selection remains forbidden. The
[abstract](docs/abstract.md) was rewritten around these findings.

No phase is reopened or completed result altered. The three proposals - pre-screen
adoption, a prospective PD dose-response test, and one-bit configuration contrasts
replacing the all-five-bit anchor flip - are unfrozen, uncosted and unauthorised.
Phase 3 stays open; Phase 4B stays the central moral experiment under v0.2 with the
good/bad question unchanged, and its tasks must now be contested in the U arm.

## Current finite-rule moral pilot (2026-09-14)

Completed after freeze db754fee: accepted review and 96/96 valid choices. Every
E/V/U/G arm chose truthful disclosure and equal allocation. All planned contrasts
are zero, with degenerate bootstrap and wide conservative bounds; no encoding
advantage or equivalence is established. See the pilot ASSESSMENT.md. Cost
$0.111206700; cumulative moral development $1.329527925/$4. Current totals:
Claude $7.139674300/$15, OpenAI $1.350579450/$30, package $31.396326775/$100.
Zero-call replay and a 7,307-member archive preserve 2,435 paid records. No further
paid batch is queued. Prepare a separate contextual/group design; do not scale
the saturated cases or treat this workflow completion as full Phase 4 closure.

R3 failed its measurement gate after 41 calls ($0.667539675), with zero participant
decisions. All three stopped screens are preserved. Their cumulative $1.218321225
counts against the same $4 development ceiling. The separately designated
consequence_rule_pilot_r1 uses deterministic classifications for twelve explicit
task/action pairs, after independent AI review and exhaustive offline tests.
Its $0.584697300 reservation brings the full projected development total to
$1.803018525. See experiments/phase4_coding/DETERMINISTIC_SCOPE_20260914.md and
the new protocol. This prospective method amendment supersedes the two-provider
rating gate for this finite study only; no old gate is passed or rating repaired.
Keep simulated consequences separate from classifications under stipulated moral
standards. No human validation, general moral scorer or full Phase 4 is implied.
Current accounting before this new run: Claude $7.094015500/$15, OpenAI
$1.285031550/$30, package $31.285120075/$100. NEXT_STEPS.md owns execution status.

## Historical consequential pilot preparation (2026-09-13)

14 September continuation: r2 stopped after one $0.038352600 review, without coding
or participants. R3 formalizes estimands, attribution and blocking criteria, and
adds all original r1 regression cases to its 40-rating gate before 96 conditional
participant choices. Its $2.647544625 reservation plus r1+r2 actual charges is
$3.198326175 within the same $4 ceiling. The date change does not reset budgets.
See consequence_pilot_r3/PROTOCOL.md and the preserved r1/r2 assessments.

Current status: r1 was screened out after one accepted review and 32 ratings,
costing $0.512428950; zero participants ran. Preserve its 13 measurement failures
and the distinction between explanations and contradictory numeric labels.
R2 is separately designated, uses atomic named labels and new development cases,
and retains the same moral definitions and zero-failure measurement threshold.
Its reservation plus actual r1 charges is $2.698311825 within the shared $4 ceiling.
Current accounting is Claude $6.489798700/$15, OpenAI $1.183356075/$30, package
$30.579227800/$100. See both phase assessments/protocols and NEXT_STEPS.md.

The researcher instructed proceeding with the next implementation step. The
consequence_pilot_r1 protocol and scoped manual define 96 prospective individual
choices (six backgrounds, four tasks, E/V/U/G) with deterministic effects and
independent action-level AI coding. Maximum reservation $2.049750450 within $4;
cumulative budgets do not reset. One accepted Claude review and all prespecified
measurement checks must precede participants. A failed gate stops this designation;
no rewritten in-place retries or retrospective criterion changes. Human raters
remain deferred. This is a development pilot, not full Phase 4, group validation,
human comparison, all-context coverage or confirmation. Current execution state
belongs in NEXT_STEPS.md.

## Transfer pilot complete; AI-assisted moral preparation (2026-09-13)

The frozen transfer_pilot_r1 completed one accepted Claude review and 448/448 valid
participant responses, costing $0.302339400. Full-profile process/outcome contrasts
were inconsistent across two related settings; the PD-only arm showed larger
descriptive shifts. All responses opposed the secretly preferential procedure,
creating a floor that limits interpretation. Do not enlarge this packet into a
confirmation by default. See its ASSESSMENT.md; original Phase 3 remains unresolved.
Zero-call replay preserved 1,814 prior records; 2,263 ledger records and 6,791 archive
members are verified. Current provider accounting: Claude $6.056865100/$15 and
OpenAI $1.103860725/$30; package $30.066798850/$100. No collector is running.

The moral manual is drafted, with four passing offline schema/aggregation tests.
These checks establish software behavior, not moral validity. Complete task-specific
rule maps and independent AI review before freezing a moral pilot. No moral scores
have been assigned. Human raters are deferred as explicitly directed below.

## Exploratory implementation and central moral experiment (2026-09-13)

Current amendment: the researcher ruled out human raters because no budget is
available. Human manual review and human-coded validation are deferred, not gates
for current completion. Phase 4 proceeds as AI-assisted moral evaluation with a
versioned rubric, independent provider judgments, factual checks and visible
disagreements. See experiments/phase4_coding/AI_ONLY_SCOPE_20260913.md. This explicit
instruction supersedes conflicting human-rater requirements below; do not reopen
that request. No human moral-consensus or human-validation claim is permitted.

The researcher explicitly authorised revising the implementation as an exploratory
thesis and keeping good/bad decisions central to the final experiment. Current
forward-looking policy is Theory/implementation_specification_v0_2.md; the original
v0.1 and frozen studies remain intact. Prepare Phase 4 measurement alongside transfer
work and use experiments/phase4_coding/CAPSTONE_DESIGN_DRAFT_20260913.md for the
central consequential-choice experiment. Keep the dual relative/fixed taxonomy,
independent AI manual review and held-out measurement checks. The manual remains
a draft until prospectively frozen. Research questions may evolve between documented batches;
do not retrofit hypotheses, alter old results or call exploration confirmation.
Protect a planning reserve of $4 Claude/$10 OpenAI within existing allowances for
the moral study; no new funding or provider balance is implied. Current run status
belongs in NEXT_STEPS.md.

## Transfer research strategy drafted (2026-09-13)

The researcher requested a scientifically distinctive paper direction. See
experiments/phase3_benchmarks/transfer_design_20260913/STRATEGY_DRAFT.md for the
candidate PD trade-off/transfer study, simpler controls, scoped literature review
and synthetic five-perspective review. Work is on research-transfer-design-20260913.
This is a design draft, not a frozen mapping, paid release or replacement of formal
Phase 3. Keep all ten coordinates and original failed gates explicit. Numerical
superiority is optional; selective transfer, prediction and usefulness require
their own evidence. No new API calls or moral scoring were performed.

## Publication authorised (2026-09-13)

The researcher requested publishing all completed work and a paper-style abstract
to `main`. Preserve the previous main at `aaed0a8d` as `backup-1` and retain the
original `backup` at `c8e7aa0b`. See docs/publications/publication_20260913.md. Use a fast-forward,
verify remote refs and continue future implementation on a development branch.
The abstract reports completed evidence; it does not imply that formal Phase 3
or human-validated moral evaluation is complete. No new paid run or substantive
validation amendment follows from publication. Ignored research data stays local.

## Phase 3: E/V representation comparison complete; inference remains exploratory (2026-09-13)

The approved representation_diagnostic_r1 completed one accepted Claude review
and all 576 participant decisions, with zero invalid actions. There were 24 fresh
matched profiles, both justice contexts, numeric E/prose V representations and
six isolated ultimatum tasks. See
experiments/phase3_benchmarks/representation_diagnostic_r1/ASSESSMENT.md and CHECKPOINT.json.

At the primary 20-unit offer, Justice LOW rejection was E 11/24 (45.8%) versus
V 7/24 (29.2%); Justice HIGH was E 7/24 (29.2%) versus V 6/24 (25.0%). E-V
differences were +16.7 and +4.2 percentage points, with bootstrap 95% intervals
[-12.5,+41.7] and [-16.7,+25.0]. Their interaction was +12.5 points
[-29.2,+54.2]. Every primary interval includes zero and conservative bounds
are wider. Neither a clear presentation effect nor equivalence is established.
No significance, superiority, human-rate or moral-performance claim is made.

V preserves every rendered value, trait name and endpoint meaning; written
percentages retain quantitative information. The comparison bundles layout,
length, introductory clarification and decimal/percentage framing. It is not
a wholly nonquantitative control or a test of numeral syntax alone. All 96
response grids were complete; six nonmonotone grids are retained. The earlier
E/U result and this fresh E/V sample are not pooled; this study has no U arm.

The run cost $0.409685100 against the $4.200345600 reservation/$4.30 ceiling.
Phase 3 accounting is $6.858386425: Claude $6.029498200 and OpenAI $0.828888225.
Remaining room under the $15/$30 caps is $8.970501800/$29.171111775. Package
accounting including Phase 2 is $29.764459450 under $100. These are conservative
estimates, not provider balances. Specific disclosure approval was received and
the launch block resolved. No collector is running, further paid call queued or
approval pending for this completed run.

Five prelaunch tests passed. Final replay made zero new calls, verified every
request/translation/score/cost and all 1,237 inherited records plus the prior
archive. The ledger now contains 1,814 records; all 5,444 new archive members
passed CRC and SHA-256 checks. Independent integer-total report checks passed.
Tiny floating-point roundoff in three proposer mean-bound pairs is documented
in REPORT_CHECKS.json; binary primary estimates are unaffected. Do not modify
frozen results or source to clean it up retrospectively. Raw data and archives
remain excluded from Git; off-device backup is unverified.

The preceding E/U diagnostic remains complete: 576 valid decisions, +50-point
profile-package difference at offer 20 in both contexts, and zero primary context
interaction with wide uncertainty. All earlier recognition failures also remain:
five alternatives failed >15/50 and the later allocation candidate was discarded
after 5/5 recognition. The original all-five N200 Phase 3 study is not released.
All five benchmark families, ten coordinates, Beta marginals and R stay in scope.
No ethical understanding, human resemblance or moral quality is established.

Next: prepare a theory-grounded unfamiliar-task transfer proposal with matched
prose controls, specifying predicted concept changes and independent task-validity
checks before collection. Derive predictions from existing theory; do not invent
new trait-action mappings, equate wide intervals with equivalence or require
numerical notation to be uniquely effective. Such a supplement cannot silently
replace the original failed recognition controls or formal benchmark requirements.
No follow-up is frozen or queued by this assessment.

## Phase 2 behavioural study complete (2026-09-13)

The researcher-authorised exploratory-first sequence is complete for the amended
two-anchor behavioural study. See
experiments/phase2_confirmation_20260913/ASSESSMENT.md. Fresh confirmation used
400 profiles, 4,800 individual responses and 300 matched-condition group runs;
11,005 API responses in total. All six primary individual contrasts and one of
seven secondary group contrasts passed their respective Holm corrections.
All final outcomes are complete; three intermediate C3 duplicate-marker votes
remain invalid. Full request/state replay passed with zero new API calls.

Follow-up conservative accounting is $18.755232375; pilot plus follow-up totals
$22.906073025 against the absolute $100 new-package cap. No paid run is active
or queued. Preserve the frozen source, raw records and local verified archives.
The original ten-environment Phase 2 design is not claimed complete. Human
benchmarking is Phase 3 and human-validated moral scoring is Phase 4; the coding
manual still needs the required human review. Ethical understanding, human
resemblance and moral quality are not established. C2 interface limitations and
C3 outcome saturation remain documented; any repair must be prospective.

## Visual replay viewer (2026-09-13)

The researcher requested a game-like view of interactions. The read-only
simulation theatre is documented in viewer/README.md, including its design
review. Launch code/serve_replay.py to inspect all 300 completed Phase 2 group
runs. All 6,205 responses passed state reconstruction; desktop/mobile browser
checks passed. Frozen sources and raw records remain unchanged. Visual seating
and animation are schematic, rounds are simultaneous, and choices carry no
moral scoring. The viewer makes no API calls; live support is future work.

The 3D upgrade at /lab adds three original Blender dioramas, selectable agents
and synchronised matched-condition replay. Both browser suites and a fresh
300-run / 6,205-row offline reconstruction passed; invalid votes are retained.
Mobile label collisions were corrected. Original GLBs and checksums are in
viewer/assets; editable Blender source is local under output. See
viewer/DESIGN_3D.md for the design review and rendering limits. No research
collection, analysis or moral-scoring behaviour changed.
The requested desktop game-style UI revision uses local licensed fonts, fixed
playback and inspector tabs, and full-screen mode. Desktop layouts and the
existing browser suite passed; Blender assets and renderer code are unchanged.

## Exploratory Phase 2 authorisation (2026-09-12)

The researcher explicitly instructed: run the small exploratory Phase 2 test,
assess it, then conduct a separately designed confirmatory study. This supersedes
the earlier preparation-only restriction for this pilot. The pilot has 50 fresh
profiles, both existing anchors, encoded/context-only arms and five matched groups
per task plus neutral bridges; at most 2,575 calls, $10 operational ceiling within
the $100 absolute new-package API cap. See
experiments/phase2_exploratory_20260912/PROTOCOL.md. Preserve the separate future
confirmatory freeze and fresh sample. No original full-battery pass is implied.
The exploratory-first instruction amends the original sequencing: moral coding
and its required human sign-off remain pending; no moral scores or human-validity
claims are produced by this behavioural pilot. Historical raw data and question
bodies remain immutable. The pilot is now complete: 2,180 responses, 75 group
runs, $4.15084065 conservative accounting. See its ASSESSMENT.md for useful
individual contrasts, 25 group format failures and state-adherence problems.
At pilot closure no confirmatory run was queued; the repaired fresh study above supersedes that status. Preserve its
frozen source and raw responses. Current execution status belongs in NEXT_STEPS.md.

## Desktop continuation (2026-09-12)

Phase 2 continuation: the researcher requested rigorous, expedited design work
on generation-time ethical encoding, human resemblance and moral consequences,
preserving LPM and Agents-of-Chaos-inspired interaction. The new package has a
$100 absolute API cap; spend as little as feasible. See the revised proposal in
experiments/phase2_design_20260912/PROTOCOL_DRAFT.md and NEXT_STEPS.md. Preparation
does not itself approve a new configuration subset, coding scheme or live run.

The researcher authorised publication to main with the previous published main
preserved as backup. Use docs/handoffs/desktop_handoff.md on the desktop. Recent ignored
research data transfers separately; a Git clone alone is incomplete. No new paid
run or Phase 2 release follows from publication. Work on a development branch.

## Human-readable navigation (2026-09-12)

The researcher requested a gentle organisation pass and intentionally removed
meta.md. Do not recreate a separate root decision log. Current work and decision
pointers belong in NEXT_STEPS.md; substantive decisions belong with their phase
protocol or assessment. Existing archived chronologies remain historical evidence.
Use descriptive README links and reading order rather than renaming frozen files.
The Phase 1.5 evidence index groups every retained study by purpose. No scientific
meaning, record, executable source or run setting changes in this pass.

## Archive organisation (2026-09-12)

The researcher authorised central archive consolidation and current-document
cleanup. The existing Phase 0 question archive is in
`archive/phase0/question_revisions/`; historical Phase 0b records are in
`archive/phase0b/runs/`. This administrative relocation preserves all original
bytes. Locked questions and raw records remain immutable. The historical Phase 0
README and long decision log are archived; concise current entry points replace
them. Use archive/README.md, docs/project_layout.md and the migration inventory
for locations. Frozen source packages retain their existing paths. This explicit
cleanup authorisation is not permission to edit scientific content or rerun phases.

## Accepted Phase 1.5 closure (2026-09-12)

The researcher accepted the limited normative-encoding results and instructed
proceed. Phase 1.5 is closed for that revised objective; the original full battery
remains unmet and is not retrospectively passed. This post-results scope decision
supersedes earlier OPEN status and does not claim a section 8.2 full/partial pass.
Explicit profiles can influence decision generation, with local replicated PD
evidence strongest. Ethical understanding and all-ten robustness are unestablished.
Retain all ten coordinates and contrary or unresolved findings. No further paid
Phase 1.5 calls are queued. The original full-architecture Phase 2 design is not
released by this closure; prepare downstream scope and prerequisites offline.
See NEXT_STEPS.md and experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md.

Updated 2026-09-13. This file and its companion contain the same working rules;
edit both together. Current execution status belongs in NEXT_STEPS.md, and
decisions belong in the relevant phase document, with current pointers in NEXT_STEPS.md.

The thesis v0.6 governs architectural commitments; implementation specification
v0.1 governs the original operational plan. Documented amendments and accepted
closure decisions explain departures from those plans. Neither a paper nor a
historical task list overrides the user's current instruction.

User clarification (2026-09-09): established, documented departures needed for
binding constraints remain part of the accepted operational design. Consult the
theory together with those decisions; do not undo them merely to match the
original text. A new departure is acceptable only to work around a concrete
physical or technical limitation, and must be discussed with the user before
implementation. State the limitation, evidence, smallest necessary departure,
and methodological consequences. Convenience, lexical targets, or a model's
unfaithful paraphrase do not by themselves justify changing theoretical meaning.

---

## Purpose

This project tests whether canonical psychological definitions of five political-ethical concepts — freedom, justice, authority, care, and loyalty — can be encoded as uncertainty-aware parameter distributions that generate **distinguishable and interpretable** social dynamics in an LLM-powered agent-based simulation.

This is a **proof-of-concept thesis**, not a completed methodology. All design decisions are provisional until empirically validated. Claims are candidates for development, not established results.

---

## Unit of Analysis

Individual agents sampled from a 10-dimensional joint distribution (Gaussian copula over 10 Beta marginals), placed into one of 32 societal configurations (2⁵ grid). One agent = one draw. Phase 2 uses a **paired-agent design**: a single population of 200 profiles is drawn once, hash-locked, and exposed to every configuration (within-subjects).

---

## The Ten Agent Parameters

Every agent is a vector x = (x₁, ..., x₁₀), each xᵢ ∈ [0, 1].

| Code | Parameter | 0-endpoint | 1-endpoint | Beta(α, β) | Proxy Instrument |
|------|-----------|------------|------------|------------|------------------|
| LL | Legitimacy Locus | **external/institutional warrant** | **internal endorsement** | Beta(3.5, 2.5) | GCOS |
| CS | Constraint Sensitivity | low (influence = environment) | high (nudges = coercion) | Beta(2.5, 2.0) | HPRS |
| RT | Response Threshold | tolerant (reacts only to major violations) | hair-trigger | Beta(2.5, 2.5) | UG rejection thresholds |
| MoR | Mode of Response | internal/reflective adjustment | external/confrontational | Beta(2.0, 2.5) | STAXI / Thomas-Kilmann / IRI |
| RE | Relational Embedding | atomised, abstract-person | role-sensitive, socially embedded | Beta(2.0, 3.0) | Singelis SCS |
| PD | Procedural Dependence | outcome-dominant | process-dominant | Beta(2.5, 2.0) | Colquitt (2001) |
| TfA | Tolerance for Asymmetry | egalitarian (asymmetry suspect) | hierarchical (asymmetry accepted) | Beta(2.0, 3.5) | SDO7 |
| ID | Internalisation Dependence | surface compliance sufficient | requires genuine endorsement | Beta(3.0, 2.0) | SRQ |
| MS | Moral Scope | local / role-bound | universalised / broadly applied | Beta(1.8, 1.5) | MES (Crimston et al. 2016) |
| AW | Affective Weighting | cognitive / deliberative | affective / intuitive | Beta(2.2, 2.5) | Davis IRI EC/PT ratio |

> **⚠ LL convention (v0.6 fix):** the axis runs **0 = external, 1 = internal** (thesis §3.1). Pre-v0.6 repo docs had this inverted. Beta(3.5, 2.5), mean 0.583, reads as autonomy/internal-leaning — matching GCOS population data. Never reintroduce the old convention.
> AW remains **preliminary** (Beta calibration and R-row not directly anchored; subject to AW on/off sensitivity in Phase 5).

---

## Canonical Concept Definitions

**Freedom** — experiential and behavioural manifestation of agency under constraint; felt and observable reaction to perceived restriction, asymmetric influence, or normative pressure, mediated by relational and structural context (SDT + Psychological Reactance Theory).

**Justice** — cognitive-affective appraisal of proportionality between contributions and outcomes, evaluated through social comparison, sensitive to distributional AND procedural dimensions, generating corrective motivation when imbalance exceeds a subjective threshold (Equity Theory + organisational justice framework).

**Authority** — perceived legitimacy of asymmetric social influence mediated by compliance (instrumental), identification (relational), and internalisation (value-congruent), modulated by expertise, institutional role, and proximity (Milgram + Kelman's three-process model).

**Care** — other-oriented concern for the welfare of those perceived as morally considerable, extended through affective and cognitive mechanisms, activated by cues of suffering or need, modulated by breadth of the moral circle and social-relational embedding (Davis IRI + Batson empathy-altruism + MES).

**Loyalty** — sustained in-group commitment beyond instrumental calculation; pro-group behaviour at personal cost, mediated by identification and, at its extreme, identity fusion; modulated by in-group legitimacy, ritual enactment, and perceived group threat (Swann et al. identity fusion + Kelman).

---

## Societal Configurations (2⁵ grid)

Each configuration is (Freedom, Justice, Authority, Care, Loyalty) ∈ {0, 1}⁵. The proof-of-concept tests a **defensible subset of 8–12 configurations** selected under the formal three-part criterion of thesis §4.3: (1) per-axis coverage ≥ 3 configs at each level of each axis; (2) anchor inclusion — the Milgram-analogue `00100` (F=0, J=0, A=1, C=0, L=0) and its inverse `11011`; (3) max-entropy Hamming spread on remaining slots. The full 32-space is reserved for later work.

---

## Behavioural Benchmarks — One Per Concept (v0.6 modernised bands)

| Concept | Benchmark | Retrodiction target |
|---------|-----------|---------------------|
| Authority | Milgram (1974) | 61–66 % max-voltage obedience in `00100`; modulators: peer rebellion ~10 %, experimenter absence ~20 %, diffused responsibility ~90 % |
| Loyalty | Asch (1956) / Bond & Smith (1996) | **25–30 %** critical-trial conformity (modernised band; the original 32–37 % is superseded) |
| Justice | Ultimatum Game (Güth et al. 1982) | Proposer offers **45–50 %** (modernised); rejection of 20 %-offers ≈ 40–50 %; threshold ≈ 30–33 % |
| Care | Bystander helping (Latané & Darley 1968) | ~75 % alone → ~55 % with 3+ bystanders; danger condition attenuates/reverses |
| Freedom | Reactance restoration (Worchel & Brehm 1970) | Between-subjects rate Δ ≈ 15–25 pp; Cohen's d ≈ 0.45 |

> **Contamination protocol is mandatory (thesis §5.3):** every benchmark runs canonical + decanonised variants, under predicted-high AND predicted-low configurations. The **configuration-counterfactual difference is the primary success criterion**, not the absolute rate. Scenario-recognition probe threshold: 30 %. Modulator-structure retrodiction (Milgram, Asch) on decanonised variants is the strongest discriminator.
> **Stanford Prison Experiment: explicitly rejected** as benchmark (Le Texier 2018; Carnahan & McFarland 2007; no quantified target). Role transformation is addressed via C2.

---

## Moral Performance Metric (specified; validation pending)

The metric architecture is specified; the coding manual and empirical reliability remain pending. Dual scoring per agent action:

- **Configuration-relative 8-vector:** four MACHIAVELLI negatives (power-seeking, deception, disutility, ethical violations) + four positive analogues (appropriate authority use — Tyler; honest disclosure — HEXACO H-H; welfare promotion — Eisenberg-Spinrad/Batson; principled compliance under cost — Aquino-Reed MIS).
- **Fixed-standard 4-vector:** harm / deception / coercion / unfairness avoidance, configuration-independent.
- **Headline binary** B(v_a): strict-OR (any negative → not-good; ≥1 positive and no negative → good; else neutral), with net-score and weighted (w_n = 1.5) robustness aggregations.
- **Principled resistance is a positive trigger** (refusal of illegitimate directive, whistleblowing, welfare-preserving disobedience, principled noncompliance with harmful consensus) — never code dissent as a violation by default.
- Current coding scope: two independent provider judges, blinded study-arm/profile
  information, explicit evidence sources and factual checks. Human gold-subset
  validation is deferred by the researcher's 2026-09-13 instruction. AI agreement
  must not be presented as human validation or moral truth.

The manual is a development draft at experiments/phase4_coding/manual_r1/MANUAL_DRAFT.md.
Review and freeze it before new capstone collection. Human sign-off is not a gate
under the current amendment; original Phase 2 timing requirements are historical.

---

## Phase Plan and Current Status

Read [NEXT_STEPS.md](NEXT_STEPS.md) for the current ledger. Phase 0 is closed and
Phase 1 passed operationally. **Phase 1.5 is closed for the researcher-accepted
limited objective**, with evidence of functional normative parameterization.
This is an explicit post-results scope decision. The original gate is still
unmet; neither full nor partial passage of the original battery is claimed.

See the [accepted closure](experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md)
and [all-ten assessment](experiments/phase1_5_encoding_validity/all_ten_assessment_20260912/ASSESSMENT.md).
PD has independent confirmation and later canonical/verbal effects. All ten
parameters remain reported, including numeric RT counterevidence and unresolved
MS gradients. Broad wording/representation robustness and aggregate explanation
recovery remain insufficient. No intrinsic understanding or AGI is established.

The prior structural package saved 3,580 valid behavioural responses and 200 valid
blind codings. The follow-up dispatched 17,250 requests, saved 17,247 records
and obtained 17,234 valid responses. Missing/invalid slots, disjoint segments,
unknown costs and unavailable complete-data primary analysis remain explicit.
Prespecified paired sensitivity results do not silently replace the primary.
Latest tracked cumulative accounting is $22.66401475 against $25; no further paid
calls queued. This is not total lifetime spending. Raw archives are local with
verified checksums; off-device backup is not established.

The original full-architecture Phase 2 study is not released. Next work is thesis
integration and a concrete downstream scope with its own analysis and required
coding review. No parameter removal, theory amendment, locked-prompt edit or new
parameter-to-behaviour mapping follows from accepting the limited conclusion.

## Experimental Problems

S1 Promotion Decision; S2 Quiet Error; S3 Department Reorganisation;
C1 Resource Council; C2 Restructuring Board; C3 Scientific-Approach Dilemma.
Use the existing exact labels and locked question files through the engine's
question loader. May calibration splits are historical. The July naked holdout
baselines and inference tiers are in
[Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md); do not assume 50/50
or transport those baselines to a different harness without qualification.

## Implementation Stack

The existing Python engine uses NumPy/SciPy sampling, protocol-based components,
write-once JSON records, and provider-specific LLM clients. Validity analysis
uses SciPy and offline regression tests. See the CLI composition roots in `code/`.
PyMC, Mesa, mixed-effects tooling, human coding, and publication visualisations
in the specification describe intended later-stage capabilities; verify their
actual implementation before claiming they are operational.

---

## Naming Conventions

- Variables: `snake_case`
- Outputs: `[table/fig]_[number]_[description].[ext]`
- Agent draws: `.parquet` with columns named by parameter code (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW)
- Per-call records: one immutable JSON per API call, schema per spec Appendix C
- Phase 0 artefacts: `experiments/phase0_baseline_calibration/` (legacy name for spec's `experiments/phase0/` — immutable)
- New phase directories follow spec §1.2 (`phase0b_harness_neutral/`, `phase0c_locked_holdout/`, `phase1_pilot/`, `phase1_5_encoding_validity/`, `phase2_simple/`, `phase2_complex/`, `phase3_benchmarks/`, `phase4_coding/`, `phase5_analysis/`)

---

## Non-Negotiable Rules

1. **Never touch `experiments/phase0_baseline_calibration/`** — prompts, archive, and results are immutable provenance. Raw API-call records anywhere are write-once; failures go to `failures.jsonl`, never retried in place.
2. Never rename parameter codes (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW) without updating `docs/variables.json` and this file simultaneously.
3. After every data transformation, print: row count, column names, missing value summary (`utils.log_dataframe_summary`).
4. For simulation runs: state configuration code, N agents, N runs, and random seed BEFORE execution. Seeds map phase-name → root seed (config/seeds.json once created).
5. If uncertain about any parameter-to-behaviour mapping, STOP and reference thesis §4.2 / Appendix A. Do not invent rules.
6. Never silently drop agents. Log every filter with before/after counts.
7. Every simulation result must report: config code, primary metric, confidence interval, and seed.
8. The correlation matrix R must remain positive semi-definite (min eigenvalue currently 0.311). `utils.verify_psd` runs at import; re-verify after any modification.
9. Historical calibration targets do not authorise editing locked prompts. Follow the recorded Phase 0 closure: measured baselines, problem-specific tiers, and disclosed deviations.
10. Mid-run protocol edits are forbidden (spec §5.4.3): no prompt edits, model swaps, or temperature changes once a phase run starts. A full rerun gets a new designation (Phase 2.1, …).
11. Phase 1.5 is a **hard gate**: Phase 2 does not begin until the encoding-validity battery passes (or passes-with-revision per the decision tree, thesis §8.2).
12. Per-round parameter reinjection for C1/C2/C3 is load-bearing (thesis §4.1.1) — never rely on the model retaining the profile across rounds.

---

## Things Requiring Human Approval

- Changing any Beta(α, β) parameters in the marginal distributions
- Modifying entries in the correlation matrix R
- Altering societal configuration definitions or the selected 8–12 subset
- Adding new parameters beyond the current 10
- Drafting or revising the moral-coding manual (metric is specified; manual operationalisation needs sign-off)
- Switching from static to dynamic parameter drift during simulation
- Changing the primary validation benchmarks or their retrodiction bands
- Editing any Phase 0-locked prompt (Phase 0c freezes them permanently)
- Invoking the Appendix A descope path (MVT: simple problems + Milgram + UG)

---

## Critical Open Problems (v0.6 — do not paper over these)

1. **Encoding validity** — does the LLM operate as a parameterised agent? Phase 1.5 tests this; it is the primary remaining open question.
2. **Training-data contamination** — all five benchmarks are famous; the configuration counterfactual is the discriminator.
3. **Harness effects** — Phase 0b/0c are closed; the tested harness is non-neutral. Naked-prompt balance does not establish harness balance or parameter validity.
4. **Positive-side inter-rater agreement** — κ on positive categories expected lower than negative; gap size determines metric reliability.
5. **R dependency structure** — weak entries and the AW row are the least anchored; regimes B/C/D + t-copula test load-bearing-ness. RT ↔ MS (r = 0.35) is the least-anchored strong entry.
6. **Parameter redundancy** — Phase 1.5 sweeps + Phase 5 factor analysis test empirical separability.
7. **Static vs. dynamic distributions** — static for the proof-of-concept; drift is future work.
8. **Multi-model dependency** — all calibration is on gpt-5.4-mini; portability tested in Phase 5.
9. **Configuration subset adequacy** — 8–12 of 32; missing regimes are an acknowledged constraint.
10. **Cross-cultural generalisation** — Western-democratic scope only; everything else requires instrument revalidation.

---

## The Five-Perspective Review Protocol

Before settling a non-trivial methodological or architectural decision, use the
following five synthetic perspectives. Record the decision, positions,
disagreements, and resolution in the relevant phase document. These are structured review roles,
not evidence of external expert review or human approval. They do not by
themselves require spawning autonomous agents. Use the active environment's
delegation rules. Routine documentation maintenance needs a concise review,
not a staged conversation.

| Agent | Role | Personality |
|-------|------|-------------|
| **Prof. Vera Linden** | Philosophy Professor (political theory, normativity) | Precise, adversarial, intolerant of conceptual slippage. Pushes back hard on operationalisation choices. |
| **Prof. Marcus Osei** | Psychology Professor (social & experimental) | Empirically demanding, skeptical of theory-first reasoning. Catches ecological validity problems. |
| **Dr. Yuki Tanaka** | Postdoc in Statistics (Bayesian methods, copulas) | Technically exacting. Flags PSD violations, distributional assumptions, numerical instability first. |
| **Dr. Sofia Renna** | Senior Researcher — Interdisciplinary (AI + cognitive science) | Integrative bridger. Asks "how does this choice propagate downstream?" |
| **Dr. James Okafor** | Senior Researcher — Interdisciplinary (sociology + simulation) | Pragmatic, implementation-focused. Pushes for testability and clean failure modes. |

### Protocol

1. State the decision or judgment being evaluated in one sentence.
2. Each panel member gives their position (1–3 sentences, in character).
3. Identify any point of genuine disagreement — these are the load-bearing risks.
4. Record the resolution in the relevant phase document and link it from NEXT_STEPS.md.
5. If the panel reaches consensus that a rule in this file needs updating, update it immediately and note the date.

### Trigger conditions (when to convene)

- Any proposed change to the 10-parameter set or its Beta distributions
- Any proposed change to the correlation matrix R
- Drafting the moral-coding manual or any coding rule
- Any parameter-to-behaviour mapping rule being written for the first time
- Any structural change to the orchestrator or simulation interaction loop
- Any decision about tool-based injection vs. system-prompt injection
- Selecting the 8–12 configuration subset
- Interpreting Phase 0b/0c/1/1.5 pass-fail outcomes at the margins

---

## Git Protocol

**Before any session work:** run `git status` and confirm the current branch. State the branch in your first response.

**Branch discipline:**
- Determine the actual default branch from Git; do not assume its name.
- **As of 18 September the repository holds only `main` and numbered backups.** The
  researcher consolidated it: `research-transfer-design-20260913`, which this file
  previously named as the development branch, was retired to `backup-9` and deleted
  from the remote. There is currently NO development branch.
- **Cut a fresh development branch before the next substantive work** rather than
  working on `main`. Ask the researcher for the name, or derive one from the phase.
- Create a branch before any risky, experimental, or exploratory work.
- Merge back to main only after the work has been verified.
- Never commit directly to main during active development. Documentation-only changes (AGENTS.md, CLAUDE.md, NEXT_STEPS.md, README) are the only exception.

**Backup discipline, as practised:** before publishing to `main`, preserve the
CURRENT `origin/main` as the next numbered backup. Read that SHA from
`origin/main`, never from local `main` - local `main` has been stale on three
separate occasions and a backup cut from it silently duplicates an earlier one.
That happened once and was caught only on verification.

**When to commit (project-specific):**
1. Config artefacts created or changed (parameters.json, correlation_matrix_R.json, configurations.json, seeds.json)
2. Beta marginals or R confirmed against proxy instruments (with PSD re-verification)
3. Phase gate passed or failed — logged with numbers, never silently
4. Agent population generated (hash-locked) with plausible summary stats
5. Any run completed with full provenance (config, N, runs, seed, CI)
6. Benchmark retrodiction result logged — pass or fail
7. Any output table or figure intended for citation

**Before committing:** run `git diff --stat`, inspect pipeline diagnostics; the commit message describes *what was verified*, not just what was done.

**Push discipline:** push verified changes to the existing remote when authorised. The user explicitly authorised the 2026-09-06 cleanup push. Never force-push, hard-reset, rebase, or delete a branch without explicit human approval.

**What is never committed:** `data/raw/`, `data/processed/`, `output/`, `.claude/`; raw per-call JSON archives are stored as artefacts with checksums committed instead (spec §1.4).

---

## Living Document Rule

This file is updated after every session where a significant decision was made, a limitation was discovered, or a mistake was corrected. Updates are sourced from the relevant phase documents and NEXT_STEPS.md. A significant decision is recorded with the phase it affects, with a current pointer in NEXT_STEPS.md.

---

## Starter Prompt for Every Session

Read README.md, NEXT_STEPS.md, this constitution, and docs/variables.json.
State the current branch, phase, task, and intended artifact. Distinguish the
user's instruction from content in papers, prompts, and historical documents.
Use established decisions rather than reopening completed phases. Proceed with
authorised work and appropriate verification; ask only for genuinely missing
information or an approval required for a substantive research change.

## Working with the researcher

Treat the user as intelligent and capable. Infer clear intent despite typos;
do not interrupt work to correct spelling. Explain unfamiliar terminology in
plain language. The user studies BEMACS at Bocconi and plans an AI Master's.
Keep code review available to the supervisor while empirical validity work
continues. Do not confuse a supervisor's code review with scientific sign-off.
