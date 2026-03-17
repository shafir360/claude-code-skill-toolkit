#!/usr/bin/env python3
"""
quick_validate.py — Deterministic Claude Code skill validator.

Validates a skill directory against the official agentskills.io spec
and Claude Code extended fields. Outputs structured JSON to stdout.

Usage: python quick_validate.py <path-to-skill-directory-or-SKILL.md>

Exit codes: 0 = all pass/warn/info, 1 = any FAIL
"""

import json
import os
import re
import sys
from pathlib import Path

# --- Constants ---

# 6 keys from the base agentskills.io spec
SPEC_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}

# Claude Code extended keys (valid but not in base spec)
EXTENDED_KEYS = {
    "argument-hint", "disable-model-invocation", "user-invocable",
    "model", "context", "agent", "hooks",
}

NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
NAME_MAX_LENGTH = 64
DESCRIPTION_MAX_LENGTH = 1024
BODY_WARN_LINES = 400  # WARN at this threshold
BODY_FAIL_LINES = 500  # FAIL at this threshold
COMPATIBILITY_MAX_LENGTH = 500

# First/second person indicators in descriptions
PERSON_PATTERNS = [
    (r"\bI\b", "first person 'I'"),
    (r"\bmy\b", "first person 'my'"),
    (r"\byou\b", "second person 'you'"),
    (r"\byour\b", "second person 'your'"),
]

# Agent spawning patterns (recursion risk detection)
# These match imperative spawn instructions, not conditional guidance about generated skills
AGENT_SPAWN_PATTERNS = [
    re.compile(r"^#{1,3}\s.*spawn.*agent", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Spawn\s+(one|a single|\d+).*agent", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Launch\s+ALL\s+agents", re.IGNORECASE | re.MULTILINE),
    re.compile(r"spawn.*deep-researcher.*agent", re.IGNORECASE),
]
SUBAGENT_TYPE_PATTERN = re.compile(r"subagent_type", re.IGNORECASE)
LEAF_NODE_PATTERN = re.compile(r"leaf.node agent|Do NOT use the Agent tool", re.IGNORECASE)
AGENT_BUDGET_PATTERN = re.compile(r"agent budget|maximum.*agents|agent.*cap", re.IGNORECASE)

# --- YAML Parsing ---

def parse_yaml_simple(yaml_text):
    """Regex-based YAML parser for simple key-value frontmatter.
    Handles strings, booleans, lists (block style), and mappings (one level).
    Falls back gracefully — does NOT handle nested structures well."""
    result = {}
    current_key = None
    current_list = None

    for line in yaml_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item under current key
        if stripped.startswith("- ") and current_key and current_list is not None:
            current_list.append(stripped[2:].strip())
            continue

        # Key-value pair
        match = re.match(r"^([a-z][a-z0-9_-]*)\s*:\s*(.*)", stripped)
        if match:
            # Save previous list if any
            if current_key and current_list is not None:
                result[current_key] = current_list

            key = match.group(1)
            value = match.group(2).strip()

            if value == "":
                # Could be start of a list or mapping
                current_key = key
                current_list = []
            elif value.lower() in ("true", "false"):
                result[key] = value.lower() == "true"
                current_key = key
                current_list = None
            else:
                # Strip quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                result[key] = value
                current_key = key
                current_list = None
        else:
            # Continuation or nested — skip
            if current_list is not None and current_key:
                continue

    # Save last list
    if current_key and current_list is not None:
        result[current_key] = current_list

    return result


def parse_frontmatter(content):
    """Extract and parse YAML frontmatter from SKILL.md content.
    Returns (parsed_dict, body_text, error_message)."""
    if not content.startswith("---"):
        return None, content, "File does not start with '---'"

    # Find the closing ---
    second_marker = content.find("\n---", 3)
    if second_marker == -1:
        return None, content, "No closing '---' found for frontmatter"

    yaml_text = content[4:second_marker].strip()
    body = content[second_marker + 4:]  # Everything after closing ---

    # Try PyYAML first
    try:
        import yaml
        parsed = yaml.safe_load(yaml_text)
        if not isinstance(parsed, dict):
            return None, body, f"Frontmatter parsed but is not a mapping (got {type(parsed).__name__})"
        return parsed, body, None
    except ImportError:
        # Fall back to regex parser
        parsed = parse_yaml_simple(yaml_text)
        return parsed, body, None
    except Exception as e:
        return None, body, f"YAML parse error: {e}"


