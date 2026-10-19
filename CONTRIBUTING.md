# Contributing

The repo's point is "cut filler, keep meaning", so these rules keep skills short and honest.

## Shape of a skill

- One folder per skill under `skills/`, containing a single `SKILL.md`.
- Frontmatter has only `name` (equal to the folder name) and `description`. Frontmatter values are single-line. The description is at most 60 words and says what the skill does and when to use it; it is all the agent sees before loading.
- The body is 350–650 words as counted by `scripts/check.py` (it ignores bare symbols such as `→`): the goal, the rules, then a short "When not to apply" section.
- Every rule carries its reason, in the same sentence or the next; reasons let a model generalise.
- Examples are concrete (`order_id=ord_8f3k2`, `api/orders.py`), not placeholders; models imitate examples.
- No glossary and no "when to use" section in the body; that is the description's job.
- A rule shared by several skills lives in one owner skill. Others point to it in one sentence and do not restate it.

## Before opening a pull request

Run `python3 scripts/check.py`; it enforces the frontmatter, length, heading and cross-reference rules; the rest is reviewed by hand. CI runs it too.

A PR adding a skill should say in its description what evidence backs it: measured (how, on what) or reasoned.
