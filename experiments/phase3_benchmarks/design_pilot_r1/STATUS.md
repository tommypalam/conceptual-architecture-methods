# One-candidate pilot frozen and ready

The user's CONTINUE releases this next bounded exploratory step after the five
formal recognition rejections. See [PROTOCOL.md](PROTOCOL.md). No full-screen
acceptance or population collection can follow automatically.

Release SHA256:
`7f8681163ceb3d0f52911acaf1fbc24d72c33ce987c8d12e31f3253eaf5998d3`.
Full maximum $0.425814400 under a $0.50 local ceiling, with the same provider and
package caps. There are at most11 calls; actual downstream calls depend on an
independent structural accept and any coding disagreements.

Offline full mock generation/review/N5/dual coding/discussion and zero-call replay
passed. Structural-rejection stopping and failure/no-retry checks passed. The
worst-case input test initially caught double counting of HTTP JSON escaping;
the decoded-content byte check plus1024 framing allowance was corrected and the
affected bound/schema/missingness/oversize tests passed on rerun. Request content,
models, limits and scientific decisions were unchanged by that guard fix.

All650 inherited records and the previous verified archive were checked before
freeze. The new release preserves their exact JSON bytes and the failure-log
prefix. No prior scenario or result is overwritten or pooled into this pilot.

Paid command: `py -3.11 -B code/phase3_design_pilot.py run --yes`.
Zero-call result/archive verification: `py -3.11 -B code/phase3_design_pilot.py verify`.
