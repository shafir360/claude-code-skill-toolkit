# commit-review

> Your dedicated second pair of eyes — a senior engineering reviewer that catches bugs, security issues, and architectural problems in your staged changes before you commit.

Built for **solo developers** who don't have a team to review their code. This skill acts as a final quality gate before committing, using adversarial multi-agent reasoning with confidence-weighted aggregation and Chain-of-Verification to surface real issues — not noise. Adaptive mode detection handles trivial and complex changes appropriately.

## Why Use This

- **Solo dev's second opinion**: Fills the gap of not having a teammate to catch blind spots
- **Evidence-grounded findings**: Every issue must cite specific code (file:line + snippet) — no hallucinated bug reports
- **Low noise**: Confidence-weighted aggregation + Chain-of-Verification replaces naive majority voting, eliminating "hallucination consensus"
- **Respects your flow**: Adaptive mode detection, progress indicators, structured override when you disagree

## Quick Start

```
/commit-review fix authentication bug
```

## Usage

```
/commit-review [quick|deep] [commit message]
```

### Examples

- `/commit-review quick update README formatting` — fast single-pass review
- `/commit-review deep refactor payment processing` — full adversarial review
- `/commit-review add user profile endpoint` — auto-detects mode based on diff

## How It Works

| Phase | Timing | Description |
|-------|--------|-------------|
| 1. Gather Changes | ~5s | Reads staged diff, extracts file list and change stats |
| 2. Adaptive Mode | ~5s | Auto-detects quick/deep based on diff complexity, proceeds immediately |
| 3. Gather Context | ~10s | Reads changed files + 1-2 hop dependencies (max 15 extra files) |
| 4. Language Detection | instant | Injects language-specific review concerns (Python, TS, React, Next.js, etc.) |
| 5/6. Review | 10s-2min | Quick: single-pass. Deep: 3 method-differentiated agents |
| 7. Verdict | instant | APPROVE (zero blocking/major) or REJECT |
| 8. Report | instant | Evidence-grounded findings with severity, code quotes, and fix suggestions |
| 9. Commit/Override | user input | Commits if approved, offers fix/override/abort if rejected |

### Deep Mode: Method-Differentiated Agents

In deep mode, three agents run in parallel — each using a **distinct verification method** (not just a different topic lens). Each agent receives the diff in a **randomized hunk order** to break positional bias:

1. **Data-Flow Tracer** — Traces inputs through code: where data enters, transforms, and exits. Catches injection, type mismatches, null propagation.
2. **Invariant & Contract Checker** — Identifies what must be true (preconditions, postconditions, type contracts) and checks if the change breaks it.
3. **Anti-Pattern & Risk Scanner** — Matches against known dangerous patterns: OWASP top 10, language-specific anti-patterns, performance issues.

### Consolidation Pipeline

1. **Confidence-weighted aggregation** — HIGH findings weighted 3x, MEDIUM 2x, LOW 1x (replaces naive majority vote)
2. **Divergence auditing** — When agents disagree, re-reads the code to resolve rather than just counting votes
3. **Chain-of-Verification (CoVe)** — For each BLOCKING/MAJOR finding, generates and answers verification questions independently
4. **Evidence audit** — Findings without valid file:line + code snippet are auto-downgraded to NIT

## Example Output

