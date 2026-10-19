---
name: write-logs-in-plain-words
description: Write log lines, error messages and diagnostic output that a stranger can understand mid-incident without a legend or decoder, while keeping evidence and compatibility. Use whenever adding or changing logs, exceptions, CLI failures or dumps, preparing an incident extract, or reviewing output someone will grep — including when the user just says "add some logging" or "make this error clearer".
---

# Write logs in plain words

Make every log line tell a stranger what happened, to what, and why, without losing evidence or breaking consumers.

## Make each event explain itself

- State the operation, outcome, affected thing, safe inputs and cause; a failure label alone explains nothing.
- Write `cause unknown` when it is, mark guesses, and add a next check only when known ("check available database connections" after a pool timeout); invented explanations misdirect.
- Put stable identifiers on the line as `key=value` (`order_id=ord_8f3k2`) so related events join by search.
- Use one field vocabulary per service (`message`/`event`/`request_id` in every file, not `msg`/`evt` in one and `message`/`event` in another); a severity-plus-event filter silently misses the odd one out.
- Give numbers units (`timeout_seconds=30`) and name what a count counts (`retry_count=3`, not `count=3`); bare numbers are ambiguous.
- Timestamp the reading view as ISO 8601 with offset; keep machine timestamps where required, but never make readers convert.
- One event per line with the stack trace attached beneath, or, in a JSON logger, the Error object or its stack as a field rather than `err.message` alone; a message without a stack is a summary instead of evidence.
- Reserve error severity for failures needing attention, not tracing or expected handled outcomes, or severity filters fail.
- JSON, pipes and `key=value` are fine; unexplained meaning is the problem, not separators. Field keys, event names and status values follow the code-naming rules in `name-things-in-full-words`.

```text
Before:
logger.error({ msg: 'charge.threw', err: err.message })
After:
logger.error({ message: 'card charge threw before the order was marked paid; retry scheduled',
  event: 'CHARGE_FAILED', order_id: 'ord_8f3k2', retry_in_seconds: 30, error: err })
```

## Preserve evidence, protect sensitive data

- No credentials, tokens, secrets or personal data, and only the safe inputs that explain the failure; extras add disclosure risk, not evidence. Correlate with approved stable placeholders (`customer_ref=cus_41a9`) unless full identifiers are approved for the reading view. Identifiers an audit policy requires (client IP, user agent) go only in the audit-tagged record, not in ordinary logs.
- Put a one-line cause summary before the stack trace, never instead of it.
- Keep the exception type and your own code's frames, which locate the failure; trim repeated library frames only when they add nothing, marking each collapse with count and range.
- Never silently drop distinct events or call a filtered extract complete; keep surrounding events, since an isolated failure hides its trigger, and the raw record under access control.
- During an unfamiliar failure retain more, not less; relevance is unknown and volume never excuses discarding clues.

```text
2026-03-14T09:21:07+00:00 ERROR service=payment_service event=charge_failed order_id=ord_8f3k2 cause="gateway timeout" timeout_seconds=30
  GatewayTimeoutError: no response
    at charge_card (payments/gateway.py:142)
    ... 14 library frames (requests, urllib3) omitted ...
    at place_order (api/orders.py:88)
```

## Required codes and large volumes

- Do not invent private event codes, acronyms, status letters or clipped reasons; each adds a decoding step.
- When a contract requires a code, put its meaning on the same line: `status=PD meaning=payment_declined`. A same-file legend may supplement but not replace it, since readers inspect single events and a separate decoder is a dependency that fails.
- Demand demonstrated storage or bandwidth limits before adding a coded view; storage compresses without changing the readable view, and an assumed saving comes back as diagnosis time.
- In a large log, filter by window, severity, identifier or component first, then strip repeated headers and progress noise before touching names, units or causes; mark omissions and keep order so the extract tells no false history.
- Before migrating an existing format, measure the whole task — see `measure-before-shrinking`.

## When not to apply

- Externally fixed protocols, schemas, file formats and audit or legal records are contracts; fix the reading view instead.
- Consumers and public fields that cannot change; readability never justifies breaking them.
- Machine-only metrics with measured storage or bandwidth limits, and hot paths with demonstrated memory, CPU or latency limits; expand before reading, not at write time.

Measure on your own setup; the evidence is one small comparison, not a controlled experiment.
