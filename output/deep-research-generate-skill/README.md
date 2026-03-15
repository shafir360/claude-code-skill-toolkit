# deep-research-generate-skill

> Generate Claude Code skills backed by exhaustive two-round research — with adversarial review of domain findings before generation.

Most skill generators create skills based on what the AI already knows. This one investigates first. It runs two rounds of parallel research to understand your skill's domain — existing tools, best practices, failure modes — then uses an Opus skeptic agent to challenge those findings before generating. The result is a skill informed by real-world evidence with documented confidence levels.

## Why Use This

- **Two research rounds before generation** — Broad sweep finds the landscape, gap analysis spots what's missing, targeted dives fill the gaps
- **Opus skeptic challenges domain findings** — So your skill isn't built on assumptions that seem right but aren't
- **Per-finding confidence in the design brief** — You can see exactly how well-supported each design decision is
- **Better skills for unfamiliar domains** — When you don't know the domain, the research does the learning for you

## Quick Start

```
/deep-research-generate-skill a skill that manages PostgreSQL database migrations with rollback support
```

## Usage

```
/deep-research-generate-skill <description of what the skill should do>
```

### Examples

- `/deep-research-generate-skill a skill that reviews pull requests for security vulnerabilities`
- `/deep-research-generate-skill a skill that converts OpenAPI specs into typed client libraries`
- `/deep-research-generate-skill a skill that manages Kubernetes deployments with canary releases and auto-rollback`
- `/deep-research-generate-skill a skill that generates comprehensive test suites from function signatures`

## How It Works

The skill runs a 9-phase pipeline in ~15-17 minutes:

| Phase | Time | Model | What Happens |
|-------|------|-------|-------------|
| 1. Requirements | ~1 min | Parent | Analyzes description, asks up to 3 clarifying questions |
| 2. Research Plan | ~30s | Parent | Identifies 4-6 research themes with specific questions |
| 3. Broad Sweep (R1) | ~3 min | Sonnet | 4-6 parallel agents collect domain data using structured output |
| 4. Gap Analysis | ~1 min | **Opus** | Identifies gaps, contradictions, claims to challenge |
| 5. Deep Dives (R2) | ~3 min | Sonnet + **Opus** | 3-4 collectors target gaps + 1 skeptic challenges findings |
| 6. Design Brief | ~1.5 min | **Opus** | Synthesizes into Enhanced Design Brief with confidence levels |
| 7. Design | ~30s | Parent | Chooses structure, pattern, model strategy based on research |
| 8. Generate | ~2 min | Parent | Writes SKILL.md, references/, scripts/, README.md |
| 9. Validate | ~1 min | Parent | Runs 13+ checks, self-checks against Phase 1 requirements |

## Example Output

The skill produces a directory like this:

```
output/manage-migrations/
├── SKILL.md                    # Complete skill with research-informed rules
├── RESEARCH_BRIEF.md           # Enhanced design brief with confidence levels
├── README.md                   # Full documentation
└── references/
    └── migration-patterns.md   # Domain-specific reference (if needed)
```

The RESEARCH_BRIEF.md includes per-finding confidence:

```markdown
# Enhanced Design Brief: manage-migrations
_Generated: 2026-03-15 | Sources: 22 | Rounds: 2 | Confidence: High_

## Prior Art
- pg-migrate and node-pg-migrate are the most popular tools `[Confidence: HIGH]`
- Most tools lack automatic rollback on partial failure `[Confidence: MEDIUM]`

## Pitfalls to Avoid
- Migration ordering bugs when multiple developers work in parallel `[Confidence: HIGH]`
- Schema drift between environments `[Confidence: HIGH]`

## Contradictions & Open Questions
- Debate on whether migrations should be reversible by default (some argue irreversibility is safer)
```

## When to Use This vs Alternatives

| Need | Use | Time |
|------|-----|------|
| Quick skill, familiar domain | `/generate-skill` | ~2 min |
| Some research, moderate quality | `/research-generate-skill` | ~8 min |
| **Maximum quality, unfamiliar domain** | **`/deep-research-generate-skill`** | **~15 min** |

