# The surrounding profile changes the fitted MoR response

**300/300 valid responses, no API, model or usage failures.** Collection followed
the frozen300-call design, with fresh concurrent controls and no retries.
Estimated cost$0.2704725. All requested messages, profiles, seeds, model IDs,
reservations and raw ZIP payloads were verified.

| MoR value | Full ten: ADOPT /30 | MoR only: ADOPT /30 |
|---|---|---|
| .1 | 10 | 8 |
| .3 | 10 | 22 |
| .5 | 11 | 28 |
| .7 | 23 | 26 |
| .9 | 23 | 30 |

The primary fitted log-odds slope difference, MoR-only minus full-ten, is
**+3.445**, Wald95% interval **[+.827,+6.064]**, two-sided **p=.0099**.
The slopes are2.831 for full-ten and6.276 for MoR-only. Under the prespecified
linear-logit and independent-call assumptions, deleting the nine background
entries produces a more positive fitted MoR response in this selected S3 test.
This is a direct between-arm comparison, not a contrast between two separate
significance labels. The hypotheses were frozen before these fresh responses;
selection of MoR/S3 from previous development evidence remains disclosed.

The less model-dependent secondary difference in endpoint probability changes
is+.300, with conservative95% interval[-.447,+.953]. That interval remains
wide and includes zero. It is not a second independent confirmation of the
primary result. Show all rates and their uncertainty alongside fitted slopes.
See [observed-rate figure](fig_01_profile_ablation.png) and
[full numerical report](ABLATION_REPORT.md).

## What this changes

The background profile is now an empirically supported factor affecting the
fitted response, rather than only a speculative explanation. That makes
profile composition worth examining before spending on another complete
ten-parameter battery. The900-call representation confirmation stays paused.

This does **not** identify prompt bandwidth or establish that the ten-entry
profile is incorrectly competing for attention. The nine retained background
values in the full profile are substantive dispositions. Their moderation of
MoR could be a legitimate joint-profile effect. The deletion also changes
prompt length, content, emphasis and the assumptions the model fills in when
traits are unspecified. These explanations remain unresolved.

Nor does the reduced profile pass the original directional criterion: its
observed counts fall from28 at.5 to26 at.7. The full-ten control does meet
that criterion. The monotonicity rule is retained, even though a finite-sample
dip could occur under an underlying monotone response. A steeper fitted slope
is neither automatic validation nor evidence that MoR-only agents are better
ethical agents. High-value saturation also limits further discrimination.

No wording variants were tested. The8/30 paraphrase-equivalence result and
reasoning-audit interpretation are unchanged. No smaller architecture, new
conceptual mapping, phase waiver, or Phase2 launch follows.

## Qualitative check and next diagnostic question

After scoring, inspected fixed call indices1 and2 in all ten cells:20 items,
chosen by index rather than favourable outcome. This is an unblinded inspection,
not a new coding instrument, causal mediation analysis or independent audit.
Full-profile rationales repeatedly refer to procedure, endorsement and human
transition costs. MoR-only rationales often emphasise peer-department evidence
and competitive timing, while some still favour caution. Both arms sometimes
use similar considerations for different decisions. These examples keep
substantive trait interactions plausible; they do not reveal internal causation.
The inspection keys and record hashes are saved separately for review.

The next question should distinguish substantive background conditioning from
presentation effects. A useful design must hold the ten intended traits fixed
when testing presentation, or vary a prespecified background trait at fixed
presentation when testing composition. Merely adding arbitrary filler would
not isolate attention, and selecting whichever small subset produces the
steepest curve would not validate the architecture. Any such control needs its
own exact treatment, hypothesis and budget before collection; no next run is
automatically commissioned by this result.

Current cumulative known usage$3.065874; conservative charge including the
earlier unknown timeout$3.07084125, leaving$5.92915875 from the latest$9
allowance. No pending calls or verified provider account balance. Records and
figures are saved locally; archive verification is not off-device backup.
