#!/usr/bin/env python3
"""Check every skills/*/SKILL.md against the rules in CONTRIBUTING.md. Stdlib only.

Checks: frontmatter has only `name` and `description` (an indented continuation line is
joined to the previous value), `name` equals the folder, the description is non-empty and
at most 60 words, the body is 350-650 words with a `# ` title and a `## When not to apply`
section and no "When to use" / "How sure" heading at any level (fenced code is ignored),
every backticked kebab-case name of three or more parts is a skill folder, and README.md
links every skill's SKILL.md. Word counter: whitespace-separated tokens containing a letter
or digit; bare symbols such as `→`, `—` or `|` are not words.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
ALLOWED_KEYS = {"name", "description"}
BANNED_HEADINGS = re.compile(r"^#{2,}\s+(when to use|how sure)", re.IGNORECASE | re.MULTILINE)
REQUIRED_SECTION = re.compile(r"^## When not to apply\s*$", re.MULTILINE)
TITLE_LINE = re.compile(r"^# \S", re.MULTILINE)
FENCED_BLOCK = re.compile(r"^```.*?^```[ \t]*$", re.DOTALL | re.MULTILINE)
BACKTICKED_SKILL_NAME = re.compile(r"`([a-z]+(?:-[a-z]+){2,})`")
BLOCK_SCALAR = {">", "|", ">-", "|-"}


def parse_frontmatter(text):
    """Return (fields, body). Accepts `key: value` lines between two `---` fences; an
    indented line continues the previous key's value, joined with a space."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with a '---' frontmatter fence")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("frontmatter has no closing '---' fence")
    fields, last_key = {}, None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line[0] in " \t" and last_key:
            fields[last_key] = (fields[last_key] + " " + line.strip()).strip()
            continue
        key, sep, value = line.partition(":")
        if not sep or not re.fullmatch(r"[a-z-]+", key.strip()):
            raise ValueError(f"unparseable frontmatter line: {line!r}")
        last_key = key.strip()
        value = value.strip()
        fields[last_key] = "" if value in BLOCK_SCALAR else value.strip("'\"")
    return fields, "\n".join(lines[end + 1:])


def word_count(text):
    """Whitespace-separated tokens containing a letter or digit; bare symbols are not words."""
    return sum(1 for token in text.split() if re.search(r"[^\W_]", token))


def check_skill(path, folders, readme_text):
    errors = []
    try:
        fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [str(exc)], None, None
    extra = set(fields) - ALLOWED_KEYS
    if extra:
        errors.append(f"frontmatter has unexpected keys: {sorted(extra)}")
    for key in ALLOWED_KEYS - set(fields):
        errors.append(f"frontmatter is missing '{key}'")
    if fields.get("name") and fields["name"] != path.parent.name:
        errors.append(f"name '{fields['name']}' does not equal folder name '{path.parent.name}'")
    desc_words = word_count(fields.get("description", ""))
    if "description" in fields and desc_words == 0:
        errors.append("description is empty")
    if desc_words > 60:
        errors.append(f"description is {desc_words} words (max 60)")
    body_words = word_count(body)
    if not 350 <= body_words <= 650:
        errors.append(f"body is {body_words} words (must be 350-650)")
    prose = FENCED_BLOCK.sub("", body)
    if not TITLE_LINE.search(prose):
        errors.append("body has no '# ' title line")
    if not REQUIRED_SECTION.search(prose):
        errors.append("body has no '## When not to apply' section")
    for match in BANNED_HEADINGS.finditer(prose):
        errors.append(f"body has a banned heading: {match.group(0).strip()!r}")
    for name in sorted(set(BACKTICKED_SKILL_NAME.findall(prose))):
        if name not in folders:
            errors.append(f"references `{name}`, which is not a skill folder")
    if f"skills/{path.parent.name}/SKILL.md" not in readme_text:
        errors.append(f"README.md has no link to skills/{path.parent.name}/SKILL.md")
    return errors, desc_words, body_words


def main():
    paths = sorted(SKILLS.glob("*/SKILL.md"))
    if not paths:
        print(f"FAIL: no skills found under {SKILLS}")
        return 1
    readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
    folders = {p.parent.name for p in paths}
    failed = False
    for path in paths:
        errors, desc_words, body_words = check_skill(path, folders, readme_text)
        status = "ok" if not errors else "FAIL"
        print(f"{path.parent.name}: description {desc_words} words, body {body_words} words, {status}")
        for message in errors:
            print(f"  error: {message}")
        failed = failed or bool(errors)
    print("FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
