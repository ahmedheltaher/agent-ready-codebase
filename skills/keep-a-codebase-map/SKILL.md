---
name: keep-a-codebase-map
description: Write and maintain a short committed CODEMAP.md listing entry points, area responsibilities, and main call flows so agents and newcomers stop spending several file reads finding where things live. Use when asked to "map the repo", "document the structure", "add a codemap", "where does X live", "explain the architecture".
---

# Keep a codebase map

A codebase map is one short committed file; orientation then costs one read.

## Decide whether a map is needed

- Write one only when finding entry points, flows or responsible files repeatedly costs several reads; otherwise it is more text to skip.
- Check whether the README or another overview already answers; a second document drifts.
- Name an owner for the map and each section; unowned text goes stale.

## What goes in

- One paragraph on what the repository does, plus owner and last-verified date, so readers judge freshness.
- Entry points with exact paths and function names: servers, binaries, CLI commands, scheduled jobs, event handlers, workers, and the test runner, or the root module whose import list wires the app; list servers and workers separately so nobody starts the wrong process.
- One line per area behind a recurring question: what belongs and what does not; every line is read again later.
- Main flows as call chains, `path:function → path:function`, every step a real location. Label conditional branches; readers must not follow a step that may not run. Mark async boundaries where a chain stops and a consumer resumes it (`⇢ topic orders.events ⇢ jobs/worker.py:handle_order_placed`); a plain arrow implies a synchronous call. Add one line for steps every request passes through (auth guards, validation pipes), since they appear in no single chain.
- Where configuration, tests, migrations, schemas, generated output, shared contracts, important state and external I/O live; these are easy to miss.
- "Do not edit" only for a real generation or ownership constraint; a false warning hides files people should change.
- One file at a stable root path such as `CODEMAP.md`, linked (not pasted) from README and `AGENTS.md`, not force-loaded every session; routine edits need no navigation.
- Omit bodies, imports, type definitions and anything a tree view or one search answers; they duplicate the source and rot first. Paths and names, not line numbers, which break on the next edit.

## Example

```text
Purpose: takes customer orders over HTTP, charges cards, emails receipts.
Owner: orders team (#orders-dev). Last verified: 2026-03-14.
Entry points
- HTTP server: api/app.py:create_app (routes in api/orders.py)
- Worker: jobs/worker.py:run — consumes queue `orders.events`
- Tests: `pytest tests/`
Areas
- api/ — HTTP handlers and request validation only; no business rules.
- orders/ — order lifecycle (place, cancel, refund); owns the orders tables.
- payments/ — card charging and refunds via Stripe; no order state.
- jobs/ — `orders.events` consumers (receipt email) and the nightly reconciliation job; no HTTP handlers.
Flows
- Every request: api/app.py:auth_guard → api/app.py:validate_body before any handler.
- Place order: api/orders.py:place_order → orders/place.py:place_order → payments/charge.py:charge_card → orders/store.py:save_order ⇢ topic orders.events ⇢ jobs/worker.py:handle_order_placed
- Refund: api/orders.py:refund_order → orders/refund.py:refund → [only if order.paid] payments/refund.py:refund_charge → orders/store.py:save_order
Locations: config/settings.py; migrations/; orders/schemas.py; payments/_generated/ (generated, do not edit; `make stripe-client`); I/O: Postgres orders/store.py, Stripe payments/client.py, SMTP jobs/email.py.
```

## Verify, then update or delete

- Open the source before editing; the map can name the wrong file.
- While drafting, mark every pointer you inferred but did not open with `(?)` and say so at the top; remove the markers only after opening the files.
- If the README already describes a structure that no longer exists, fix or delete that paragraph in the same change and link the map from it; two wrong documents are worse than one.
- Scripts may generate path lists and CI may check that paths exist; a person verifies responsibilities and relationships in review, since scripts invent plausible ones.
- Update the map in the same change that moves or renames anything mapped; a later pass never happens.
- Refresh the last-verified date only after checking; a fresh date on unchecked text is false assurance.
- Prune rather than grow; fix or remove a known wrong pointer immediately.
- Delete it, with its incoming links, when ownership lapses or other maintained navigation replaces it.

## When not to apply

- Small repositories whose tree already shows the structure.
- Daily-changing prototypes; the map is wrong before anyone uses it.
- Teams that will not assign an owner or enforce updates in review.

Reasoned, not measured; compare tasks with and without the map, counting upkeep.
