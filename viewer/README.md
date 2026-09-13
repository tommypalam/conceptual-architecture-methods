# PARIA simulation theatre

A local visual replay of the **completed Phase 2 confirmation**, with all 300
recorded group runs. No new generations, profile changes or API spending.

From the repository root, run:

```powershell
py -3.11 -B code/serve_replay.py
```

Open **http://127.0.0.1:8765**. Stop the server with Ctrl+C. Use `--port 8766`
if another process occupies the default port. The launcher uses the existing
Python research dependencies (NumPy/SciPy) and, if present, the local
`output/phase2_runtime` target. The UI needs no JavaScript installation,
build step, remote fonts or external web service.

The original local raw data under `data/raw/phase2_confirmation_20260913`
must be present, including `records`, `dispatches` and `groups`. A Git clone
alone does not contain these records. Missing or inconsistent data produces
an error; the viewer cannot collect replacement responses.

## Explore the 3D rooms

Open **http://127.0.0.1:8765/lab** for the Blender-built rooms. The current desktop
session runs the upgraded server at **http://127.0.0.1:8766/lab**; the earlier
classic server uses 8765. Restart a server after adding static files, because its
asset allowlist is constructed at startup.

The council, boardroom and laboratory each have an original Blender diorama
with selectable ceramic figures. Drag to orbit, scroll or pinch to zoom, or use
Top view and Reset view. Agent buttons provide the same inspection without
requiring a click on the 3D model. Small leader lines keep projected labels
readable when they would otherwise overlap.

Press Play or select a numbered round. Inspect a selected agent's complete
response, ten-coordinate profile, information available at that round, exact
incoming prompt and record provenance. Vote changes pulse briefly; C3 evidence
cards travel toward the shared bench only for newly authenticated disclosures.
These animations are illustrative and reveal no speaking order.

Compare conditions opens two matched conversations with a shared round control.
An early-ending conversation holds its final recorded state and says when it
ended. Select an agent in either room to inspect that conversation. Comparison
is exploratory; it does not add a statistical test. A run's URL fragment can be
bookmarked, but camera, comparison and playback state are not persisted.

The 3D view requires WebGL 2. The classic link remains available if graphics or
asset loading fails. Reduced motion disables the disclosure and vote pulses;
both rooms stop rendering when idle, and playback pauses when the tab is hidden.
All code and assets load locally. Browser checks emulate phone sizes, not
physical devices.

### Blender assets and maintenance

`build_assets.py` generated four original GLB assets using Blender 5.2.1 LTS;
no downloaded models, paid assets or generated textures are involved. Each GLB
contains exactly its intended scene. Byte sizes and SHA-256 checksums are in
`assets/manifest.json`; the four files total about 2.25 MB. The editable project
is retained locally at `output/paria_dioramas.blend` and is not committed.

Playback does not require Blender or its addon. To make a fresh asset set,
execute `build_assets.py` in Blender with `PARIA_ROOT` set to a separate output
root. It creates new scenes and refuses to overwrite existing generated assets
or a project. Inspect exports before replacing a versioned asset set. The live
Blender connection used during development is a separate local setup; a Git
clone does not install or configure that addon.

Three.js 0.186.0 is vendored under its MIT licence in `vendor/three/`. See
`vendor/README.md` for the four local import substitutions. The design and
synthetic review are recorded in [DESIGN_3D.md](DESIGN_3D.md).

Run the additional offline browser checks against a running upgraded server:

```powershell
node tests/check_theatre3d.cjs <path-to-playwright-module> http://127.0.0.1:8766
```

On 2026-09-13 these passed at 1440 px and 390 px: GLB isolation/checksums,
selection, camera controls, complete prompts, profile omission, matched
comparison and early ending, amendment/evidence boundaries, invalid votes,
playback, idle rendering, reduced motion, local-only requests, mobile label
layout and asset-failure fallback. Screenshots of all three rooms and comparison
were visually inspected; browser errors were zero. The classic browser suite
also passed on the updated server, and all 300 runs / 6,205 rows passed a fresh
offline reconstruction with all three invalid votes retained and zero API calls.

