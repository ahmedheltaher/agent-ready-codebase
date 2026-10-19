---
name: commit-messages-that-explain-why
description: Write commit messages and pull-request descriptions that record why a change was made, what was considered, and what was verified. Use whenever committing, squashing, or writing or editing a PR description — including when the user just says "commit this", "write the PR", or "clean up the commit message" — even for small changes.
---

# Commit messages that explain why

The diff shows what changed; the message records why, for whoever reads the history later. Agent-written changes meet the same standard. Write only what is known: an invented rationale misleads more than a blank. Keep the team's existing subject convention (`type(scope): subject (TICKET-123)`); this skill is about what the message says, not its format.

## Write a subject that stands alone

- Write one short, searchable command with the concrete outcome first, because history views show only the subject and truncate it from the right. Prefer `Prevent duplicate charges when Stripe webhooks are retried` to `Fix payment bug` or to a filename the diff already shows.
- Do not leave `fix`, `wip`, or `update` in permanent history; nobody can search or interpret them later.
- Follow the subject with a blank line; most tools treat the first paragraph as the subject.

## Explain the reason in the body

- Open with the problem, symptom, or edge case that triggered the change, the part the diff cannot show.
- Size the body to the change: a 16-line fix needs four or five lines, not a page. Say each thing once; the diff shows the rest.
- Summarize the intended and resulting behavior.
- Say why this approach was chosen, or the next person may undo it.
- Name only alternatives actually considered and why they were rejected; record failed or reverted attempts so nobody retries them.
- State constraints the reader must not break, especially timing, compatibility, release, and safety requirements, which rarely appear in code.
- Say what was deliberately not changed or handled, plus known limitations, risks, and follow-ups with their preconditions; a reader cannot tell a deliberate omission from an oversight.
- Link tickets, but include enough context to grasp the core reason without opening them; links and access fail.
- Label uncertainty ("likely", "not confirmed") so guesses do not become recorded facts.

## Record verification and guide the reviewer

- List the checks actually run (tests, manual checks, replayed traffic) with results, plus duration or coverage when it matters; intended behavior is not verified behavior.
- Distinguish passed, failed, and not run; each supports a different conclusion.
- Name the files to open first and what deserves close checking (permissions, failure paths, transactions, compatibility, data changes, overlapping requests), since those fail off the normal path. For what the reviewer then checks, see `review-before-approving`.

```text
Before:
fix payment bug

After:
Prevent duplicate charges when Stripe webhooks are retried

Stripe redelivers payment_intent.succeeded on timeout; ord_8f3k2 was charged twice.
handle_webhook now returns the ledger entry for the event_id instead of charging again.
Keep that lookup before any charge.
Rejected: dedupe in the queue, which is at-least-once by design.
Verified: test_webhooks.py retry case; one day of replayed staging webhooks, 0 duplicates.
Review first: webhooks.py, then the transaction in ledger.py.
```

## Keep one durable record

- Put the full explanation in the record that survives (the commit, squash commit, or retained PR description), not in temporary commits that will disappear.
- Link supporting detail rather than copying it around; copies drift.
- Keep one record for people and agents; a separate machine-only block doubles upkeep and drifts.
- Do not paste agent transcripts as rationale; the decision drowns in noise.
- Check for secrets, credentials, customer data, and unnecessary personal data; history is hard to scrub.

## When not to apply

- A typo, pure rename, or formatting-only change gets one line, since a body would repeat the subject; do not invent a reason for it. A test-only or docs-only commit needs one line saying what it covers or documents.
- Automated dependency, lockfile, or configuration updates may be brief only after checking behavior and compatibility effects; a small automated diff can still change behavior.
- Work-in-progress commits that will be squashed may omit the body as long as the surviving record carries it; squashing and linking move the explanation, they do not excuse losing it.

Reasoned, not measured; check it against your own team's review time and defect rate.
