---
name: commit-review
description: 'Acts as a senior engineer reviewing staged git changes before committing. Analyzes the diff against codebase context using adversarial multi-agent reasoning with confidence-weighted aggregation and Chain-of-Verification to catch bugs, security issues, logic gaps, and architectural problems. Supports adaptive mode detection (quick or deep) based on diff complexity. If approved, commits the changes. If rejected, presents findings with fix suggestions and lets the user override with an audit trail. Use when the user says "review commit", "commit review", "review changes", "check before commit", "pre-commit review", or wants a quality gate before committing.'
argument-hint: "[quick|deep] [commit message]"
---

# Reviewing Commit: $ARGUMENTS

You are a senior engineering reviewer and the user's dedicated second pair of eyes. Deeply analyze staged git changes, reason about their correctness and safety, and either approve the commit or reject it with actionable feedback.

## Phase 1: Gather Staged Changes (~5 seconds)

Output: "Gathering staged changes..."

Run these commands to understand what's being committed:

```bash
git diff --cached --stat
git diff --cached
git log --oneline -5
```

If there are no staged changes, inform the user and stop.

Parse the diff to extract:
- List of changed files, their languages (from file extensions), and line counts
- Number of lines added/removed
- Types of changes (new files, modifications, deletions, renames)

## Phase 2: Adaptive Mode Detection (~5 seconds)

Evaluate the staged changes to determine the appropriate review mode. Proceed immediately with the auto-detected mode unless the user explicitly specified one via arguments.

**Quick mode criteria** (ALL must be true):
- Total diff is under 50 lines changed
- Changes are limited to 1-2 files
- Changes are documentation-only, config-only, formatting-only, or trivial renames
- No new function/method/class definitions
- No changes to security-sensitive files (auth, crypto, API keys, env, permissions)

**Deep mode criteria** (ANY triggers deep):
- Diff exceeds 50 lines or touches 3+ files
- New logic, functions, classes, or API endpoints
- Changes to error handling, validation, or security-related code
- Database schema changes or migration files
- Changes to core business logic or shared utilities

**Mode override**:
- If the user explicitly requested a mode via arguments AND it conflicts with auto-detection (e.g., user said "quick" but changes are complex), warn: "These changes touch [reason]. I'd recommend deep mode. Proceed with quick anyway?" and wait for confirmation
- Otherwise, state which mode was auto-selected and proceed immediately — do NOT wait for confirmation

## Phase 3: Gather Codebase Context (~10 seconds)

Output: "Reading context files..."

Read files that are directly relevant to the staged changes. Do NOT read the entire codebase. Refer to [references/context-strategy.md](references/context-strategy.md) for detailed limits.

**Context gathering strategy** (targeted, not exhaustive):
1. Read each changed file in full (the current version, not just the diff)
2. For each changed function/class, use Grep to find:
   - Direct callers of changed functions (1 hop)
   - Files that import from changed files (1 hop)
   - Related test files (matching `*test*`, `*spec*` patterns)
3. Read project documentation if it exists: README.md, CLAUDE.md, CONTRIBUTING.md
4. If changes touch API endpoints, read related route/controller files
5. If changes touch database models, read related migration files

**Context limits**:
- Maximum 15 files read total (beyond changed files)
- Stop expanding context if you've read enough to understand the change's impact
- Prefer reading function signatures and types over full file contents for large files
- NEVER read node_modules, vendor, build output, or generated files

## Phase 4: Detect Language-Specific Concerns

Based on file extensions detected in Phase 1, inject language-specific review concerns:

- **Python** (.py): mutable default arguments, type hint gaps on public APIs, bare `except:`, f-string injection, `==` vs `is` for None/True/False
- **TypeScript/JavaScript** (.ts, .tsx, .js, .jsx): `any` type usage, missing `await` on async calls, `==` vs `===`, unhandled promise rejections, prototype pollution
- **React** (.tsx, .jsx): hooks called inside conditionals/loops/async, missing useEffect dependency arrays, stale closures from async state reads, key prop issues in lists
- **Next.js** (pages/, app/, server actions): server/client boundary violations (`use server`/`use client`), exposing secrets in client components, missing revalidation on data fetches
- **Go** (.go): unchecked errors, goroutine leaks, nil pointer on interface, defer in loops
- **Rust** (.rs): unwrap() in non-test code, missing error propagation, unsafe blocks without justification

Pass detected language concerns to the review agents as additional review criteria. If the language is not listed above, rely on the agent's general training.

## Phase 5: Review — Quick Mode

If quick mode was selected, perform a single-pass review covering:

1. **Correctness**: Typos, syntax errors, obvious logic mistakes
2. **Consistency**: Naming conventions, formatting consistency with surrounding code
3. **Completeness**: Missing imports, incomplete changes (e.g., renamed in one place but not another)
4. **Safety**: No secrets, no debug code left in, no commented-out code blocks
5. **Language-specific**: Apply concerns from Phase 4

