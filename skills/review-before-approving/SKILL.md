---
name: review-before-approving
description: Review a pull request or diff before approving: check that stated intent matches the code, tests exercise behavior, and the change is small enough to verify. Use whenever asked to review, approve or merge a change, the agent's own included, or split a large PR — or when the user says "is this ready to merge" or "look over this diff".
---

# Review before approving

Approval means a reviewer could verify the change, not that it looked plausible. Apply the same standard to human-written and agent-written code: both need an inspectable reason and a diff a person can check in full.

## Keep changes reviewable

- If the PR states no target (intended behavior, what stays unchanged, checks), read the diff, then ask for one with specific questions; there is nothing to compare the diff against otherwise.
- Keep each change small enough to understand and verify in one sitting; overloaded reviews miss details.
- Separate unrelated changes and mechanical cleanup (renames, formatting, import sorting) from the behavior change, so noise does not hide the decision.
- Keep dependent edits together when splitting them would hide how correctness is preserved; the reviewer must see the whole fix to judge it. A migration and the code that reads the new column belong in one change.
- Judge size by whether a reviewer can verify the decision, not by line or file count. A 400-line generated fixture is easy; a 20-line change to lock ordering is not.
- Split or rework any change that cannot be reviewed with confidence, rather than hoping the reviewer will manage.

## What to check before approving

- Confirm the stated intent matches the diff and the checks cover the intended behavior; descriptions omit and misstate.
- Inspect unexplained changes, unrelated edits, omitted edge cases, and behavior that was supposed to stay unchanged, because unexplained edits hide regressions.
- Check that new tests exercise behavior rather than mirror the implementation. A test asserting `charge.assert_called_once()` passes for the wrong reason when the bug is which event id was looked up.
- Check the diff is complete: a new import needs its dependency and lockfile change; a new env flag needs its config and docs.
- Follow the change past the repo boundary: if correctness depends on a template, consumer or service you cannot see, ask for that evidence (a link, a screenshot, a before/after).
- Inspect new fallbacks and error paths the fix introduces; a `?? default` that can never trigger, or that throws on the input it guards, is a bug the happy path hides.
- Send back a non-trivial change whose retained record has no explanatory body; a reason added later is a reconstruction, not a record. For what that body should contain, see `commit-messages-that-explain-why`.
- If the change touches permissions, data integrity or public contracts and you do not know that domain, pull in someone who does before approving; failures there reach other users and systems.

## Do not approve on these alone

- A fluent explanation. Prose is cheap to generate and does not show the code does what it says.
- Agent confidence. Confidence is a tone, not evidence.
- Passing tests. Tests prove only what they assert, and the same agent may have written both the code and the tests.
- Fast generation. Speed says nothing about correctness, and fast generation can hide slow review.

## Example

```text
PR #412 "Prevent duplicate charges when Stripe webhooks are retried"

Reviewer: Sending this back. The description says handle_webhook
reuses the ledger entry for a repeated event_id, but the diff also
changes the retry backoff in payments/client.py with no mention.
The new test asserts charge() is called once but never sends the
same event twice, so it would pass without the fix. Please drop or
explain the backoff change and add a test that replays the event.
```

This works because it names three concrete, fixable problems, none a matter of taste, so the author can act without a discussion.

## When not to apply

- A one-line typo, rename, or formatting-only change needs a glance, not the full checklist.
- Automated dependency and lockfile updates need a behavior and compatibility check, not an intent statement.
- Throwaway spikes and prototypes that will never merge; review the version that will.

Reasoned, not measured; check it against your team's defect rate.
