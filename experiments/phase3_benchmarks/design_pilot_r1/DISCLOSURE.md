# Concrete pilot awaiting specific paid-disclosure approval

The implementation and frozen cost are complete. Automatic approval review
rejected the paid command before launch because it did not consider OK CONTINUE
specific authorisation for this new experiment's external payloads/destinations.
Do not bypass that rejection. [PRELAUNCH_CHECKPOINT.json](PRELAUNCH_CHECKPOINT.json)
verifies zero new calls/charges, all650 historical records and unchanged sources.

| Recipient | Payload | Purpose |
|---|---|---|
| OpenAI, GPT-5.4 mini | Existing ultimatum operational invariants and frozen drafting instructions | Generate one new scenario |
| Anthropic, Sonnet4.6 | That candidate plus the existing invariant packet | Independent structural review |
| Anthropic, Sonnet4.6 | The accepted candidate plus the existing recognition question | Five exploratory recognition answers |
| Anthropic, Haiku4.5, and OpenAI, GPT-5.4 mini | Those five short answers and the existing all-five rubric | Independent dual coding |
| Same two raters, only if needed | Original short answers and both original rating pairs | One bounded discussion round |

No profiles, participant records, images, credentials, unrelated project files
or previous raw probe answers are included. The candidate is generated content,
so its exact text is not available before the first call. Its generation request
is frozen in [generation_request.json](generation_request.json). Downstream
request composition is frozen in code/phase3_design_pilot.py and source-hashed
in [release.json](release.json). A structural rejection stops before recognition.

Maximum11 calls and **$0.425814400 total additional accounting**, under a $0.50
local ceiling and the existing $15 Claude/$30 OpenAI/$100 package caps. No full
screen, population run, automatic regeneration or retry is included. The N5 pilot
cannot pass the specification's N50 recognition gate.

After explicit approval of these payloads and destinations, run the SAME frozen
command, loading the already configured keys without displaying them:

    py -3.11 -B code/phase3_design_pilot.py run --yes

Then verify with `py -3.11 -B code/phase3_design_pilot.py verify`. Preserve all
existing frozen files and archives. Do not re-prepare or re-test unchanged work
merely to resume after approval.
