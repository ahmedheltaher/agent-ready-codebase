---
name: cut-boilerplate-not-meaning
description: Decide whether a layer, wrapper, interface, base class or file earns its place, and split or merge code only at real boundaries. Use whenever adding or removing a wrapper, interface, factory, service layer or file, inlining a pass-through, flattening a call chain, or when the user says "simplify this", "refactor this", "too many layers", "split this file" or "merge these".
---

# Cut boilerplate, not meaning

Remove structure that adds no behavior and no boundary; keep what carries meaning. For naming rules see `name-things-in-full-words`.

## Trace one behavior first

- Trace one real request (say `POST /orders` in `api/orders.py`) from entry to outcome; a layer can only be judged by what passes through it. Read the bodies of every hop before any verdict; a name or signature cannot show a permission check or a transaction.
- Name the problem, what must stay unchanged and which checks show success; otherwise it is churn.
- Prefer one local, reversible change to a rewrite; it is easy to review and undo.

## Make every layer earn its place

- Keep descriptive names, useful types, units, business rules, error messages with context and comments explaining why; they say what must not break. When deleting a wrapper, move its comments to the remaining code.
- Do not copy shared logic (copies diverge) or build grab-bag types mixing unrelated responsibilities (their purpose is unreadable). The same file copied into several repositories is a copy problem, not a layer problem: diff the copies first, since divergence is the real risk.
- Warning signs: an interface with one implementation and no test substitute, a function forwarding the same inputs, a file that only wires, modifiers restating the default, repeated setup, "manager", "helper" or "impl" chains (interfaces a framework makes you implement do not count: the tool demands them). Reasons to look, not permission to delete.
- Before adding any layer, package or file, name its benefit today: two real implementations, real reuse, a used test substitute, required startup or cleanup, a supported extension point, a stable contract for callers, a separation the build relies on, or one of the split reasons below.
- Reject "cleaner", "the template does this", "we might need it" and a planned second implementation: habits, not problems; an unused layer costs readers now.
- Before deleting a layer, check for permission checks, transactions, retries, validation, transformations, error translation, dependency isolation, error context, startup, cleanup and build requirements; short is not the same as empty.
- Inline a pass-through once confirmed to supply none of those, and prefer a short chain of named functions to a long inheritance chain; both are easier to trace, though keeping a real boundary matters more than fewer file reads.

```text
Before:
place_order_handler → OrderServiceFacade.create (checks caller permission)
  → OrderManagerImpl.create_order → OrderRepository.save → db.insert_order

After:
place_order_handler   validates input
→ require_permission  the facade's permission check, now its own step
→ create_order        pricing rules, opens the transaction
→ insert_order        the single write
Removed: OrderServiceFacade, OrderManagerImpl and OrderRepository.save;
each only forwarded once the permission check moved out.
```

## Split and merge at real boundaries

- Split where two pieces must change separately: separate deployment or release, independent tests, separate owners, conflicting parallel work, or a public-versus-private boundary; never on line or class count. If a split adds mostly imports and wiring, keep the code together.
- Never merge across trust, permission, transaction, data-integrity, public-contract, ownership, deployment or release boundaries; they stop mistakes spreading.
- Do not merge just to save a tool call.
- Put the contract, entry points and a guide to key functions at the top of a long file, since readers miss logic buried in the middle. Match the layout to how the team reviews; if reviewers cannot understand the result, the change moved work instead of removing it.

## Check the result

- Run the tests on the changed path and inspect failure paths; structural edits break edge cases quietly.
- Stop or revert if tests, compatibility, review, parallel work, boundary enforcement or findability gets worse.

## When not to apply

- Public APIs, published libraries, outside callers' contracts and extension points.
- Wrappers enforcing authentication, permissions, trust, transactions or data integrity: often the only enforcement.
- Generated code, layouts a tool requires, and formats exchanged with other systems; tools and consumers you cannot see depend on them.
- Untouched stable code; restructuring costs review without demonstrated benefit.

Measure before claiming a saving; this is reasoned, not measured.
