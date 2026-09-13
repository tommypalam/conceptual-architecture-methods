# Initial Phase 3 source audit

Checked 2026-09-13. This is a source-to-measure audit, not a completed literature
review or a validated human reference dataset. Full-text access limits are explicit.
No historical rates are inserted into agent prompts.

| Benchmark | Inspected primary research source | What is supported / still unresolved |
|---|---|---|
| Authority | [Milgram 1963, original article](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/Milgrim_1963_Behavioral_study_of_obedience.pdf) | The original procedure escalates an aversive intervention. A single vignette response must not be treated as an observed full escalation trajectory. Exact variant-specific targets and modern synthesis extraction remain pending. |
| Loyalty | [Asch 1956 DOI](https://doi.org/10.1037/h0093718) | Bibliographic record located; the attempted public PDF resolved to an unrelated website and the DOI full text was unavailable through the browser. No new precise human rate is verified here. The thesis and spec also give different conformity bands; resolve the intended critical-trial dataset. |
| Justice | [Oosterbeek, Sloof and van de Kuilen, authors' March 2003 manuscript](https://econwpa.ub.uni-muenchen.de/econ-wp/exp/papers/0401/0401003.pdf) | Reports mean offer around 40% and overall rejection around 16%; overall rejection is not rejection conditional on a 20% offer. The manuscript excludes hypothetical-payoff studies. A claim about Western-specific 45-50% offers needs its own matching evidence. |
| Care | [Fischer et al. 2011, publication abstract](https://pubmed.ncbi.nlm.nih.gov/21534650/) | Reports 105 independent effect sizes, over 7,700 participants, g=-.35 and danger/cost moderators. It does not by itself establish a universal 75%/55% pair for a chosen procedure. |
| Freedom | [Rains 2013, publisher abstract](https://doi.org/10.1111/j.1468-2958.2012.01443.x) | Reports K=20 and N=4,942, not the thesis's 123 studies. The outcome concerns competing reactance models with anger/counterargument indicators. A source-matched adjacent-option probability target remains unverified. |

Additional original-study records located for procedure selection:
[Darley and Latane 1968, diffusion of responsibility](https://pubmed.ncbi.nlm.nih.gov/5645600/),
[Latane and Darley 1968, group inhibition](https://pubmed.ncbi.nlm.nih.gov/5704479/),
and [Hammock and Brehm 1966, eliminated choice](https://onlinelibrary.wiley.com/doi/10.1111/j.1467-6494.1966.tb02370.x).
These locate relevant paradigms; they are not substituted for the thesis's exact
Worchel/Brehm reference or a full-text quantitative extraction.

A simulated response is not a directly observed human action. Preserve the unit,
population, procedure, incentive, uncertainty and denominator of each comparison.
Do not mix a study's participant-level prevalence with its trial-level response
rate, or use a standardized effect size as a probability difference without an
explicit conversion model and baseline.
