# defeasibility_screen_r1 — protocol

**Status: prepared offline; not released.** Programme: [../PROGRAMME.md](../PROGRAMME.md),
Stage 3a. Motivated by [probe_fields_r1](../probe_fields_r1/ASSESSMENT.md): an
invented "keep existing arrangements" field matched PD's effect, so PD may be a
status-quo dial. Exploratory; not part of the submitted thesis.

## Purpose

Learn, for the minimum spend, whether the Stage 3a twin items can carry a profiled
study. Nothing is manipulated and no profile is rendered.

## The items

Each of the seven screened items gets a **twin**: one clause in the situation
states a procedure and that the holder came by the arrangement outside it. Options,
descriptions, consequence texts and payoffs are byte-identical to the base item
(`phase7_defeasibility_items.verify_twins`, content hash
`0e0ff8845877fcc2829bf7bcfea0e25bcec9187ce5020d53ca7d1a37710627a9`). The clause
states facts only: no evaluative word, violation label or modal, enforced in code.

On a twin the two readings of PD predict opposite signs — PROCESS: raising PD
lowers the keep-rate; DIAL: raises it. That test is the NEXT designation, not this
one.

## Run statement

| | |
|---|---|
| Review | 1 call, `claude-sonnet-4-6`. **Hard gate** (new materials): anything but `accept` stops the designation. Not re-run. |
| Screen | 7 twins x 25 unprofiled decisions = 175 calls, `gpt-5.4-mini-2026-03-17`, temperature 1, no profile block, order alternating |
| Configuration | NEUTRAL on all five axes; no agents drawn, no seed needed |
| Cost | $0.675 reserved worst case; about $0.15 expected |

## Rules fixed before collection

- **Usable** = unprofiled keep-share in [0.10, 0.90]. Stricter than the parent
  pool's "modal below 1.00", because the profiled study must be able to move in
  both directions.
- The profiled stage needs **at least 4 usable twins**; otherwise `screen_stop`,
  reported as such.
- Screening is on baseline dispersion only. No twin is reworded and re-screened
  under this designation.
- The outcome is the share choosing the base item's KEEP option. **No twin option
  is morally classified**, here or later.

## What no outcome establishes

Anything about PD. A passed screen shows only that the twins disperse.
