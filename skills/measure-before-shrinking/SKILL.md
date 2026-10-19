---
name: measure-before-shrinking
description: Measure whole-task cost (tokens, tool calls, retries, time, correctness, human fixes) before adopting a shorter prompt, log, data or file format for an agent. Use whenever someone proposes compressing, abbreviating, encoding, or trimming anything an agent reads — "make this smaller", "save tokens", "add a legend", "compact the logs" — or asks whether such a change paid off.
---

# Measure before shrinking

A smaller file proves only a smaller file. Compact input can shift cost into retries, output chatter, and human fixes, so measure the whole task.

## Decide and set guardrails first

- Before testing, write down the change, the expected benefit, what must not get worse, and limits for usage, time, and human effort; limits set afterwards excuse any result. Correctness is never traded for size.
- Track usage, money, time, and correctness separately; a blended score hides which got worse.

## Cut noise before inventing codes

- Strip repeated headers, banners, decorative formatting, progress bars, and irrelevant duplicates first; safer than codes the agent decodes every turn.
- Collapse duplicates only when repetition is not evidence; otherwise report the count ("same timeout 47 times").
- Omit a default or empty field only when its absence cannot change meaning; missing and default differ.
- Prefer an excerpt, but mark omitted ranges so it never looks complete, and keep a way back to the original (path, line range).
- Preserve descriptive names, units, error reasons, timestamps with an offset, exact cross-reference ids, and the only copy of any constraint, or the reader guesses.
- For unfamiliar failures, keep the untrimmed source reachable; the trimmed view may have dropped the clue.
- When input fits one read, use a format that needs no legend; decoder calls add overhead and can fail elsewhere.
- If codes are unavoidable, put the complete legend in the same read, and count legend, schema, decoder, queries, and failed calls as task cost.
- Consider a decoder only beyond one read, and compare it against plain filtering or paging, which stay readable without tools. Do not assume a break-even size; measure it.

```text
Before (coded):
# Legend: T=time S=severity C=component R=reason O=order
T=1773480067 S=E C=checkout R=timeout O=ord_8f3k2

After (readable):
2026-03-14T09:21:07+00:00 ERROR component=checkout reason="payment gateway timed out" order_id=ord_8f3k2
```

## Run a fair comparison

- Pick several representative tasks with verifiable answers, including one hard case, and define correctness and preserved-evidence checks before running.
- Test at real volume; small-volume results do not predict large ones.
- Hold data, agent settings, task wording, tools, and permissions steady; record unavoidable differences such as an added decoder.
- Use a fresh, isolated session for every run, randomize condition order, and repeat each condition several times, because run-to-run variation is large. Run tasks that modify data on safe copies.
- Record correctness, input size, and usage split into input, output, cached, reasoning if the provider reports it, and tool traffic, plus errors, retries, time, cost, and human fixes. Do not invent or double-count categories.
- Keep failed runs; report typical results and spread, not the best run.

Shape of the record to keep (illustrative numbers, not a measurement):

```text
Task: why did ord_8f3k2 fail? (median of 5 runs, illustrative)

format        correct  in_tok  out_tok  tool_calls  retries  seconds  human_fixes
readable      5/5      18.2k   1.1k     4           0        41       0
coded+legend  4/5      12.6k   2.9k     9           2        78       1
```

## Watch hidden costs and decide

- The agent explaining its decoding, asking what a code means, repeating lookups, or taking extra turns means the format makes the job harder.
- If both formats answer everything correctly, say you measured cost, not quality.
- Adopt only when typical results meet the pre-set limits at real volume and the saving pays for evaluation and upkeep; if differences are unstable, run more trials or keep readable.
- Record the decision, volume, run count, typical results, and spread; re-measure when the agent, tools, or volume change.

## When not to apply

- Tiny inputs, one-off tasks, or trivial reversible edits: evaluation costs more than the saving; keep the readable form and claim no gain.
- Machine-only payloads, deterministic parsers, storage or network compression, and browser delivery budgets; this applies only to what the agent reads.
- When input exceeds the context, filtering, paging, or summarising is unavoidable; compare those rather than skipping evaluation.

One small experiment found the coded format smaller but the whole debugging task costlier; a reason to measure, not a law.