## Watching a run in the classic viewer

- Select one of three scenarios, one of 20 matched groups, and one of five
  profile/context conditions. The condition selector keeps the current round
  where possible, to make switching between matched runs easier.
- Press Play or step through rounds. The slider supports rewind and replay.
  Space and left/right arrows also work outside focused interactive controls.
- Click an agent to inspect its fixed ten-coordinate LPM profile. In the
  context-only and neutral conditions, the profile is explicitly labelled as
  **not supplied** to that agent.
- Click a dialogue card for the complete raw response, exact incoming prompt,
  record path and checksum. The card preview is shortened for readability;
  peers actually received the saved structured excerpts, not these full texts.
- Use Knowledge and Shared state to follow private evidence and public
  disclosures in C3, or registered and adopted amendments in C2.
- Expand the comparison and load the five final outcomes for the same group.
  This deliberately reveals the ending. URL fragments bookmark individual runs.

The three starting examples are selected illustrations, not representative
samples or additional statistical findings. All group runs are available.

## What the visual means

Round steps reveal simultaneous responses together. Agent seating and the brief
vote-change animation are schematic; they do not represent physical actions,
speaking order, elapsed deliberation time or measured influence between agents.
Blue and amber distinguish the two choices without assigning moral value.
An adjacent-round change is marked only when both votes are valid.

C2 excludes the CEO from vote totals. Proposals and adopted amendments are
separate; only amendments adopted before a round are part of the incoming
working plan for that round. C3 distinguishes public evidence at round start
from disclosures that become public for the next round. Authenticating an
evidence ID does not validate an agent's interpretation of it.

This is a replay tool, not a live simulation engine. Future studies can add a
separate adapter to supply the same display structure. Their recording formats
and interaction rules must be reviewed before claiming live support. The
completed Phase 2 collector, parser, state logic and records are unchanged.

## Verification

The reader checks frozen source hashes and population/schedule hashes. Each
requested replay verifies record envelopes, dispatch links, exact incoming
messages and state hashes; it runs the frozen pure state transition and checks
the reconstructed final state and outcome against the saved group artifact.
It never instantiates a collector ledger or API client. Its HTTP server binds
only to loopback and serves allowlisted assets and read-only JSON routes.

On 2026-09-13, all **300 runs / 6,205 response rows** passed reconstruction.
All **three missing/ambiguous intermediate votes** remain missing. Final
outcomes agree with the saved artifacts. Zero API calls were made.

Repeat the full offline check with:

```powershell
py -3.11 -B code/serve_replay.py --verify-all
```

Browser integration checks passed at desktop (1440 px) and mobile (390 px)
widths: playback, full prompt inspection, omitted-profile labelling, CEO vote
exclusion, amendment adoption across the round boundary, evidence visibility,
all five comparison conditions, invalid vote retention and read-only routes.
Screenshots were visually inspected; browser errors: zero. The check script
accepts an existing Playwright or playwright-core module location:

```powershell
node tests/check_replay_viewer.cjs <path-to-playwright-module>
```

The test script writes screenshots and its report under ignored `output/`.
The scientific data and frozen manifest are not modified by either check.

## Design review

Decision: add a read-only theatre alongside the frozen experiment, with recorded
round boundaries and no inferred actions. These are synthetic review
perspectives, not external review or human validation.

- Linden: profiles and dialogue must not be presented as proof of ethical
  understanding; choice colours carry no moral scoring.
- Osei: schematic seating and playback must not imply human conversation or
  causal peer influence; simultaneous rounds are explicit.
- Tanaka: every group remains browsable; selected examples and final-outcome
  comparisons must not masquerade as population estimates.
- Renna: a separate adapter preserves the current evidence while leaving a path
  to later study formats; future live support remains unimplemented.
- Okafor: reuse verified pure transitions, check saved states and fail visibly
  on missing data; never invoke the collector for a replay.

The principal tradeoff is an engaging presentation versus implied behaviour
that was never measured. The resolution is round-based playback of actual
responses, explicit visual conventions, and inspectable original inputs.