Use this when the domain is unfamiliar, when the skill is important enough to get right the first time, or when you want documented evidence for why the skill is designed the way it is.

## Tools Used

| Tool | Purpose |
|------|---------|
| Read | Read reference files and existing patterns |
| Write | Create SKILL.md, references, README, RESEARCH_BRIEF |
| Bash(python *) | Run validation script |
| Bash(mkdir *) | Create output directories |
| Grep | Search codebase for patterns |
| Glob | Find files by pattern |
| WebSearch | Research the skill's domain |
| WebFetch | Fetch full page content when needed |

## Safety: Anti-Recursion Guards

All sub-agents are spawned as `deep-researcher` type (never `general-purpose`), which restricts their tool access to WebSearch, WebFetch, Read, Write, Grep, and Glob. This structurally prevents agents from spawning further sub-agents or invoking skills. Every agent prompt also includes an explicit anti-recursion instruction as defense-in-depth.

## Timeout & Fallback Safety

To prevent agent hangs and cascading timeouts during the research phases:

- **Round 1 timeout**: Maximum 10 minutes for parallel agent batch. If fewer than 3 agents return by deadline, Round 2 is skipped and the skill proceeds directly to synthesis.
- **Round 2 timeout**: Maximum 8 minutes for collectors + skeptic agents. If agents don't complete by deadline, synthesis proceeds with available results.
- **WebFetch fallback**: If a WebFetch request fails or times out, the agent automatically falls back to using the search snippet instead of blocking.
- **Replacement agent cap**: If Round 1 returns fewer than 3 agents, at most one replacement batch is launched. If still fewer than 3 after replacement, synthesis proceeds with available data and flags the limitation.
- **Graceful degradation**: If Round 1 succeeds with 3+ agents, skill generation can proceed even if Round 2 research fails entirely. Quality degrades gracefully rather than failing completely.
- **Overall pipeline timeout**: 15 minutes total for research and generation. If any phase exceeds its budget by 50%, remaining sub-phases are skipped and the skill proceeds to generation.

These safeguards ensure the skill completes and generates output even when facing slow networks, hanging URLs, or partial agent failures.

## Limitations & Edge Cases

- **Time cost**: ~15 minutes is significantly longer than standard generation (~2 min). Use `/generate-skill` for familiar domains where you don't need research.
- **Internet required**: Research phases need WebSearch and WebFetch access.
- **Research quality varies by domain**: Well-documented domains (web dev, databases) produce better research than niche or brand-new topics.
- **Research != correctness**: The skeptic agent reduces false confidence, but research findings still need human judgment for critical applications.
- **500-line limit**: Generated SKILL.md files stay under 500 lines per spec. Very complex skills may need manual refinement of the references/ structure.

## Sources & References

- [Deep Research Agent Survey (arXiv)](https://arxiv.org/pdf/2508.12752) — Two-round architecture is standard across all leading systems
- [Heterogeneous Agent Debate (Springer)](https://link.springer.com/article/10.1007/s44443-025-00353-3) — ~91% vs ~82% accuracy with tiered models
- [LLM Debate Limitations (arXiv)](https://arxiv.org/html/2511.07784v1) — Why skeptic must challenge majority regardless of confidence
- [D3 Framework (arXiv)](https://arxiv.org/abs/2410.04663) — Confidence-weighted adversarial evaluation
- [Skill Activation Research](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1) — "Use when..." clauses push activation from ~20% to ~95%
- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Official guidance on effective skill design
- [Retrieval-Augmented Code Generation (arXiv)](https://arxiv.org/abs/2510.04905) — Research-informed generation improves completion accuracy
- [Context Rot Research (Chroma)](https://research.trychroma.com/context-rot) — Why research briefs must be summarized, not dumped verbatim

## Installation

This skill is part of the core toolkit. To install manually:

```bash
cp -r output/deep-research-generate-skill ~/.claude/skills/deep-research-generate-skill
```

Or: `/implement-skill deep-research-generate-skill`

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Python 3.6+ (for validation script)
- Internet access (for research phases)

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit) (deep-research mode)_