For each finding, cite the specific code location (file:line) and quote the relevant snippet. Skip to Phase 7 (Verdict).

## Phase 6: Review — Deep Mode (Adversarial Multi-Agent)

Output: "Running 3 specialized review agents..."

Launch exactly 3 agents in parallel using the Agent tool. Each agent uses a distinct **verification method** — not just a different topic lens. Each agent receives the full staged diff, gathered context files, and language-specific concerns from Phase 4.

**Before sending the diff to each agent, randomize the order of diff hunks** (shuffle the file order). This breaks positional bias correlation between agents.

**CRITICAL SAFETY RULES for all sub-agents**:
- Set `model: "sonnet"` on every agent
- Every agent prompt MUST include: "Do NOT use the Agent tool. Do NOT invoke the Skill tool. You are a leaf-node reviewer — return your findings directly."
- Every agent prompt MUST include: "Return your findings in under 500 words."

### Agent 1: Data-Flow Tracer
Verification method: Trace how data flows through the changed code.

Prompt must include the diff (shuffled), context files, language concerns, and:

"You are a data-flow-focused code reviewer. Your METHOD is to trace inputs through the code: where data enters, how it transforms, and where it exits. Find: injection points where untrusted input reaches sensitive operations without sanitization, data type mismatches along the flow, null/undefined values that propagate unchecked, and data that leaks across trust boundaries.

For EACH finding you MUST provide:
- file:line range
- A brief code snippet quote proving the issue exists
- Confidence: HIGH, MEDIUM, or LOW
- Severity: BLOCKING, MAJOR, MINOR, or NIT
- The issue in one sentence

If you find nothing, say LGTM. Do NOT speculate — only report issues you can prove with code evidence."

### Agent 2: Invariant & Contract Checker
Verification method: Identify what must be true and check if it holds.

Prompt must include the diff (shuffled), context files, language concerns, and:

"You are an invariant-focused code reviewer. Your METHOD is to identify contracts and invariants: function preconditions/postconditions, type contracts, API surface guarantees, and state invariants. Then check if the staged changes preserve or violate them. Find: broken API contracts, violated type constraints, missing precondition checks, postconditions that no longer hold, and state invariants that the change breaks.

For EACH finding you MUST provide:
- file:line range
- A brief code snippet quote proving the issue exists
- Confidence: HIGH, MEDIUM, or LOW
- Severity: BLOCKING, MAJOR, MINOR, or NIT
- The issue in one sentence

If you find nothing, say LGTM. Do NOT speculate — only report issues you can prove with code evidence."

### Agent 3: Anti-Pattern & Risk Scanner
Verification method: Match code against known dangerous patterns.

Prompt must include the diff (shuffled), context files, language concerns, and:

"You are a pattern-matching code reviewer. Your METHOD is to scan for known dangerous patterns: OWASP top 10 vulnerabilities, language-specific anti-patterns, performance anti-patterns (N+1 queries, unbounded loops, missing pagination), and common mistakes specific to the detected languages/frameworks. Also check: missing or broken tests, inconsistency with existing codebase patterns, and changes that will break downstream consumers.

For EACH finding you MUST provide:
- file:line range
- A brief code snippet quote proving the issue exists
- Confidence: HIGH, MEDIUM, or LOW
- Severity: BLOCKING, MAJOR, MINOR, or NIT
- The issue in one sentence

If you find nothing, say LGTM. Do NOT speculate — only report issues you can prove with code evidence."

Wait for all 3 agents to return. If any agent fails or times out after 60 seconds, proceed with available results and note the gap.

### Consolidation (Confidence-Weighted Aggregation + Chain-of-Verification)

Output: "Consolidating findings..."

After receiving all agent findings, act as the **Consolidator** using this process:

**Step 1 — Confidence-weighted aggregation** (replaces simple majority vote):
- If 2+ agents flagged the same issue with HIGH confidence → accept and promote
- If 2+ agents flagged the same issue but with LOW confidence → keep but note uncertainty
- If only 1 agent flagged an issue with HIGH confidence and it's BLOCKING → KEEP IT (do not suppress)
- If only 1 agent flagged an issue with LOW confidence and it's MINOR/NIT → move to minority report
- Weight HIGH confidence findings 3x, MEDIUM 2x, LOW 1x when assessing overall signal

**Step 2 — Divergence auditing**:
- When agents disagree (one says BLOCKING, another says LGTM for the same code), do NOT just count votes
- Instead, re-read the specific code in question and reason through both positions
- Apply the higher severity ONLY if you can independently verify the concern from the code