# --- Validation Checks ---

def check(check_id, status, message):
    """Create a check result dict."""
    return {"id": check_id, "status": status, "message": message}


def validate_skill(skill_path):
    """Run all validation checks on a skill directory. Returns list of check results."""
    checks = []
    path = Path(skill_path)

    # Resolve to SKILL.md
    if path.is_dir():
        skill_md = path / "SKILL.md"
    elif path.name == "SKILL.md":
        skill_md = path
        path = path.parent
    else:
        return [check("file_exists", "FAIL", f"Not a directory or SKILL.md: {skill_path}")]

    # --- Check: file exists ---
    if not skill_md.exists():
        return [check("file_exists", "FAIL", f"SKILL.md not found at {skill_md}")]
    checks.append(check("file_exists", "PASS", f"SKILL.md found at {skill_md}"))

    # Read content
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return checks + [check("file_readable", "FAIL", f"Cannot read SKILL.md: {e}")]

    # --- Check: frontmatter exists ---
    if not content.startswith("---"):
        checks.append(check("frontmatter_exists", "FAIL", "File does not start with '---'"))
        return checks  # Can't continue without frontmatter
    checks.append(check("frontmatter_exists", "PASS", "Frontmatter delimiter found"))

    # --- Check: YAML parses ---
    parsed, body, error = parse_frontmatter(content)
    if error:
        checks.append(check("yaml_parses", "FAIL", error))
        return checks
    if parsed is None:
        checks.append(check("yaml_parses", "FAIL", "Frontmatter parsed as empty/null"))
        return checks
    checks.append(check("yaml_parses", "PASS", "YAML frontmatter parsed successfully"))

    # --- Check: name ---
    name = parsed.get("name")
    if not name:
        checks.append(check("name_exists", "FAIL", "Required field 'name' is missing"))
    elif not isinstance(name, str):
        checks.append(check("name_format", "FAIL", f"'name' must be a string, got {type(name).__name__}"))
    else:
        if not NAME_PATTERN.match(name):
            if re.search(r"[A-Z]", name):
                checks.append(check("name_format", "FAIL", f"Name '{name}' contains uppercase characters"))
            elif "--" in name:
                checks.append(check("name_format", "FAIL", f"Name '{name}' contains consecutive hyphens"))
            elif name.startswith("-") or name.endswith("-"):
                checks.append(check("name_format", "FAIL", f"Name '{name}' starts or ends with a hyphen"))
            else:
                checks.append(check("name_format", "FAIL", f"Name '{name}' contains invalid characters (only a-z, 0-9, - allowed)"))
        else:
            checks.append(check("name_format", "PASS", f"Name '{name}' is valid kebab-case"))

        if len(name) > NAME_MAX_LENGTH:
            checks.append(check("name_length", "FAIL", f"Name is {len(name)} chars (max {NAME_MAX_LENGTH})"))
        else:
            checks.append(check("name_length", "PASS", f"Name is {len(name)} chars (max {NAME_MAX_LENGTH})"))

    # --- Check: description ---
    desc = parsed.get("description")
    if not desc:
        checks.append(check("description_exists", "FAIL", "Required field 'description' is missing"))
    elif not isinstance(desc, str):
        checks.append(check("description_exists", "FAIL", f"'description' must be a string, got {type(desc).__name__}"))
    else:
        checks.append(check("description_exists", "PASS", "Description field present"))

        # Angle brackets
        if "<" in desc or ">" in desc:
            checks.append(check("description_no_angles", "FAIL", "Description contains angle brackets (< or >)"))
        else:
            checks.append(check("description_no_angles", "PASS", "No angle brackets in description"))

        # Length
        if len(desc) > DESCRIPTION_MAX_LENGTH:
            checks.append(check("description_length", "FAIL",
                f"Description is {len(desc)} chars (max {DESCRIPTION_MAX_LENGTH})"))
        elif len(desc) > 800:
            checks.append(check("description_length", "WARN",
                f"Description is {len(desc)} chars — consider trimming (max {DESCRIPTION_MAX_LENGTH})"))
        else:
            checks.append(check("description_length", "PASS",
                f"Description is {len(desc)} chars (max {DESCRIPTION_MAX_LENGTH})"))

        # Voice check (first/second person)
        person_issues = []
        for pattern, label in PERSON_PATTERNS:
            if re.search(pattern, desc, re.IGNORECASE):
                person_issues.append(label)
        if person_issues:
            checks.append(check("description_voice", "WARN",
                f"Description may use non-third-person voice: {', '.join(person_issues)}"))
        else:
            checks.append(check("description_voice", "PASS", "Description uses third-person voice"))

        # Trigger clause check
        desc_lower = desc.lower()
        has_when = any(phrase in desc_lower for phrase in ["use when", "use for", "when asked", "when the user"])
        if has_when:
            checks.append(check("description_triggers", "PASS",
                "Description includes trigger/activation clause"))
        else:
            checks.append(check("description_triggers", "INFO",
                "Description may benefit from a 'Use when...' trigger clause for better activation"))

    # --- Check: allowed keys ---
    all_allowed = SPEC_KEYS | EXTENDED_KEYS
    unknown_keys = set(parsed.keys()) - all_allowed
    spec_keys_used = set(parsed.keys()) & SPEC_KEYS
    extended_keys_used = set(parsed.keys()) & EXTENDED_KEYS

    if unknown_keys:
        checks.append(check("allowed_keys", "WARN",
            f"Unknown frontmatter keys: {', '.join(sorted(unknown_keys))}"))
    else:
        checks.append(check("allowed_keys", "PASS", "All frontmatter keys are recognized"))

    if extended_keys_used:
        checks.append(check("extended_keys", "INFO",
            f"Claude Code extended keys used: {', '.join(sorted(extended_keys_used))}"))

    # --- Check: compatibility length ---
    compat = parsed.get("compatibility")
    if compat and isinstance(compat, str) and len(compat) > COMPATIBILITY_MAX_LENGTH:
        checks.append(check("compatibility_length", "FAIL",
            f"Compatibility is {len(compat)} chars (max {COMPATIBILITY_MAX_LENGTH})"))

    # --- Check: body line count ---
    body_lines = body.strip().split("\n")
    line_count = len(body_lines) if body.strip() else 0

    if line_count > BODY_FAIL_LINES:
        checks.append(check("body_line_count", "FAIL",
            f"Body is {line_count} lines (max recommended {BODY_FAIL_LINES})"))
    elif line_count > BODY_WARN_LINES:
        checks.append(check("body_line_count", "WARN",
            f"Body is {line_count} lines (approaching {BODY_FAIL_LINES} limit)"))
    else:
        checks.append(check("body_line_count", "PASS",
            f"Body is {line_count} lines (max recommended {BODY_FAIL_LINES})"))

    # --- Check: directory structure ---
    refs_dir = path / "references"
    if refs_dir.exists():
        # Check for nested directories in references/
        nested = [p for p in refs_dir.rglob("*") if p.is_dir()]
        if nested:
            nested_names = [str(p.relative_to(refs_dir)) for p in nested]
            checks.append(check("references_depth", "WARN",
                f"Nested directories in references/: {', '.join(nested_names)} — keep references one level deep"))
        else:
            checks.append(check("references_depth", "PASS", "References are one level deep"))

    scripts_dir = path / "scripts"
    if scripts_dir.exists():
        # Check for __pycache__ or .pyc files
        pycache = list(scripts_dir.rglob("__pycache__")) + list(scripts_dir.rglob("*.pyc"))
        if pycache:
            checks.append(check("scripts_clean", "WARN",
                "scripts/ contains __pycache__ or .pyc files — clean before distribution"))

    # --- Check: path format (backslashes in SKILL.md body) ---
    if "\\" in body and not "\\n" in body and not "\\\\" in body:
        # Heuristic: look for path-like backslashes
        backslash_paths = re.findall(r"[a-zA-Z]:\\[^\s]+", body)
        if backslash_paths:
            checks.append(check("path_format", "WARN",
                f"Body contains Windows-style paths: {backslash_paths[0][:50]}... — use forward slashes"))

    # --- Check: recursion risk (agent spawning without guards) ---
    spawns_agents = any(p.search(body) for p in AGENT_SPAWN_PATTERNS)
    if spawns_agents:
        has_subagent_type = bool(SUBAGENT_TYPE_PATTERN.search(body))
        has_leaf_node = bool(LEAF_NODE_PATTERN.search(body))
        has_budget_cap = bool(AGENT_BUDGET_PATTERN.search(body))

        if not has_subagent_type:
            checks.append(check("recursion_guard_structural", "WARN",
                "Skill spawns agents but does not specify subagent_type — "
                "add subagent_type: \"deep-researcher\" to prevent recursive agent spawning"))
        else:
            checks.append(check("recursion_guard_structural", "PASS",
                "Skill spawns agents and includes subagent_type enforcement"))

        if not has_leaf_node:
            checks.append(check("recursion_guard_text", "WARN",
                "Skill spawns agents but does not include leaf-node instructions — "
                "add 'Do NOT use the Agent tool' text to agent prompts"))
        else:
            checks.append(check("recursion_guard_text", "PASS",
                "Skill spawns agents and includes leaf-node text instructions"))

        if not has_budget_cap:
            checks.append(check("recursion_guard_budget", "INFO",
                "Skill spawns agents but does not mention an agent budget cap — "
                "consider adding a maximum agent count"))
        else:
            checks.append(check("recursion_guard_budget", "PASS",
                "Skill spawns agents and includes an agent budget cap"))
    else:
        checks.append(check("recursion_risk", "PASS",
            "Skill does not appear to spawn agents — no recursion risk"))

    # --- Check: trigger phrase collision risk ---
    if name and desc and isinstance(desc, str):
        collision_phrases = [
            (r"\bgenerate\b.*\bskill\b", "generate-skill"),
            (r"\bimprove\b.*\bskill\b", "improve-skill"),
            (r"\bresearch\b.*\bgenerate\b", "research-generate-skill"),
            (r"\bresearch\b.*\bimprove\b", "research-improve-skill"),
            (r"\bdeep research\b", "deep-research"),
            (r"\bvalidate\b.*\bskill\b", "validate-skill"),
        ]
        desc_lower = desc.lower()
        collisions = []
        for pattern_str, skill_name in collision_phrases:
            # Skip if this skill's name matches or contains the target skill name
            if name != skill_name and skill_name not in name and re.search(pattern_str, desc_lower):
                collisions.append(skill_name)
        if collisions:
            checks.append(check("trigger_collision", "WARN",
                f"Description contains phrases that may trigger other skills: "
                f"{', '.join(collisions)} — consider rewording to avoid accidental activation"))
        else:
            checks.append(check("trigger_collision", "PASS",
                "No trigger phrase collision risk detected"))

    return checks


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python quick_validate.py <path-to-skill-directory-or-SKILL.md>"
        }))
        sys.exit(1)

    skill_path = sys.argv[1]
    checks = validate_skill(skill_path)

    # Build summary
    summary = {"pass": 0, "warn": 0, "fail": 0, "info": 0}
    for c in checks:
        status_lower = c["status"].lower()
        if status_lower in summary:
            summary[status_lower] += 1

    has_fail = summary["fail"] > 0
    result = {
        "valid": not has_fail,
        "path": str(Path(skill_path).resolve()),
        "checks": checks,
        "summary": summary,
    }

    # JSON to stdout
    print(json.dumps(result, indent=2))

    # Human-readable summary to stderr
    status_icon = {
        "PASS": "+",
        "WARN": "!",
        "FAIL": "X",
        "INFO": "i",
    }
    print("\n--- Validation Summary ---", file=sys.stderr)
    for c in checks:
        icon = status_icon.get(c["status"], "?")
        print(f"  [{icon}] {c['id']}: {c['message']}", file=sys.stderr)
    print(f"\n  Result: {'VALID' if not has_fail else 'INVALID'} "
          f"(PASS={summary['pass']}, WARN={summary['warn']}, "
          f"FAIL={summary['fail']}, INFO={summary['info']})", file=sys.stderr)

    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
