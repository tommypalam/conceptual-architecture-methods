# Precollection verification

2026-09-13, branch `phase2-design-20260912`.

Twenty confirmation regression checks and five independent-field parser checks
passed before paid collection. Checks cover fresh allocation and matched groups,
neutral prompts and role reinjection, unchanged individual messages, complete
voting rules, deterministic ties, independent evidence disclosure and round
barriers, valid CEO adoption and invalid reference handling, refusal/truncation,
write-once records, replay identity, orphan/corruption/lock detection, reservation
before dispatch, and failure charges retained on halt.

Analysis checks cover exact paired contrasts and Holm ordering, missing-pair
handling, nondegenerate unanimous-outcome intervals, symmetry, and interval
coverage by enumerating all discordance outcomes at N=8 under six probability
scenarios including boundaries. Conservative coverage follows from the union
bound over exact binomial marginal limits; enumeration is a numerical check.

Population: 400 profiles, ten columns, no missing values or filtering. The
unchanged correlation matrix minimum eigenvalue is 0.3114080941511761. Exact
profile vectors do not overlap the 50-profile exploratory population.

Manifest: `2290a0e2e4d11770ebc0c879bc63951b6ae51ecdbbf31e15b96e32dc9fa3ba5a`.
Population content hash: `72ff60b570ef45623ab0c26e675c316cb34b4976917862331332cc101f87363a`.
Schedule hash: `98c45b719a1b1a051802ffa36d98c38b571b750ba022750f5fbc3193da9964ec`.

Full mock run: 12,375 synthetic responses, all 4,800 individual slots and 300
group runs executed. Reconstructing every request and group trajectory required
zero new mock calls. Final offline analysis passed with complete allocation,
4,800 valid individual and 7,575 valid group responses, no API/integrity/usage
errors, and CLI exit 0. The frozen manifest then verified unchanged.
Mock accounting is synthetic and incurs no API charges. Group/round/state-hash
columns are intentionally absent for all 4,800 individual rows; these are
structural missing fields, not lost outcomes.

The preflight group power scenarios underline the limited secondary design:
at N=20 and conservative alpha .05/7, power is .030 for a 20-point difference
with .40 discordance; .333 for a 40-point difference with .50 discordance;
and .943 for a 60-point difference with .60 discordance. Group non-rejection
therefore cannot establish equivalence or absence of an encoding effect.
