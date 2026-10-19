---
name: name-things-in-full-words
description: Choose names that say what a thing means, in full real words, for variables, functions, types, fields, events, columns, config keys, enum and status values, and log field keys. Use whenever naming or renaming anything, reviewing names, writing log or event keys, picking status values, or when asked to "shorten", "abbreviate" or "compress" names or keys.
---

# Name things in full words

A name travels to every call site and log line; a comment at the declaration does not. Pick names a stranger can read without a legend, and keep them stable. Case style follows the codebase; `PAYMENT_FAILED` and `payment_failed` are both full words.

## Say what it means

- Name functions, variables, types, fields, events, columns, configuration keys, flags and status values with a short phrase of real words saying what the thing means, does or returns, not the implementation trick behind it. `verify_order_within_balance(order, balance)` tells the reader what is checked; `chk(o, b)` makes them open the body.
- Write enum and status values as words: `payment_declined`, not `PD` or `3`. A code needs a lookup on every read and every search.
- Never shorten a meaningful word to save characters or tokens; cryptic names cost more across the task than they save.
- Avoid padding and misleading names such as `AbstractBaseOrderManagerImpl`. Padding hides the one word that matters; a name promising what the code does not do is worse than a vague one.
- Fix a bad naming pattern before generating more code that copies it; every new use makes the later rename bigger.

```text
Bad                     Good
rc                      retry_count
chk(o, b)               verify_order_within_balance(order, balance)
PD / 3 (status value)   payment_declined
ttl_s                   ttl_seconds
OrderMgrImpl            OrderPlacement
evt=PF o=ord_8f3k2      event=payment_failed order_id=ord_8f3k2
```

Rename for what the code actually does, not for what sounds right.

## One name per concept, everywhere

- Use one stable name per concept across code, error text, events, columns, config keys and documentation; do not alternate between `customer` and `client`. Inconsistent names split searches. Check that a search for the name returns the right hits with little noise.
- Make error text use the same words as the code and event names (`payment_declined` in the exception message, the event name and the status column), so a search for either finds the other.
- When a constant maps to a value (`TIMEOUT = 'GatewayUnavailableError'`), use the same words for both, or a search for one misses the other.
- Spell out service names, event names, reasons and field keys in structured output: `order_id`, `retry_count`, `timeout_seconds`, `reason="insufficient funds"`. Full words carry the meaning and the unit without a legend.
- For codes a contract forces on you, see `write-logs-in-plain-words`.

## Short forms that are fine

- Universal short forms such as `id`, `url`, `http`, `max`, `min`, `io` and `config`, and public codes such as HTTP status numbers and currency codes; expanding them helps nobody.
- Local conventions such as `i`, `ctx` and `err`, only in a tight scope like a loop body or short function, and never in incident-facing keys; familiarity inside the code does not explain a log line to someone outside it.
- Established domain or mathematical notation such as `x`, `dx` or `sigma`, where readers in that field expect it; elsewhere, say it in words.
- Keep any project list of extra accepted short forms tiny and do not grow it by habit; every entry is one more thing each new reader must learn.

## Renaming

- Keep public and externally consumed names stable: library APIs, columns, event names, config keys and schema fields with existing readers. A shorter or prettier name alone does not justify breaking consumers or old queries.
- When a rename is justified, update every use, error string, test and document in the same change, and for a consumed field coordinate writers, readers and queries with a compatible path; a partial rename breaks callers and leaves two names for one concept.

## When not to apply

- Names fixed by a third-party API, wire format, or schema required by law or policy; keep the name and improve the reading view instead.
- Generated symbols nobody reads directly; renaming them is churn.
- A proven hard storage or runtime budget can require compact externally visible names; bring measurements, keep a readable view where possible, and do not extend the exception to ordinary source names.

Measure before claiming a saving; this is reasoned, not measured.
