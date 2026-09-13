# Revised packet: specific destination approval required

The implementation, candidate, exact requests, tests and budget freeze are complete.
Automatic approval review blocked the paid command before launch. It acknowledged
that approve continue authorises the continuation in substance, but required specific
authorisation for this revised payload to Anthropic/OpenAI. No calls or charges
occurred; [PRELAUNCH_CHECKPOINT.json](PRELAUNCH_CHECKPOINT.json) verifies652 preserved
records, unchanged sources and zero continuation spending. Do not bypass the block.

The specific approval covers:

- Send the [clarified six-task packet](candidate.json) and existing operational
  invariants to Anthropic/Sonnet4.6 for one independent structural review. The exact
  request is [review_request.json](review_request.json).
- If accepted, send that full packet and the existing recognition question to
  Anthropic/Sonnet4.6 for five probes. Exact [requests](recognition_requests.json)
  are saved; no profile, context, previous answer or recommended verdict is supplied.
- Send the five resulting answers to Anthropic/Haiku4.5 and OpenAI/GPT-5.4 mini for
  independent coding, and the answers plus original rating pairs to those same
  raters for one bounded discussion only if needed.

No generation call, image, participant record, credential or unrelated project file
is sent. The packet preserves the original token-allocation rule and makes the
one-proposer/five-responder schedule explicit. It is a disclosed local repair,
not an already accepted low-recognition scenario.

Maximum new accounting **$0.411347200**. Including the stopped attempt, maximum
combined accounting **$0.415707325**, within the already approved $0.425814400 ceiling
and $15 Claude/$30 OpenAI/$100 package caps. No full screen or population run.

After explicit approval of this revised packet and these destinations, execute
the SAME frozen command with the configured keys, without printing credentials:

    py -3.11 -B code/phase3_design_pilot_r2.py run --yes

Verify afterward with `py -3.11 -B code/phase3_design_pilot_r2.py verify`.
No redesign, repeated generation, fresh quote or repeat of unchanged tests is needed.
