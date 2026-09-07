"""
CI check: every .claude/ Rule/Skill/Agent file has valid, parseable YAML
frontmatter with the fields Claude Code actually requires, and
evals/protocol.yaml parses as valid YAML. Exits nonzero on any failure.
"""
import sys
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []


def check_frontmatter(path: pathlib.Path, required_keys: set):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path}: does not start with '---' frontmatter delimiter")
        return
    try:
        end = text.index("\n---", 4)
    except ValueError:
        errors.append(f"{path}: no closing '---' frontmatter delimiter found")
        return
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as e:
        errors.append(f"{path}: frontmatter is not valid YAML: {e}")
        return
    missing = required_keys - set(fm.keys())
    if missing:
        errors.append(f"{path}: frontmatter missing required key(s): {sorted(missing)}")


for skill_dir in (ROOT / ".claude" / "skills").iterdir():
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        check_frontmatter(skill_file, {"name", "description"})

for agent_file in (ROOT / ".claude" / "agents").glob("*.md"):
    check_frontmatter(agent_file, {"name", "description"})

for rule_file in (ROOT / ".claude" / "rules").glob("*.md"):
    check_frontmatter(rule_file, set())  # rules only require valid YAML, no mandatory keys

try:
    yaml.safe_load((ROOT / "evals" / "protocol.yaml").read_text(encoding="utf-8"))
except yaml.YAMLError as e:
    errors.append(f"evals/protocol.yaml: not valid YAML: {e}")

if errors:
    print("Frontmatter/YAML check FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("Frontmatter/YAML check OK.")
