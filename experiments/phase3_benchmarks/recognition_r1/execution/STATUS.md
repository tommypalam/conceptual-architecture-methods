# Verified collector; paid dispatch blocked before launch

The researcher instructed START after the $14.06743250 full cost review. The
collector and allocation supplement were completed and frozen in commit
`01e9ec28`. **All65 Phase3 tests pass**, including a complete mock500-probe run,
100 initial coding calls, a triggered discussion round and zero-call replay in
a temporary ledger. Synthetic test responses never entered the research ledger.

The full mock test found and fixed an insertion-order resume bug before freeze:
canonicalized saved ratings could change the JSON field order in a later
discussion prompt. Rating objects are now normalized before composing those
dependent requests, so first execution and disk replay are byte-identical.

Release SHA256:
`e8e1b85ddf73db22a78e1919b7b7d261af15aece04c36627e41f869b1e85beb8`.
The exact500 probes,100 coding calls and up to100 discussion calls remain fixed.
The new explicit allocation supplements the earlier rough stage allocations;
the original policy file,48 paid records and145 historical JSON files are intact.
See [RELEASE.md](RELEASE.md) and [release.json](release.json).

Automatic approval review rejected the command BEFORE process launch. It stated
that the previous approval covered free Anthropic token counting, not paid work
and the expanded screening payload/destinations. It did not accept START after
the cost report as sufficient specific approval. No screening intent, response,
charge, stage manifest or failure record was created. Do not bypass the block.

Required specific disclosure scope: send the ten frozen private scenario bundles
and36 distinct task images to Anthropic for500 recognition probes; send the
resulting short answers to Anthropic/OpenAI for dual coding, and original answers
plus original rating pairs for the bounded discussion. OpenAI coding does NOT
receive the scenario bundles or images. Maximum additional cost $14.06743250,
within the existing $15 Claude/$30 OpenAI/$100 package hard caps.

After that explicit approval, execute the SAME frozen command:

    py -3.11 -B code/phase3_recognition_run.py run --yes

Load the existing Anthropic user-environment key into the process without
printing it. Preserve the OpenAI process key. Do not regenerate stimuli, rerun
quotes, alter frozen sources or retry the old truncated consultation. The runner
enforces one in-flight call, permanent failure records, full-reservation retention
on failure, exact request replay and no automatic retry. No population task is
authorised by this screening release.

Current spending is unchanged: Phase3 $0.41639895; Claude $0.3587892; OpenAI
$0.05760975; package $23.322471975. These are conservative estimates, not balances.
