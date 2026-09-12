# Phase 1.5: researcher-accepted closure

Decision date: 12 September 2026. Development branch: `phase1-5-all-ten-criteria`.

**Phase 1.5 is closed for the revised, limited research objective: evidence that explicit normative parameters can begin to shape AI decision generation.** The researcher accepted this interpretation and instructed the project to proceed. This follows the explicit clarification that passing the original gate is no longer the research priority.

This is an accepted change in the scope of the conclusion after observing the results. It is not a retrospective pass of the original battery, a preregistered replacement criterion, or a declaration of a thesis section 8.2 full/partial pass. The original gate remains unmet. The earlier rejected closure and the later accepted decision are distinct; this document records the latter.

## Supported conclusion

> In the tested model, harness and dilemmas, explicit normative profiles can systematically influence generated decisions. Replicated Procedural Dependence effects provide an initial demonstration of functional normative parameterization, with substantial limits on generality and representation robustness.

The profile enters the request before generation. The application stores the raw response and extracts its decision label without substituting an ethically preferred answer. This identifies the location of the intervention in the application. It does not identify the model's internal mechanism or remove the possible contribution of provider-side alignment. Ethical understanding, persistent internalization, moral improvement and AGI are not established.

## Evidence retained at closure

| Evidence | Result and interpretation | Source |
|---|---|---|
| Independent PD confirmation | Neutral context; 25 new backgrounds, 100 valid responses. PD .1 to .9 increased S2 FORMAL_REPORT by 80 percentage points (simultaneous 95% CI 35.4 to 95.2) and S3 WAIT by 68 points (22.9 to 88.2). Both prospectively specified contrasts passed Holm-adjusted exact tests. Draw/schedule seeds 20261012/20261013. | [Confirmation](structural_encoding_20260912/pd_confirmation/analysis/REPORT.md) |
| Later all-ten follow-up | Neutral context; 50 backgrounds, first 25 for gradients. Canonical PD endpoints and verbal PD endpoints/interiors on both dilemmas survive the prespecified Holm180 sensitivity analysis. Canonical PD observed curves are ordered. Draw/schedule/analysis seeds 20261020/20261021/20261022. | [All-ten assessment](all_ten_assessment_20260912/ASSESSMENT.md) |
| Explanation recovery | Separate 200-item audit: PD active accuracy 11/20, supplementary Holm10 p=.03. Brief self-explanations and repeated-background dependence limit the inference; aggregate audit thresholds fail. | [Audit](structural_encoding_20260912/audit_schema_r3/analysis/REPORT.md) |
| Contrary and unresolved findings | All ten parameters remain reported. Numeric RT/S3 opposes its predicted sign; MS lacks an ordered canonical curve. Broad wording equivalence and representation retention are not established. | [Complete parameter table](all_ten_assessment_20260912/ASSESSMENT.md) |

The confirmation used previously studied dilemmas with new backgrounds; it is not unseen-task transfer. S3 WAIT can reflect caution as well as procedural concern. Neither action is assumed morally superior. Canonical endpoints vary numbers under fixed descriptions; verbal comparisons also vary the verbal profile expression.

The original 39,000-response battery established 8/30 paraphrase cells against 24 required. The later fresh-profile study established 1/30 under its conservative paired calculation (25 complete cells, five incomplete), with 3/30 in the independent-TOST sensitivity. These are different estimands and methods. Failure to establish equivalence is not proof of non-equivalence, although earlier experiments also documented substantial actual wording divergence. The fresh study's two eligible legacy MoR representation comparisons failed; PD was ineligible under that original prediction rule, not thereby empirically disproved.

The final allocation dispatched 17,250 requests, saving 17,247 records with 17,234 valid responses. Ten parse failures, three recorded API failures and three unresolved dispatches remain explicit. The frozen complete-data bootstrap is unavailable; the prespecified exact paired sensitivity retains all 180 contrasts, including eight incomplete contrasts assigned p=1. No missing observation was silently replaced.

## Consequences and next work

- Finish the thesis account using this scoped positive conclusion and the complete mixed record. The all-ten results remain visible; no parameter is removed from the architecture.
- Stop additional Phase 1.5 collection. No paid calls are queued. Latest tracked package accounting is $22.66401475 against $25, including unknown-charge bounds; this is not total lifetime project spending.
- Preserve frozen protocols, raw responses, seeds, archives, thresholds, theory, distributions and locked questions. Same-computer archives are verified; off-device backup is not established.
- Prepare downstream scope and analysis offline. The original full-architecture Phase 2 study is not scientifically validated by this closure. Any revised empirical study needs a concrete scope, appropriate validation and its own frozen protocol. The planned moral-scoring manual and analysis preregistration remain pending; no new coding rules or parameter-to-action mappings are introduced here.

The [thesis results draft](../../docs/phase1_5_results.md) and [updated abstract](../../docs/abstract.md) carry this conclusion into the manuscript. [NEXT_STEPS.md](../../NEXT_STEPS.md) owns current execution status.

Five synthetic review perspectives are preserved in the [archived decision history](../../archive/shared/documents/meta_through_scoped_closure_2026-09-12.md). They are an internal structured review, not external expert endorsement or supervisor approval.
