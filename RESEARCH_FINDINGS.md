## Research Findings: How Top Claude Code Skill Creators Build Their Skills
_Initial research: 2026-03-14 | Enriched: 2026-03-15 | Sources consulted: 34_

---

## Table of Contents
1. [Official SKILL.md Specification](#1-official-skillmd-specification)
2. [Anthropic's Skill-Creator Meta-Skill](#2-anthropics-skill-creator-meta-skill)
3. [Top Community Skill Creators Analysis](#3-top-community-skill-creators-analysis)
4. [Common Structural Patterns](#4-common-structural-patterns-across-all-top-skills)
5. [Description Writing Techniques](#5-description-writing-techniques-that-trigger-reliably)
6. [$ARGUMENTS and Dynamic Context Injection](#6-arguments-and-dynamic-context-injection)
7. [Multi-Step Instruction Patterns](#7-multi-step-instruction-patterns)
8. [Edge Case Handling](#8-edge-case-handling-in-skill-prompts)
9. [Supporting File Organization](#9-supporting-file-organization)
10. [Skill Factory Analysis](#10-alirezarezvaniclaude-code-skill-factory-analysis)
11. [What We Can Do Better](#11-what-we-can-do-better)
12. [Anti-Patterns to Avoid](#12-anti-patterns-to-avoid)
13. [Master Checklist](#13-master-checklist-for-high-quality-skills)
14. [Skill-Creator 2.0 Evaluation Pipeline](#14-skill-creator-20-evaluation-pipeline)
15. [Automated Prompt/Skill Evaluation Methods](#15-automated-promptskill-evaluation-methods)
16. [Multi-Agent Prompt Generation Architectures](#16-multi-agent-prompt-generation-architectures)
17. [Skill Description Optimization Deep Dive](#17-skill-description-optimization-deep-dive)
18. [Key Insights for Our Skill Generator](#18-key-insights-for-our-skill-generator)

---

## 1. Official SKILL.md Specification

### Required File Structure
```
my-skill/
├── SKILL.md              # Required entry point
├── references/           # Optional - docs loaded into context as needed
│   └── guide.md
├── scripts/              # Optional - executable code for deterministic tasks
│   └── validate.py
└── assets/               # Optional - templates, icons, fonts for output
    └── template.html
```

### SKILL.md Format
```yaml
---
name: my-skill-name          # REQUIRED: kebab-case, [a-z0-9-]+, max 64 chars
description: What it does     # REQUIRED: max 1024 chars, no < or >
license: Apache-2.0           # Optional: SPDX identifier
allowed-tools:                # Optional: restrict tool access
  - Read
  - Grep
  - Bash(python *)
metadata:                     # Optional: extensibility mechanism
  category: creative
  complexity: advanced
compatibility: Claude Code 1.0+  # Optional: max 500 chars
---

# Markdown instructions here
```

### Claude Code Extended Frontmatter Fields
Claude Code adds several fields beyond the base spec:

| Field | Purpose |
|-------|---------|
| `argument-hint` | Hint shown during autocomplete. Example: `[issue-number]` |
| `disable-model-invocation` | `true` = only user can invoke (prevents auto-trigger) |
| `user-invocable` | `false` = hidden from / menu (background knowledge only) |
| `allowed-tools` | Tools Claude can use without permission when skill active |
| `model` | Override model selection for this skill |
| `context` | `fork` = run in isolated subagent context |
| `agent` | Which subagent type (`Explore`, `Plan`, `general-purpose`, or custom) |
| `hooks` | Hooks scoped to this skill's lifecycle |

### Validation Rules (from quick_validate.py)
1. File must start with `---`
2. YAML must parse via `yaml.safe_load()`
3. Only allowed top-level keys: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`
4. Name: lowercase + digits + hyphens only, no consecutive hyphens, no start/end hyphens
5. Description: non-empty, no angle brackets, max 1024 chars

### How Skills Work Internally (Architecture)
Skills are **prompt-based context modifiers**, NOT executable code:

1. **Startup**: Only `name` + `description` from ALL skills loaded into system prompt as `<available_skills>` (budget: 2% of context window, fallback 16,000 chars)
2. **Selection**: Claude's native reasoning matches user intent against descriptions (no regex/keyword matching)
3. **Loading**: Claude invokes the `Skill` meta-tool with `{"command": "skill-name"}`
4. **Injection**: Two messages injected - one visible ("skill is loading"), one hidden (full SKILL.md body)
5. **Context Modification**: Skill pre-approves specified tools, optionally overrides model
6. **Progressive Disclosure**: Referenced files loaded only when Claude needs them via Read tool

**Source**: [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) (Credibility: HIGH)

---

## 2. Anthropic's Skill-Creator Meta-Skill

### Directory Structure
```
skills/skill-creator/
├── SKILL.md                    # Main instructions
├── LICENSE.txt
├── agents/
│   ├── analyzer.md             # Analyzes skill quality
│   ├── comparator.md           # Compares skill versions
│   └── grader.md               # Grades skill effectiveness
├── assets/                     # Templates and supporting files
├── eval-viewer/                # Tool for viewing evaluation results
├── references/
│   └── schemas.md              # Schema definitions for skills
└── scripts/
    ├── __init__.py
    ├── aggregate_benchmark.py  # Aggregates benchmark results
    ├── generate_report.py      # Generates evaluation reports
    ├── improve_description.py  # Improves skill descriptions
    ├── package_skill.py        # Packages skills for distribution
    ├── quick_validate.py       # Validates SKILL.md format
    ├── run_eval.py             # Runs skill evaluations
    ├── run_loop.py             # Runs evaluation loops
    └── utils.py                # Shared utilities
```

### Key Design Principles
The skill-creator follows a **5-stage iterative development cycle**:

1. **Define** - Figure out skill purpose and approach
2. **Draft** - Write the initial SKILL.md version
3. **Evaluate** - Create test scenarios and run evaluations
4. **Review** - Analyze outputs qualitatively and quantitatively
5. **Refine** - Iterate based on feedback

It uses **sub-agents** for specialized tasks:
- `analyzer.md` agent for deep skill analysis
- `comparator.md` for A/B comparison of skill versions
- `grader.md` for scoring skill effectiveness

It includes **automation scripts** for:
- Validation (`quick_validate.py`)
- Benchmarking (`aggregate_benchmark.py` produces `benchmark.json` and `benchmark.md` with pass_rate, time, tokens)
- Description optimization (`improve_description.py`)
- Packaging (`package_skill.py`)

**Key Insight**: Anthropic treats skill development as a data-driven process with automated evaluation, not just prompt engineering.

**Source**: [anthropics/skills GitHub](https://github.com/anthropics/skills) (Credibility: HIGH)

---

## 3. Top Community Skill Creators Analysis

### A. alirezarezvani/claude-skills (180+ skills)

**Organization**: Skills grouped by domain in top-level directories:
```
claude-skills/
├── engineering-team/        # 24 core + 25 POWERFUL-tier
│   ├── senior-frontend/
│   ├── aws-solution-architect/
│   └── ...
├── marketing-skill/         # 43 skills in 7 pods
├── product-skill/           # 12 skills
├── c-level-advisory/        # 28 skills across 10 roles
├── compliance-skill/        # 12 RA/QM skills
└── ...
```

**Patterns Used**:
- Role-based skill naming (e.g., `senior-frontend`, `aws-solution-architect`)
- Each skill has SKILL.md + optional scripts/, references/, assets/
- Heavy use of decision frameworks and workflows within SKILL.md
- 254 Python automation tools (all standard library, no deps)
- 357 reference guides for domain knowledge
- POWERFUL-tier skills use more advanced patterns with deeper context

**Source**: [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (Credibility: MEDIUM)

### B. levnikolaevich/claude-code-skills (Full Delivery Workflow)

**Organization**: Skills form a **complete Agile pipeline** with numbered prefixes:
```
claude-code-skills/
├── ln-100-*    # Documentation generation
├── ln-200-*    # Scope decomposition (Epics/Stories)
├── ln-400-*    # Task execution
│   ├── ln-401-task-executor
│   ├── ln-402-task-reviewer
│   └── ln-403-task-rework
├── ln-500-*    # Quality gates
│   └── ln-500-story-quality-gate  # 4-level: PASS/CONCERNS/REWORK/FAIL
└── ln-700-*    # Project bootstrap
```

**Key Patterns**:
- **Numbered prefix system** for ordering (100, 200, 400, 500, 700)
- **Pipeline architecture**: Each skill feeds into the next
- **Review loops**: task-executor -> task-reviewer -> task-rework -> back to reviewer
- **Quality gates** with explicit pass/fail criteria
- **Graceful degradation**: Works without Linear; falls back to `kanban_board.md`
- **5 independent plugins**: agile-workflow, documentation-pipeline, codebase-audit-suite, project-bootstrap, optimization-suite
- **Human approval checkpoints** between stages

**Source**: [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) (Credibility: MEDIUM)

### C. posit-dev/skills (Data Science Skills)

**Organization**: Skills by technology/platform:
```
posit-dev/skills/
├── posit-dev/           # General dev tools (code review, design docs)
├── github/              # PR workflow automation
├── open-source/         # Release/changelog management
├── r-lib/               # R package development
├── shiny/               # Dashboard/app development
│   └── shiny-bslib-theming/
├── quarto/              # Document creation/publishing
│   ├── quarto-authoring/
│   └── quarto-alt-text/
└── brand-yml/           # Cross-platform brand consistency
    ├── SKILL.md
    └── references/
        ├── brand-yml-spec.md
        ├── shiny-r.md
        ├── shiny-python.md
        ├── quarto.md
        └── brand-yml-in-r.md
```

**Key Patterns**:
- **Decision trees** within SKILL.md (e.g., brand-yml has 7 workflow branches)
- **Heavy use of references/** for platform-specific docs
- **Incremental build guidance** ("Build incrementally from minimal to complete structure")
- **Integration-specific reference files** (separate docs for Shiny R, Shiny Python, Quarto)
- **Troubleshooting sections** addressing common issues
- **Common patterns sections** with concrete examples

**Source**: [posit-dev/skills](https://github.com/posit-dev/skills) (Credibility: HIGH - official Posit team)

---

## 4. Common Structural Patterns Across All Top Skills

### Pattern 1: Progressive Disclosure (Used by ALL top creators)
```
SKILL.md           -> Core instructions (~500 lines max)
  └── references/  -> Detailed docs (loaded on demand)
  └── scripts/     -> Automation (executed, not loaded into context)
  └── assets/      -> Templates (referenced by path)
```
**Rule**: Keep references ONE level deep from SKILL.md. Never nest references within references.

### Pattern 2: Template Pattern
````markdown
## Output Format

ALWAYS use this exact structure:

```markdown
# [Title]

## Summary
[One paragraph overview]

## Details
[Findings with data]

## Recommendations
1. [Specific action]
```
````

### Pattern 3: Examples Pattern (Input/Output Pairs)
````markdown
**Example 1:**
Input: Added user authentication with JWT
Output:
```
feat(auth): implement JWT-based authentication
```

**Example 2:**
Input: Fixed date display bug
Output:
```
fix(reports): correct date formatting
```
````

### Pattern 4: Conditional Workflow / Decision Tree
```markdown
## Determine approach:

**Creating new?** -> Follow "Creation workflow" below
**Editing existing?** -> Follow "Editing workflow" below
**Troubleshooting?** -> See [troubleshooting.md](references/troubleshooting.md)
```

### Pattern 5: Checklist-Driven Workflow
````markdown
Copy this checklist and track progress:

```
- [ ] Step 1: Analyze input
- [ ] Step 2: Generate plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```
````

### Pattern 6: Feedback Loop / Validation Loop
```markdown
1. Make changes
2. Run validation: `python scripts/validate.py`
3. If validation fails:
   - Review errors
   - Fix issues
   - Run validation again
4. Only proceed when validation passes
```

### Pattern 7: Domain-Specific Organization (BigQuery example)
```
skill/
├── SKILL.md (overview + navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```
SKILL.md points to the right reference file based on user query domain.

### Pattern 8: Role-Based Persona (alirezarezvani pattern)
```markdown
# Senior Frontend Engineer

You are acting as a senior frontend engineer with expertise in...

## Decision Framework
When evaluating approaches, consider:
1. Performance implications
2. Accessibility
3. Maintainability
```

### Pattern 9: Pipeline/Chain Skills (levnikolaevich pattern)
Skills that explicitly hand off to each other:
```
bootstrap -> document -> decompose -> execute -> review -> quality-gate
```
Each skill knows its predecessor and successor in the pipeline.

---

## 5. Description Writing Techniques That Trigger Reliably

### Official Guidance (Anthropic)
The description is the **single most critical field** for skill activation. Claude uses it to choose from 100+ available skills.

### Rules for Effective Descriptions

1. **Always write in third person**
   - GOOD: "Processes Excel files and generates reports"
   - BAD: "I can help you process Excel files"
   - BAD: "You can use this to process Excel files"

2. **Include BOTH what it does AND when to use it**
   ```yaml
   description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
   ```

3. **Include specific trigger keywords**
   ```yaml
   description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
   ```

4. **Consider gerund form for names**
   - `processing-pdfs` (clearly describes activity)
   - `analyzing-spreadsheets`
   - `managing-databases`

5. **Avoid vague descriptions**
   - BAD: "Helps with documents"
   - BAD: "Processes data"
   - BAD: "Does stuff with files"

### Activation Rate Data
From the official best practices:
- Base description: ~20% activation rate
- Properly optimized description: ~50% activation rate
- Description + examples in SKILL.md: 72% -> 90% activation rate

### Token Budget for Descriptions
All skill descriptions must fit within 2% of context window (fallback: 16,000 chars). If you have many skills, keep descriptions concise.

**Sources**:
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (Credibility: HIGH)
- [Claude Code Skills docs](https://code.claude.com/docs/en/skills) (Credibility: HIGH)

---

## 6. $ARGUMENTS and Dynamic Context Injection

### $ARGUMENTS Usage

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`, `$2`) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's SKILL.md |

**Example - Simple argument**:
```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
```
Usage: `/fix-issue 123` -> "Fix GitHub issue 123 following our coding standards."

**Example - Multiple arguments**:
```yaml
---
name: migrate-component
description: Migrate a component between frameworks
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```
Usage: `/migrate-component SearchBar React Vue`

**Fallback**: If `$ARGUMENTS` not present in skill content, arguments are appended as `ARGUMENTS: <value>`.

### Dynamic Context Injection (Shell Commands)

The `` !`command` `` syntax runs shell commands BEFORE skill content reaches Claude:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

**Key points**:
- Commands execute immediately (preprocessing, not Claude execution)
- Output replaces the placeholder
- Claude only sees the final rendered prompt with actual data
- Use `` !`echo $VAR` `` to read environment variables (standard `$VAR` not expanded)

**Source**: [Claude Code Skills docs](https://code.claude.com/docs/en/skills) (Credibility: HIGH)

---

## 7. Multi-Step Instruction Patterns

### Imperative Language (CRITICAL)
```markdown
GOOD: "Always run tests before committing"
BAD: "You might want to consider running tests"
```
Agents follow directives more reliably than suggestions.

### Degrees of Freedom Model

**High freedom** (multiple approaches valid):
```markdown
## Code review process
1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability
4. Verify adherence to project conventions
```

**Medium freedom** (preferred pattern exists):
````markdown
## Generate report
Use this template and customize as needed:
```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
```
````

**Low freedom** (fragile/critical operations):
````markdown
## Database migration
Run exactly this script:
```bash
python scripts/migrate.py --verify --backup
```
Do not modify the command or add additional flags.
````

### Plan-Validate-Execute Pattern
For complex tasks, create verifiable intermediate outputs:
```
analyze -> create plan file (JSON) -> validate plan with script -> execute -> verify
```
This catches errors before destructive changes.

### Workflow Branching
```markdown
## Document modification workflow

1. Determine the modification type:
   **Creating new content?** -> Follow "Creation workflow" below
   **Editing existing content?** -> Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build from scratch
   - Export to .docx

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

**Source**: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (Credibility: HIGH)

---

## 8. Edge Case Handling in Skill Prompts

### Concrete Examples Beat Abstract Rules
```markdown
GOOD: Show input/output pairs for edge cases
BAD: "Handle edge cases appropriately"
```

### Explicit Error Handling in Scripts
```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ""
```

### Verbose Validation Error Messages
```
"Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed"
```
Specific messages help Claude self-correct.

### No "Voodoo Constants"
```python
# GOOD: Self-documenting
REQUEST_TIMEOUT = 30  # HTTP requests typically complete within 30 seconds
MAX_RETRIES = 3       # Most intermittent failures resolve by second retry

# BAD: Magic numbers
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### Graceful Degradation (levnikolaevich pattern)
```markdown
## Task Management
If Linear integration is available:
  - Use Linear API for task management
If Linear is NOT available:
  - Use local kanban_board.md as fallback
```

---

## 9. Supporting File Organization

### File Type Purposes

| Directory | Purpose | How Claude Uses It |
|-----------|---------|-------------------|
| `references/` | Docs, API specs, guides | **Read into context** via Read tool |
| `scripts/` | Python/Bash automation | **Executed** via Bash tool (output only enters context) |
| `assets/` | Templates, images, fonts | **Referenced by path** (not loaded into context) |

### Naming Conventions
- GOOD: `form_validation_rules.md`, `reference/finance.md`
- BAD: `doc2.md`, `docs/file1.md`

### Reference File Best Practices
1. Keep references ONE level deep from SKILL.md
2. For files >100 lines, include a table of contents at top
3. Use descriptive file names
4. Organize by domain or feature
5. All paths use forward slashes (even on Windows)

### SKILL.md Referencing Pattern
````markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
- For troubleshooting, see [troubleshooting.md](references/troubleshooting.md)
````

### How Progressive Disclosure Works
```
Context cost:
  - SKILL.md metadata (name+description): Always loaded
  - SKILL.md body: Loaded when skill triggered
  - references/*.md: Loaded ONLY when Claude reads them
  - scripts/*.py: NEVER loaded (only output enters context)
  - assets/*: NEVER loaded (referenced by path)
```

---

## 10. alirezarezvani/claude-code-skill-factory Analysis

### Architecture
```
claude-code-skill-factory/
├── .claude/
│   ├── agents/              # 5 interactive guides
│   │   ├── factory-guide.md     # Main orchestrator
│   │   ├── skills-guide.md      # Skill building specialist
│   │   ├── prompts-guide.md     # Prompt engineering specialist
│   │   ├── agents-guide.md      # Agent building specialist
│   │   └── hooks-guide.md       # Hook building specialist
│   └── commands/            # 8+ slash commands
│       ├── build.md             # /build - main entry
│       ├── build-hook.md        # /build-hook
│       ├── validate-output.md   # /validate-output
│       ├── install-skill.md     # /install-skill
│       └── ...
├── documentation/
│   ├── references/          # Anthropic & OpenAI docs
│   └── templates/           # 4 factory prompt templates
│       ├── SKILLS_FACTORY_PROMPT.md
│       ├── AGENTS_FACTORY_PROMPT.md
│       ├── HOOKS_FACTORY_PROMPT.md
│       └── MASTER_SLASH_COMMANDS_PROMPT.md
└── generated-skills/       # 9 production-ready examples
    ├── aws-solution-architect/  (53 KB)
    ├── content-trend-researcher/ (35 KB)
    ├── prompt-factory/          (427 KB!)
    └── ...
```

### How It Works
Three interaction paths:
1. **Guided**: Say "I want to build something" -> `factory-guide` agent orchestrates specialists
2. **Direct**: Use `/build skill`, `/build agent`, `/build prompt`, `/build hook`
3. **Copy**: Use pre-built skills from `generated-skills/`

### What It Does Well
- Multi-format output (Skills, Agents, Commands, Hooks, Prompts)
- Interactive Q&A flow (5-7 questions to gather requirements)
- Validation built into the pipeline
- Template-based generation using factory prompt templates
- Cross-platform support (Claude, OpenAI Codex)

### What We Can Improve
- Generated skills are VERY large (53KB-427KB) - violates Anthropic's "concise is key" principle
- No automated evaluation/benchmarking (unlike Anthropic's skill-creator)
- No progressive disclosure optimization
- No description optimization tooling
- Does not generate test scenarios / evaluations
- Heavy reliance on templates rather than adaptive generation
- v1.4.0 (Oct 2025) - not updated for latest skill spec features

**Source**: [alirezarezvani/claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) (Credibility: MEDIUM)

---

## 11. What We Can Do Better

Based on analysis of ALL sources, here's what a superior skill generator should do:

### 1. Enforce Anthropic's Official Best Practices
- SKILL.md body under 500 lines
- Description: third person, includes what AND when, specific trigger keywords
- Name: gerund form preferred, kebab-case
- Progressive disclosure: auto-split large content into references/

### 2. Include Evaluation from Day One (Anthropic's approach)
```json
{
  "skills": ["my-skill"],
  "query": "Representative user request",
  "files": ["test-files/input.pdf"],
  "expected_behavior": [
    "Specific observable behavior 1",
    "Specific observable behavior 2"
  ]
}
```

### 3. Optimize Descriptions Automatically
- Generate multiple description variants
- Test activation rates
- Include both "what" and "when" components
- Use Anthropic's `improve_description.py` pattern

### 4. Generate Supporting File Structure Intelligently
- Auto-detect when SKILL.md is too long and needs references/
- Auto-generate scripts/ for deterministic operations
- Generate reference files with table of contents for long docs

### 5. Use the Degrees-of-Freedom Model
- Analyze task fragility to determine instruction specificity
- High freedom for creative tasks
- Low freedom for critical/destructive operations

### 6. Generate Validation/Feedback Loops
- For every skill with side effects, generate a validation step
- Plan-validate-execute pattern for complex workflows

### 7. Include Concrete Examples
- Generate input/output pairs for the skill's domain
- Show edge cases with expected behavior

### 8. Test Across Models
- Generate with model-appropriate verbosity
- Haiku needs more detail; Opus needs less

---

## 12. Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad |
|-------------|--------------|
| Windows-style paths (`scripts\helper.py`) | Fails on Unix systems |
| Offering too many options | Confusing; provide a default with escape hatch |
| Time-sensitive information | Will become wrong; use "old patterns" section |
| Inconsistent terminology | Confuses Claude; pick one term and stick to it |
| Deeply nested references | Claude may only `head -100` nested files |
| Over-explaining basics | Claude already knows what PDFs are |
| Vague descriptions | "Helps with documents" won't activate reliably |
| First/second person in descriptions | Causes discovery problems |
| Magic numbers in scripts | Claude can't determine right values either |
| Punting errors to Claude | Handle errors explicitly in scripts |
| Loading everything into SKILL.md | Wastes context window; use references/ |

---

## 13. Master Checklist for High-Quality Skills

### Core Quality
- [ ] Name: kebab-case, gerund form preferred, max 64 chars
- [ ] Description: third person, what + when, specific keywords, max 1024 chars
- [ ] SKILL.md body: under 500 lines
- [ ] Large content split into references/ files
- [ ] References one level deep (no nesting)
- [ ] Long reference files have table of contents
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Imperative language ("Always do X" not "You might want to X")
- [ ] Concrete input/output examples
- [ ] Forward slashes in all paths
- [ ] Progressive disclosure used appropriately

### Instructions
- [ ] Appropriate degrees of freedom for task fragility
- [ ] Decision trees for branching workflows
- [ ] Checklists for multi-step workflows
- [ ] Feedback loops for quality-critical tasks
- [ ] Plan-validate-execute for complex operations
- [ ] Edge cases with explicit handling
- [ ] Error recovery guidance

### Code and Scripts
- [ ] Scripts handle errors explicitly (don't punt to Claude)
- [ ] All constants documented with rationale
- [ ] Standard library only when possible
- [ ] Required packages listed in instructions
- [ ] Scripts use descriptive names
- [ ] Clear distinction: execute vs. read as reference

### Evaluation
- [ ] At least 3 test scenarios created
- [ ] Tested with target models (Haiku, Sonnet, Opus)
- [ ] Tested with real usage scenarios
- [ ] Description activation rate verified

---

## 14. Skill-Creator 2.0 Evaluation Pipeline

_Added: 2026-03-15 | Sources: Anthropic Blog, DeepWiki, Tessl.io, GitHub_

### Four-Agent Evaluation Harness

Anthropic's skill-creator 2.0 uses a **four-agent evaluation system** that benchmarks skills rigorously:

| Agent | Role | Output |
|-------|------|--------|
| **Executor** | Runs the skill against test queries (with_skill and without_skill paths) | Raw outputs in `eval-N/` directories |
| **Grader** | Scores each output against predefined assertions | `grading.json` with `text`, `passed`, `evidence` fields |
| **Comparator** | Blind A/B rubric scoring (1-5 scale) without knowing which version is which | Eliminates evaluator bias |
| **Analyzer** | Explains why one version outperformed the other | `improvement_suggestions` for next iteration |

**Source**: [DeepWiki: Skill Creator](https://deepwiki.com/anthropics/skills/4-skill-creator) (MEDIUM), [Anthropic Blog](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) (HIGH)

### Workspace Structure
```
iteration-N/
├── eval-0/
│   ├── with_skill/      # Output when skill is active
│   └── without_skill/   # Baseline output
├── eval-1/
│   ├── with_skill/
│   └── without_skill/
├── grading.json
└── benchmark.json
```

The skill-creator operates in **four modes**: Create, Eval, Improve, Benchmark. Each iteration is isolated in its own directory to prevent cross-contamination.

### Quantitative Benchmark Metrics

`aggregate_benchmark.py` consolidates per-run metrics into `benchmark.md` and `benchmark.json`:

| Metric | What It Measures |
|--------|-----------------|
| **Pass rate** | % of test queries where skill output met assertions |
| **Mean tokens** | Average token consumption per query |
| **Mean time** | Average execution time per query |
| **Delta** | Change in each metric across iterations |

### Real-World Validation

Anthropic's internal testing on **six document-related skills** showed:
- **5 of 6 skills** improved trigger rates after optimization
- **17% token reduction** (~93,000 → ~77,000 tokens) with no measured quality loss
- Validates that the benchmark metrics actually correlate with real-world improvement

**Source**: [Tessl.io](https://tessl.io/blog/anthropic-brings-evals-to-skill-creator-heres-why-thats-a-big-deal/) (MEDIUM)

### Eval Viewer & Human Feedback Loop

The pipeline includes a **browser-based eval viewer** that:
- Displays side-by-side comparisons of with_skill vs without_skill outputs
- Collects human feedback for the next improvement iteration
- Closes the loop: automated eval → human review → next iteration

**Source**: [Anthropic Blog](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) (HIGH)

---

## 15. Automated Prompt/Skill Evaluation Methods

_Added: 2026-03-15 | Sources: arxiv, EvidentlyAI, Braintrust, Maxim.ai_

### Evaluation Tool Landscape

| Tool | Approach | Unique Strength |
|------|----------|----------------|
| **promptfoo** | Open-source, CI/CD-native | Red-teaming layer for injection & PII vulnerability scanning |
| **LangSmith** | LangChain-ecosystem observability | Tracing and debugging chains end-to-end |
| **Braintrust** | End-to-end scoring | Natural-language rubrics (describe criteria in plain English) |
| **DSPy** | Black-box prompt optimization | LLM iteratively proposes/evaluates/selects instruction candidates |

**Source**: [Braintrust](https://www.braintrust.dev/articles/best-prompt-evaluation-tools-2025) (MEDIUM)

### LLM-as-Judge Best Practices

Using an LLM to evaluate another LLM's output is now standard practice, but requires specific anti-bias measures:

**Required techniques**:
1. **Chain-of-thought before scoring** — force the judge to reason before assigning a score
2. **Low temperature** (0.1-0.2) — reduce scoring variance
3. **Few-shot calibration examples** — anchor the judge's scale with known-quality examples
4. **Anti-bias instructions** — explicitly instruct to ignore length, style, position

**Without these measures**, correlation with human judgments drops to 0.03-0.2 for smaller models.

**Source**: [EvidentlyAI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) (MEDIUM)

### Known Biases in LLM Judges

| Bias | Impact | Mitigation |
|------|--------|-----------|
| **Position bias** | Swapping candidate order shifts accuracy by >10% | Randomize presentation order |
| **Verbosity bias** | LLMs systematically favor longer responses | Normalize for length in rubric |
| **Self-preference** | LLMs favor outputs stylistically similar to their own training | Use ensemble judging with different models |

**Sources**: [arxiv 2406.07791](https://arxiv.org/abs/2406.07791) (HIGH), [arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) (HIGH)

### Core Quality Metrics for Prompts/Skills

| Metric | Measures | Best For |
|--------|----------|----------|
| **Accuracy** | Output vs. reference ground truth | Tasks with clear correct answers |
| **Consistency** | Variance across repeated runs | Reliability assessment |
| **Token efficiency** | Cost per request | Budget optimization |
| **Latency** | Time to complete | User experience |
| **BLEU/ROUGE/BERTScore** | Text similarity to reference | Text generation tasks |
| **Rubric-based LLM scoring** | Open-ended quality assessment | Creative/complex tasks |

**Source**: [Maxim.ai](https://www.getmaxim.ai/articles/prompt-evaluation-frameworks-measuring-quality-consistency-and-cost-at-scale/) (MEDIUM)

---

## 16. Multi-Agent Prompt Generation Architectures

_Added: 2026-03-15 | Sources: arxiv, Anthropic, DSPy, Optimas_

### The Generator/Critic/Refiner Pattern

The **dominant production pattern** for prompt/skill generation uses three agents in a loop:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Generator   │────→│   Critic     │────→│   Refiner    │
│  (drafts)    │     │  (scores)    │     │  (polishes)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
       ↑                                        │
       └────────────────────────────────────────┘
                    (loop until pass)
```

- **Generator**: Creates initial draft based on requirements
- **Critic**: Applies hard-coded or LLM-scored criteria against rubric
- **Refiner**: Polishes based on critic feedback
- **Break condition**: Loop terminates when critic gives a pass score

One e-commerce firm reported **40% reduction in support-ticket resolution time** using this pattern.

**Source**: [arxiv 2502.02533](https://arxiv.org/abs/2502.02533) (HIGH)

### Black-Box Prompt Optimization (DSPy / OPRO)

Stanford's **DSPy** and Google DeepMind's **OPRO** treat prompt generation as optimization:
1. LLM proposes multiple instruction candidates
2. Each candidate is evaluated against a test set
3. Best-performing candidates are selected
4. Process repeats with the best candidates as seed

**Optimas** extends this across multi-agent stacks (CrewAI, AutoGen, OpenAI SDK) in a single CLI workflow.

**Sources**: [DSPy](https://dspy.ai/learn/optimization/optimizers/) (HIGH), [Optimas](https://medium.com/@shashikant.jagtap/optimas-superoptix-global-reward-optimization-for-dspy-crewai-autogen-and-openai-agents-sdk-29257eff039d) (MEDIUM)

### Context Engineering > Prompt Engineering

Anthropic internally frames this discipline as **"context engineering"** rather than prompt engineering:
- Focus on **what goes into the context window**, not just phrasing
- Use Console tools: prompt generator, prompt improver, Evaluate Tab
- **Ralph Loop plugin**: autonomous self-referential loops where Claude iteratively refines its own outputs against test failures
- Key insight: the quality of injected context (examples, references, constraints) matters more than instruction wording

**Source**: [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (HIGH)

### Co-Optimization: Prompts + Topology

Recent research (Feb 2025) shows that in multi-agent systems, **prompt optimization and topology optimization must be co-optimized**:
- Block-level: optimize individual agent prompts
- Workflow-level: optimize how agents connect and hand off
- Global: optimize the overall system architecture

Optimizing prompts alone without restructuring agent topology leaves **significant performance gains uncaptured**.

**Source**: [arxiv 2502.02533](https://arxiv.org/abs/2502.02533) (HIGH)

### Caution: Moving-Target Problem

A 2025 study ("Prompting Inversion") found that automated prompt sculpting **improves performance on GPT-4o but becomes actively detrimental on GPT-5**. This suggests:
- Automated optimization systems may need to be **model-version-aware**
- Optimizations tuned for one model generation may not transfer
- Human-readable, principled prompt design may be more durable than automated optimization

**Source**: [arxiv](https://arxiv.org/html/2510.22251v1) (MEDIUM)

---

## 17. Skill Description Optimization Deep Dive

_Added: 2026-03-15 | Sources: Anthropic, DEV Community, 650-Trials Study_

### How `improve_description.py` Works Internally

Anthropic's description optimizer uses a **data-driven LLM loop**:

1. **Split** test queries into 60% train / 40% test sets
2. **Run** each description variant 3 times per query (for statistical reliability)
3. **Score** activation rate on train set
4. **Propose** edits based on failure analysis (which queries didn't trigger?)
5. **Evaluate** proposed edits on test set (NOT train set)
6. **Select** the description with the highest test-set score

**Key design choice**: Selection by test-set score prevents **overfitting** — a description that triggers on training queries but fails on unseen queries is rejected.

**Source**: [Anthropic Blog](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) (HIGH), [GitHub SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) (HIGH)

### Empirical Activation Rate Data (650+ Trials)

| Technique | Activation Rate |
|-----------|----------------|
| Basic description (what only) | ~20% |
| Optimized description (what + when) | ~50% |
| Description + "Use when..." clauses with literal phrases | ~90-95% |
| Description + examples in SKILL.md body | 72% → 90% |

**Source**: [Medium: 650 Trials](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1) (MEDIUM)

### Highest-Impact Technique: Explicit Trigger Clauses

The single most effective technique is embedding **"Use when..." clauses with literal user phrases** directly in the description:

```yaml
# BAD (~20% activation)
description: Processes documents and generates reports

# GOOD (~50% activation)
description: Process PDF, Word, and Excel documents to generate formatted reports. Use when working with document files or when asked to create reports from files.

# BEST (~95% activation)
description: Process PDF, Word, and Excel documents to generate formatted reports. Use when the user says "generate a report", "process this document", "convert this PDF", "analyze this spreadsheet", or asks about document processing.
```

**Source**: [DEV Community](https://dev.to/oluwawunmiadesewa/claude-code-skills-not-triggering-2-fixes-for-100-activation-3b57) (MEDIUM)

### Hard Constraints

| Constraint | Limit | Consequence of Violation |
|-----------|-------|------------------------|
| Max length | 1024 characters | Hard truncation — content past 1024 is lost |
| Ideal length | 100-200 words | Verbosity dilutes trigger signal even within 1024 limit |
| Voice | Third person | First/second person degrades discovery (description injected verbatim into system prompt) |
| Required components | "What" + "When" | Missing either reduces activation significantly |

**Source**: [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (HIGH)

### Blind A/B Testing with Comparator Agents

Skill-creator 2.0 uses **comparator agents** for unbiased description evaluation:
- Two description variants are tested against the same query set
- Comparator judges outputs **without knowing which description is active**
- Eliminates evaluator bias (the comparator can't favor the "new" version)
- Enables systematic A/B testing of descriptions at scale

**Source**: [Skills 2.0 Guide](https://www.pasqualepillitteri.it/en/news/341/claude-code-skills-2-0-evals-benchmarks-guide) (MEDIUM), [Geeky Gadgets](https://www.geeky-gadgets.com/anthropic-skill-creator/) (MEDIUM)

---

## 18. Key Insights for Our Skill Generator

_Added: 2026-03-15_

### What We Should Adopt from This Research

1. **Eval-first design** (from Anthropic): Our `validate-skill` should check the same metrics Anthropic's pipeline tracks — pass rate, token cost, description activation. Not just spec compliance.

2. **Train/test splitting for descriptions** (from `improve_description.py`): Our `improve-skill` should test description variants against a split query set to prevent overfitting.

3. **Generator/Critic/Refiner loop** (from multi-agent research): Our `generate-skill` should internally validate its own output before presenting — effectively acting as its own critic.

4. **Blind A/B comparator** (from skill-creator 2.0): Our `improve-skill` should evaluate description alternatives without bias — present variants to the user with objective scoring, not subjective preference.

5. **"Use when..." trigger clauses** (from 650-trial study): Our `generate-skill` must ALWAYS include explicit trigger phrases in generated descriptions. This is the single highest-leverage improvement.

6. **Context engineering mindset** (from Anthropic): Skills are context modifiers, not code. What we inject into context matters more than how we phrase instructions. Our skills should optimize for context quality.

7. **Anti-bias measures for LLM-as-judge** (from academic research): If we use LLM-based evaluation, we must use chain-of-thought scoring, low temperature, and randomized order to avoid position and verbosity biases.

### What We Should NOT Do

1. **Don't over-optimize prompts automatically** — the "Prompting Inversion" study shows automated optimization can be detrimental on newer models. Design principled, human-readable skills instead.

2. **Don't skip evaluation** — most community generators produce unverified skills. Our eval pipeline (validate-skill) is a key differentiator.

3. **Don't bloat skills** — volume ≠ quality. Context pollution from oversized SKILL.md files is the most common failure mode in community generators.

4. **Don't ignore topology** — prompt optimization alone leaves gains uncaptured. The structure of how our skills interact (validate → generate → improve pipeline) matters as much as the individual skill quality.

---

## Sources

| # | Source | URL | Type | Credibility |
|---|--------|-----|------|-------------|
| 1 | Anthropic Official Skills Repo | https://github.com/anthropics/skills | GitHub | HIGH |
| 2 | Skill Authoring Best Practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Official Docs | HIGH |
| 3 | Claude Code Skills Docs | https://code.claude.com/docs/en/skills | Official Docs | HIGH |
| 4 | Anthropic Engineering Blog | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Blog | HIGH |
| 5 | Skills Deep Dive (Lee) | https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/ | Technical Blog | HIGH |
| 6 | SKILL.md Format Spec (DeepWiki) | https://deepwiki.com/anthropics/skills/2.2-skill.md-format-specification | Wiki | MEDIUM |
| 7 | Inside Claude Code Skills (Mikhail) | https://mikhail.io/2025/10/claude-code-skills/ | Technical Blog | HIGH |
| 8 | alirezarezvani/claude-skills | https://github.com/alirezarezvani/claude-skills | GitHub | MEDIUM |
| 9 | alirezarezvani/claude-code-skill-factory | https://github.com/alirezarezvani/claude-code-skill-factory | GitHub | MEDIUM |
| 10 | levnikolaevich/claude-code-skills | https://github.com/levnikolaevich/claude-code-skills | GitHub | MEDIUM |
| 11 | posit-dev/skills | https://github.com/posit-dev/skills | GitHub | HIGH |
| 12 | skills.sh Skill Creator | https://skills.sh/anthropics/skills/skill-creator | Catalog | MEDIUM |
| 13 | Awesome Claude Skills | https://github.com/travisvn/awesome-claude-skills | GitHub | MEDIUM |
| 14 | Anthropic Skill-Creator SKILL.md | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | GitHub | HIGH |
| 15 | Anthropic Blog: Improving skill-creator | https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills | Blog | HIGH |
| 16 | Anthropic: Context Engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Blog | HIGH |
| 17 | Anthropic Complete Guide PDF | https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf | PDF | HIGH |
| 18 | arxiv: Position Bias in LLM-as-Judge | https://arxiv.org/abs/2406.07791 | Paper | HIGH |
| 19 | arxiv: Multi-Agent Prompt+Topology Optimization | https://arxiv.org/abs/2502.02533 | Paper | HIGH |
| 20 | arxiv: LLM Judge Biases | https://arxiv.org/html/2410.02736v1 | Paper | HIGH |
| 21 | DSPy Optimizers Docs | https://dspy.ai/learn/optimization/optimizers/ | Docs | HIGH |
| 22 | DeepWiki: Skill Creator | https://deepwiki.com/anthropics/skills/4-skill-creator | Wiki | MEDIUM |
| 23 | Tessl.io: Evals in skill-creator | https://tessl.io/blog/anthropic-brings-evals-to-skill-creator-heres-why-thats-a-big-deal/ | Blog | MEDIUM |
| 24 | Medium: 650 Trials Activation Study | https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1 | Blog | MEDIUM |
| 25 | MindStudio: Common Mistakes Guide | https://www.mindstudio.ai/blog/claude-code-skills-common-mistakes-guide | Blog | MEDIUM |
| 26 | DEV Community: Activation Fixes | https://dev.to/oluwawunmiadesewa/claude-code-skills-not-triggering-2-fixes-for-100-activation-3b57 | Blog | MEDIUM |
| 27 | EvidentlyAI: LLM-as-Judge Guide | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | Guide | MEDIUM |
| 28 | Braintrust: Best Eval Tools 2025 | https://www.braintrust.dev/articles/best-prompt-evaluation-tools-2025 | Blog | MEDIUM |
| 29 | Maxim.ai: Eval Frameworks | https://www.getmaxim.ai/articles/prompt-evaluation-frameworks-measuring-quality-consistency-and-cost-at-scale/ | Blog | MEDIUM |
| 30 | Skills 2.0 Guide (Pillitteri) | https://www.pasqualepillitteri.it/en/news/341/claude-code-skills-2-0-evals-benchmarks-guide | Blog | MEDIUM |
| 31 | arxiv: Prompting Inversion | https://arxiv.org/html/2510.22251v1 | Paper | MEDIUM |
| 32 | GitHub: mingrath/awesome-claude-skills | https://github.com/mingrath/awesome-claude-skills | GitHub | MEDIUM |
| 33 | Optimas/SuperOptiX | https://medium.com/@shashikant.jagtap/optimas-superoptix-global-reward-optimization-for-dspy-crewai-autogen-and-openai-agents-sdk-29257eff039d | Blog | MEDIUM |
| 34 | Geeky Gadgets: Skills 2.0 | https://www.geeky-gadgets.com/anthropic-skill-creator/ | Blog | MEDIUM |
