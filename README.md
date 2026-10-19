# agent-ready-codebase

Seven short, independent Agent Skills for making a codebase easier to work in when AI coding agents read and write it. Each is one folder with one `SKILL.md`, under 650 words of plain Markdown. Each stands alone; a few point to a sibling skill for a rule that sibling owns. None depends on any particular agent, model, language or framework.

## The idea

Agents pay for every word they read, and pay again for every word they have to figure out. Removing boilerplate makes their job cheaper. Shortening meaningful words into codes does the opposite: the file gets smaller, but the agent decodes it on every read, and sometimes decodes it wrong. So keep the meaning, cut the filler, and measure the whole task before believing any saving.

## Which skill do I need?

| If you want to... | Use |
| --- | --- |
| write log lines and error messages that an agent (or a person on call) can search and understand | [write-logs-in-plain-words](skills/write-logs-in-plain-words/SKILL.md) |
| name variables, functions, fields, status values and log keys so nobody needs a legend | [name-things-in-full-words](skills/name-things-in-full-words/SKILL.md) |
| write commit messages that say why, so nobody has to re-read the diff later | [commit-messages-that-explain-why](skills/commit-messages-that-explain-why/SKILL.md) |
| review a diff or PR (including agent-written ones) and know what is enough to approve it | [review-before-approving](skills/review-before-approving/SKILL.md) |
| decide whether a wrapper, interface, extra file or split is worth having | [cut-boilerplate-not-meaning](skills/cut-boilerplate-not-meaning/SKILL.md) |
| stop the agent from spending ten file reads just finding where things are | [keep-a-codebase-map](skills/keep-a-codebase-map/SKILL.md) |
| check whether shortening a prompt, log or context file actually saves anything | [measure-before-shrinking](skills/measure-before-shrinking/SKILL.md) |

## Install

The skills follow the open [Agent Skills](https://agentskills.io/specification) format: a folder named after the skill containing a `SKILL.md` whose frontmatter has `name` and `description`. Any agent that reads that format can load them.

**With the [`skills` CLI](https://github.com/vercel-labs/skills)** (detects your installed agents, or pass `-a claude-code`, `-a codex` and so on; `-g` installs for the user instead of the project; see its README for current flags):

```sh
npx skills add ahmedheltaher/agent-ready-codebase
```

**By hand**: copy the `skills/<name>` folders you want into your agent's skills directory. Paths as of October 2026; check your agent's documentation if a copy is not picked up.

| Agent | In a project | For the user |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex CLI | `.agents/skills/` | `~/.agents/skills/` |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |

At the time of writing, OpenCode and Cursor also read the `.claude/skills/` and `.agents/skills/` locations, so one copy can serve several agents.

**Without skill support**: paste the body of a `SKILL.md` into your project's `AGENTS.md` or `CLAUDE.md`. You lose on-demand loading, but the advice is the same.

## How sure is this advice?

- `write-logs-in-plain-words` is backed by one small experiment: a coded log format made the file smaller but made the whole debugging job cost more and take longer, and a terse structured form also cost more. One model, one dataset, one run per format, and field naming was not tested separately, so treat it as a strong hint, not a law.
- `measure-before-shrinking` is the method that experiment used; it is how you find out what is true for your setup.
- The other five (`name-things-in-full-words`, `commit-messages-that-explain-why`, `review-before-approving`, `cut-boilerplate-not-meaning`, `keep-a-codebase-map`) are reasoned advice, not measured results. They are good habits for human readers regardless; the agent benefit is something you should try and measure.

Where a skill says "measure", do it: run the same small task with and without the change, in a fresh session each time, and compare total tokens, tool calls, time and correctness.

## What is deliberately not here

Some advice says agents work better with very large files, "do everything" classes, or dropped design principles. That has not been shown, and there are reasons to doubt it: models were trained on well-structured code, long files make them miss things in the middle, and humans still have to review the result. `cut-boilerplate-not-meaning` says to split and merge at real boundaries (deployment, testing, ownership), never on line count in either direction.

Also left out: advice tied to one language or framework, custom compressed log formats with decoder scripts (the one experiment found they lose), and anything about designing new programming languages for agents.

## Background

These skills grew out of *Beyond Human-Readable: Rethinking Software Engineering Conventions for the Agentic Development Era* (Dmytro Ustynov, [arXiv:2604.07502](https://arxiv.org/abs/2604.07502), April 2026). The paper's measured part is a single experiment on log formats; its other proposals (a committed code map, richer commit messages, trimming boilerplate) are presented as ideas to test, and the skills treat them the same way. The first drafts came from several AI models independently analysing the paper and proposing which ideas were safe and useful enough to become a skill. The skills were then rewritten against a tighter brief and reviewed by the maintainer. The skills themselves do not cite the paper, so each stands alone.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the rules a skill has to follow. Run `python3 scripts/check.py` before opening a pull request; CI runs the same script.

## License

MIT. See [LICENSE](LICENSE).
