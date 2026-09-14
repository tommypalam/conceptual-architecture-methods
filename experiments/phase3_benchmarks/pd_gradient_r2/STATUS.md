# pd_gradient_r2: frozen, never dispatched

r2 was prepared and its release frozen, but **no call was ever made under this
designation**. Its collector source required a correction after the freeze, and
the write-once rule forbids overwriting a frozen artifact, so the corrected
version was designated [r3](../pd_gradient_r3/PROTOCOL.md) rather than
re-released here.

r3 carries r2's design unchanged: same tasks, same content hash
`fc244646…`, same seeds, same estimands, same gates, same $3.38861325
reservation. r3 ran its review gate and was rejected; see its
[assessment](../pd_gradient_r3/ASSESSMENT.md).

This folder is preserved as evidence of the freeze and the re-designation.
Cost of this designation: $0.
