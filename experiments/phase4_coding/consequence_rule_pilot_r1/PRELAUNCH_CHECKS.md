# Prelaunch checks

14 September 2026. All five offline tests passed (211.621 seconds): exhaustive
authored vectors for all twelve actions; balanced labels, matched controls and
budget; missing/duplicate/invalid decisions and analysis; full mocked collection
plus zero-call replay and preservation; malformed review stops before participants.

Command: `py -3.11 -B -m unittest discover -s tests -p test_phase4_consequence_rule_pilot.py -v`.

An earlier offline attempt correctly rejected stale source hashes after the
review packet was expanded to include the scoped definitions. Its unused manifests
are retained in prelaunch_attempt_01. No paid request used that attempt. The
subsequent prepared release and full tests above passed without changing any
previously collected source, response or rating.

Frozen full reservation: $0.584697300 for at most 97 calls. Adding all $1.218321225
prior screening charges gives $1.803018525 within the same $4 development ceiling.
This tests implementation and preservation; it is not moral validation.
