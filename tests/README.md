# Offline tests

Seventy-one Python test modules plus two browser suites. **No test makes an API
call.** They verify implementation behaviour and provenance safeguards, not
scientific or moral validity.

[Back to the project](../README.md) · [Code guide](../code/README.md)

## Run them

```powershell
python -B -m pytest tests -q -p no:cacheprovider
```

The full suite takes several minutes. Target a single area while working:

```powershell
python -B -m pytest tests/test_phase5_reanalysis.py -q -p no:cacheprovider
python -B -m pytest tests -q -k phase3 -p no:cacheprovider
```

The two `.cjs` files are browser checks for the replay viewer, run separately
against a locally served viewer — see [viewer/README.md](../viewer/README.md).

## What the groups cover

| Prefix | Count | Covers |
|---|---:|---|
| `test_phase3_*` | 22 | Benchmark stimuli, recognition transport, budget guards, diagnostics |
| `test_validity_*` | 14 | Encoding-validity analysis paths and aggregation |
| `test_phase4_*` | 5 | Moral schema, rule maps, deterministic classification |
| `test_structural_*` | 5 | Structural package assembly and reporting |
| `test_phase2_*` | 4 | Confirmation collector, preflight, group field parsing |
| `test_all_ten_*` | 3 | All-ten-parameter follow-up and continuation paths |
| `test_repetition_*`, `test_repeat_*` | 4 | Replay determinism and record reuse |
| others | — | Profiles, seeds, PD interaction, project layout, tooling |

## What they protect

The safeguards these tests cover are the reason the project's provenance claims
hold. Treat a failure here as blocking:

- **Write-once records.** A per-call record is never rewritten or retried in place.
- **Strict parsing.** Wrong, duplicate, missing or reordered item IDs fail the
  batch rather than being partially salvaged.
- **Budget and size guards.** A run cannot exceed its frozen cost reservation.
- **Source-hash guards.** A stale review packet or edited frozen source is caught
  before any paid launch. This has already prevented one live mis-launch.
- **Zero-call replay.** Completed studies reproduce from local records with no
  network access.
- **Historical preservation.** Failure records and stopped screens stay intact.

## Conventions

New tests use `test_<area>_<behaviour>.py` and stay offline — mock the provider
client rather than reaching a network. Existing test filenames are stable because
frozen protocols and assessments reference them by name; do not rename them for
tidiness.

A passing suite establishes that the software behaves as specified. It does not
establish encoding validity, ethical understanding or moral correctness.