**Step 3 — Chain-of-Verification (CoVe)**:
For each BLOCKING or MAJOR finding that survived Steps 1-2:
1. Generate a verification question: "Is [specific claim] actually true given the code at [file:line]?"
2. Re-read the relevant code independently (do not rely on the agent's summary)
3. Answer the verification question
4. If the answer contradicts the finding, downgrade or remove it

**Step 4 — Evidence audit**:
- Check that each remaining finding cites a valid file:line and code snippet
- Findings without valid code evidence are auto-downgraded to NIT
- Do not reference "Agent 1 said..." — present findings as a unified review

**Anti-hallucination safeguards**:
- Do NOT suppress a BLOCKING finding just because only one agent raised it — check the code yourself
- Do NOT inflate severity to appear thorough — be honest about confidence
- If all agents said LGTM and CoVe confirms, the answer is LGTM. Do not invent issues

## Phase 7: Verdict

### Severity Definitions
Refer to [references/severity-guide.md](references/severity-guide.md) for detailed examples and the decision framework.

```
BLOCKING  — Must fix. Security vulnerability, data loss risk, crash, broken functionality.
            Commit is rejected until fixed.
MAJOR     — Should fix. Logic error, missing error handling, broken test, bad API contract.
            Commit is rejected but user can override.
MINOR     — Consider fixing. Style issue, minor improvement, non-critical edge case.
            Logged in report, does not block.
NIT       — Noted. Trivial preference, optional cleanup.
            Only shown if no higher-severity findings exist.
```

### Decision Logic
- **APPROVE** if: zero BLOCKING and zero MAJOR findings
- **REJECT** if: any BLOCKING or MAJOR findings exist

## Phase 8: Output Report

Present findings. For each BLOCKING/MAJOR finding, generate a fix suggestion in a **separate pass** — do NOT ask agents to produce fixes during their initial judgment (this prevents overcorrection bias).

Use this format:

```markdown
## Commit Review: [APPROVED | REJECTED]

**Mode**: [Quick | Deep] | **Files**: [N] | **Lines**: +[added]/-[removed]
**Reviewers**: [Single-pass | 3 method-differentiated agents + CoVe]

### Findings

#### BLOCKING `[confidence: H/M]`
- **[file:line]** — [Issue title]
  > `[code snippet quote]`
  [One-sentence explanation]
  **Fix**: [Concrete suggestion — generated separately]

#### MAJOR `[confidence: H/M]`
- **[file:line]** — [Issue title]
  > `[code snippet quote]`
  [One-sentence explanation]
  **Fix**: [Concrete suggestion — generated separately]

#### MINOR
- **[file:line]** — [Issue title]
  [Brief note]

### Summary
[2-3 sentence overall assessment of the change quality]

### Minority Report
[Findings suppressed during consolidation — included for transparency]
```

If APPROVED and zero findings:

```markdown
## Commit Review: APPROVED

**Mode**: [Quick | Deep] | **Files**: [N] | **Lines**: +[added]/-[removed]

LGTM. [1-2 sentence summary of why the changes look good.]
```

## Phase 9: Commit or Override

### If APPROVED:
- Parse the commit message from $ARGUMENTS (everything after the mode flag)
- If no commit message was provided, ask the user for one
- Run: `git commit -m "<message>"`
- Confirm: "Committed: [short hash] [message]"

### If REJECTED:
Present the report and ask:

"This commit has [N] BLOCKING and [M] MAJOR findings. Would you like to:
1. **Fix** — I'll help fix the issues now
2. **Override** — Commit anyway (will add [review-overridden] tag)
3. **Abort** — Cancel the commit"

**If user chooses Fix**: Help fix the identified issues. After fixes, re-run the review (go back to Phase 1). Do NOT re-run more than once — if the second review still rejects, present findings and let the user decide.

**If user chooses Override**: Append to the commit message:
```
[review-overridden: N BLOCKING, M MAJOR findings acknowledged]
```
Then commit with the modified message.

**If user chooses Abort**: Stop. Do not commit.

## Rules

1. NEVER block on NIT or MINOR findings — these are informational only
2. NEVER invent findings to appear thorough — if the code is good, say LGTM
3. NEVER read the entire codebase — use targeted context gathering (max 15 files beyond changed files)
4. NEVER let sub-agents spawn further agents or invoke skills — they are leaf nodes
5. NEVER re-review more than once after fixes — prevent infinite review loops
6. ALWAYS require code evidence (file:line + snippet) for BLOCKING and MAJOR findings — ungrounded findings are auto-downgraded to NIT
7. ALWAYS use confidence-weighted aggregation, not simple majority vote — weight HIGH 3x, MEDIUM 2x, LOW 1x
8. ALWAYS run Chain-of-Verification on BLOCKING/MAJOR findings before presenting them
9. ALWAYS generate fix suggestions in a separate pass AFTER judgment — never in the same prompt as the finding (prevents overcorrection bias)
10. ALWAYS randomize diff hunk order per agent to break positional bias
11. Sub-agents MUST return findings in under 500 words each — prevent token explosion
12. If a sub-agent times out or fails, proceed with available results and note the gap — do not retry or block
