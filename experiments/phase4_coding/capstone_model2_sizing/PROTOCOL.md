# Second-model output sizing probe

16 September 2026. **Sizing only, under $0.50.** Measures how many output tokens
`claude-haiku-4-5-20251001` actually uses on the capstone task format, so the
replication's `max_tokens` can be set from evidence.

`capstone_model2_r1` failed its first call at `max_tokens: 64`, inherited from a
study whose model returns bare JSON. Raising the budget blind to 512 pushed the
worst-case reservation to $6.69, because the guard charges the full output budget
on every call. Neither guessing high nor guessing low is acceptable.

Two agents, four tasks, four arms: 32 calls at `max_tokens: 512`. The measured
distribution of actual output tokens sets the budget for the real run.

No recognition, moral or arm claim is made. Two agents cannot support one, and
these decisions are not used as study data.