```markdown
## Commit Review: REJECTED

**Mode**: Deep | **Files**: 4 | **Lines**: +127/-23
**Reviewers**: 3 method-differentiated agents + CoVe

### Findings

#### BLOCKING [confidence: HIGH]
- **src/auth/login.ts:45** — SQL injection via unsanitized email parameter
  > `const user = db.query(\`SELECT * FROM users WHERE email = '${email}'\`)`
  User email is interpolated directly into SQL query without parameterization.
  **Fix**: Use parameterized query: `db.query('SELECT * FROM users WHERE email = ?', [email])`

#### MAJOR [confidence: HIGH]
- **src/api/users.ts:89** — Missing pagination on user list endpoint
  > `const users = await User.findAll()`
  Returns unbounded results; will cause OOM on large datasets.
  **Fix**: Add `limit` and `offset` parameters, default to 50 results.

#### MINOR
- **src/utils/format.ts:12** — Unused import `dayjs`
  Imported but never referenced after refactor.

### Summary
The auth change introduces a critical SQL injection vulnerability. The user listing needs pagination.

### Minority Report
- Data-flow tracer noted potential circular dependency between auth/ and users/ modules (LOW confidence, not independently confirmed)
```

## Deep Research Insights

- Majority vote is provably broken for correlated agents (0% recovery on consensus-wrong cases) — replaced with confidence-weighted aggregation + divergence auditing `[Confidence: H]` ([source](https://arxiv.org/html/2602.09341v1))
- Chain-of-Verification reduces hallucinations 50-70% by independently verifying each finding `[Confidence: H]` ([source](https://aclanthology.org/2024.findings-acl.212/))
- Requiring explanations/fixes in the SAME prompt as judgment increases misjudgment rates — this skill separates judgment from fix generation `[Confidence: M]` ([source](https://arxiv.org/abs/2603.00539))
- Role differentiation only works when agents use different verification METHODS, not just different topic lenses `[Confidence: M]` ([source](https://arxiv.org/html/2404.04834v4))
- BugBot's randomized diff order counters positional bias across parallel review passes `[Confidence: M]` ([source](https://cursor.com/blog/building-bugbot))
- Evidence-grounding (requiring code citations) prevents hallucinated bug reports with 92% citation accuracy `[Confidence: H]` ([source](https://arxiv.org/html/2512.12117v1))
- Over-fetching codebase context degrades accuracy — relevance density matters more than raw coverage `[Confidence: H]` ([source](https://research.trychroma.com/context-rot))
- Solo developers need a tool that stays in their flow — pre-commit integration with no context-switching is the key adoption driver `[Confidence: M]` ([source](https://www.michaelagreiler.com/code-review-pitfalls-slow-down/))

## When to Use This vs Alternatives

| Scenario | Use |
|----------|-----|
| Quick sanity check before commit | `/commit-review quick` |
| Complex code changes, unfamiliar areas | `/commit-review deep` |
| Already have a PR open and want review | Use CodeRabbit, Copilot PR review, or similar |
| Want linting/formatting only | Use pre-commit hooks (ESLint, Prettier, Ruff) |
| Team-wide enforcement | Set up CI-based review tools |

## Tools Used

| Tool | Purpose |
|------|---------|
| Bash | Git commands (diff, log, commit) |
| Read | Reading changed files and context |
| Grep | Finding callers, imports, dependencies |
| Glob | Locating test files and related code |
| Agent | Spawning specialized reviewer sub-agents |

## Limitations & Edge Cases

- Deep mode takes 30s-2min depending on diff size — not instant
- Cannot catch runtime-only bugs (integration issues, environment-specific problems)
- Language-specific concerns are built-in for Python, TypeScript, React, Next.js, Go, Rust — other languages use general training
- Very large diffs (1000+ lines) may exceed context limits — consider splitting commits
- Sub-agents are capped at 500 words each to prevent token explosion
- Cannot replace human reviewers for business logic validation or product decisions

## Sources & References

- [Chain-of-Verification Reduces Hallucination (ACL 2024)](https://aclanthology.org/2024.findings-acl.212/) — CoVe technique integrated into consolidation
- [AgentAuditor: Divergence Auditing Outperforms Majority Vote](https://arxiv.org/html/2602.09341v1) — confidence-weighted aggregation design
- [SGCR: Specification-Grounded Code Review (IEEE ASE 2025)](https://arxiv.org/abs/2512.17540) — evidence-grounding framework
- [LLM Overcorrection in Code Review](https://arxiv.org/abs/2603.00539) — why judgment and fix-generation are separated
- [Building a Better BugBot (Cursor)](https://cursor.com/blog/building-bugbot) — randomized diff order technique
- [Graphite: Code Review Comment Types](https://graphite.com/guides/code-review-comment-types) — severity classification
- [Chroma Research: Context Rot](https://research.trychroma.com/context-rot) — context window limits
- [Microsoft CodePlan](https://huggingface.co/papers/2309.12499) — dependency-aware context retrieval

## Installation

```bash
cp -r output/commit-review ~/.claude/skills/commit-review
```

Or: `/implement-skill commit-review`

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Git repository with staged changes

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit) (deep-research mode, improved with deep-research-improve)_
