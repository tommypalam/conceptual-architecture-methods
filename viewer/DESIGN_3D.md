# 3D theatre design

The researcher requested a more immersive, game-like visualiser using the
installed Blender and frontend skills. This is a display upgrade for recorded
Phase 2 groups, with no change to collection, analysis or moral scoring.

## Direction before implementation

The memorable element is an explorable architectural diorama with ceramic
agents. The controls remain quiet and the text remains readable. A council,
boardroom and lab distinguish tasks through setting rather than invented
behaviour. The design uses the Anthropic frontend design workflow and the
Blender-to-GLB export workflow; it retains the existing static app architecture.

Palette: porcelain #fbfcff; mist #dbe7e9; ink #203b50; slate #708491;
choice blue #4476c4; choice amber #c98431. Type: a single humanist sans-serif
stack (Trebuchet MS, Segoe UI, sans-serif), with tabular numerals for readings.
Headings are left aligned; controls use sentence case and specific verbs.

Layout:

```text
PARIA / Simulation rooms     scenario / group / condition      Classic view
┌────────────────────────────────────────────┬────────────────────────────┐
│ Task title                    Camera tools │ Selected agent             │
│                                            │ Full response / profile /  │
│       Explorable 3D room and agents         │ knowledge                  │
│       (two rooms in comparison mode)       │                            │
│                                            │ This round's contributions │
│ Choice tally                  Round events │                            │
├────────────────────────────────────────────┤                            │
│ Play / step / round timeline / speed       │                            │
└────────────────────────────────────────────┴────────────────────────────┘
```

Review against the brief: a marketing hero would waste space; rounded cards
around every object would obscure the room. Use a large canvas, compact
projected name labels and a single inspector. Robot-like figures give agents
an identifiable presence without inventing demographic identities. Physical
placement never encodes profile values or a measured social network.

## Evidence and interaction rules

- Reveal all responses in a round together. No fabricated speaking order.
- Every agent can be selected through both its model/label and an accessible
  HTML control. Full responses and exact prompts remain available.
- Colour a vote ring according to the parsed vote; invalid votes stay neutral.
  Blue/amber are choices, not moral judgements. The CEO is visibly non-voting.
- Animate an adjacent-round vote change only when both votes are valid.
- C3 disclosure arcs represent authenticated disclosures recorded in the audit.
  Newly shared evidence is distinguished from information available at round
  start. An arc is not a claim about causal influence or physical movement.
- C2 lists registered proposals separately from adopted amendments; the incoming
  working plan uses the recorded start-of-round state.
- Comparison uses matched membership and role assignments. One round control
  drives both conversations; a conversation that ended early holds its final
  state with an explicit ended label. No additional responses are fabricated.
- The room geometry and character appearance remain constant across conditions.
- The classic viewer remains available; WebGL failure provides a useful link.
- Respect reduced motion. Rendering stops when idle/hidden where possible;
  cap device pixel ratio, keep meshes compact and assets local.

## Synthetic design review

Linden: animated characters cannot stand for inner ethical understanding; use
recorded choices without moral colours. Osei: preserve simultaneous rounds and
label movement as illustrative. Tanaka: paired playback is an exploration of
two recorded runs, not a new inferential comparison. Renna: separate rendering
from the frozen record adapter so later study formats can be added deliberately.
Okafor: retain the classic viewer, test state timing and fail visibly on missing
data or graphics capability.

Resolution: a separate 3D route consumes the existing verified replay API;
decorative geometry and reversible display state have no path into the frozen
experiment. These perspectives are internal design checks, not external review.

## Implementation review, 2026-09-13

The three dioramas and neutral agent were built in Blender 5.2.1 and exported as
isolated GLBs. An initial export included additional scenes; this was corrected
with active-scene-only export and independently checked in the GLB JSON. Each
final file is checksum-listed. Original scenes and research records were retained.

Browser inspection prompted a fixed-height canvas, a background-matched shadow
plane, larger response text and collision-aware labels with leader lines. The
initial phone view cropped the room and overlapped labels; the final camera
framing and label layout were checked at 390 px. Three task scenes, paired view
and desktop/mobile screenshots were inspected after correction.

Both classic and 3D integration suites passed on the upgraded server. The 3D
suite checks state boundaries, early ending, camera/selection controls, missing
votes, rendering at rest, reduced motion, local-only requests and asset-load
failure. All 300 recordings / 6,205 response rows passed offline reconstruction;
all three invalid votes remain missing. No model calls were made.

Remaining limits: tested in Chromium with emulated viewport sizes, not across
physical phones or every GPU. At extreme orbit/zoom positions a figure can be
occluded; the HTML agent selector remains available. The geometry, leader lines
and animations remain explanatory illustrations. The visualiser introduces no
human comparison, moral score or evidence of ethical understanding.
