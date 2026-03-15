# deep-research-improve-skill

> Improve existing Claude Code skills with exhaustive two-round research — including an Opus skeptic that defends the current approach when it's already optimal.

Most skill improvers suggest changes based on generic best practices. This one researches your skill's specific domain first — finding best-in-class examples, evolving standards, and common quality issues — then uses a dedicated Opus skeptic to challenge every improvement assumption. Sometimes the best improvement is no change at all.

## Why Use This

- **Research-backed improvements** — Every suggestion is tagged with confidence level (HIGH/MEDIUM/LOW) so you can prioritize
- **Skeptic defends the status quo** — The Opus skeptic actively looks for evidence that the current approach is already optimal, preventing unnecessary churn
- **Domain-specific insights** — Goes beyond generic best practices to find what the best tools in your skill's domain actually do
- **Transparent reasoning** — Challenged improvements are tagged `[Skeptic: challenged]` so you know which suggestions were contested

## Quick Start

```
/deep-research-improve-skill .claude/skills/research
```

## Usage

```
/deep-research-improve-skill <path/to/skill-directory>
```

### Examples

- `/deep-research-improve-skill output/my-custom-skill`
- `/deep-research-improve-skill ~/.claude/skills/generate-skill`
- `/deep-research-improve-skill .claude/skills/deploy-k8s`
- `/deep-research-improve-skill output/deep-research`

## How It Works

The skill runs a 10-phase pipeline in ~15-17 minutes:

| Phase | Time | Model | What Happens |
|-------|------|-------|-------------|
| 1. Read & Understand | ~30s | Parent | Reads entire skill directory (SKILL.md + references + scripts) |
| 2. Research Plan | ~30s | Parent | Identifies 4-6 research themes using improvement lenses |
| 3. Broad Sweep (R1) | ~3 min | Sonnet | 4-6 parallel agents benchmark against best-in-class tools |
| 4. Gap Analysis | ~1 min | **Opus** | Identifies weak research areas + 2-3 improvement assumptions to challenge |
| 5. Deep Dives (R2) | ~3 min | Sonnet + **Opus** | Collectors fill gaps + skeptic defends the current approach |
| 6. Improvement Context | ~1.5 min | **Opus** | Synthesizes findings with confidence levels and priority ranking |
| 7. Validate | ~30s | Parent | Runs 13+ automated checks on current skill |
| 8. Identify Improvements | ~1 min | Parent | Categorizes by priority, tags with confidence and skeptic status |
| 9. Present Plan | — | Parent | Shows improvement plan with apply options |
| 10. Apply & Summarize | ~1 min | Parent | Creates .bak backup, applies approved changes, re-validates |

## Example Output

The improvement plan looks like this:

```markdown
# Deep Research Improvement Plan: research
_Analyzed: 2026-03-15 | Research: 18 sources | Rounds: 2 | Confidence: High_

## Current Assessment
The skill is well-structured with clear phases and good activation triggers.
Overall: GOOD

## Deep Research Insights
- Best-in-class research tools use iterative rounds, not single-pass [Confidence: HIGH]
- 58% of users prefer explicit confidence scores on findings [Confidence: MEDIUM]

## Skeptic's Assessment
- "Add citation chain following" was challenged — current approach already handles
  cross-referencing adequately for single-round research
- "Switch to tiered models" survived scrutiny — genuine quality improvement

## Proposed Changes

### High Priority
1. `[Research: HIGH]` **Add per-finding confidence tags**: Research shows users
   want explicit uncertainty. Add [Confidence: H/M/L] to each finding.
2. **Update description triggers**: Missing "investigate" and "analyze" as
   trigger phrases.

### Medium Priority
1. `[Skeptic: challenged]` **Add citation chain following**: Skeptic found
   this adds complexity without proportional benefit for single-round research.
   Recommendation: defer to /deep-research instead.

## Apply Changes?
- "apply all" / "apply critical+high" / "show diff" / specify by number
```

## When to Use This vs Alternatives

| Need | Use | Time |
|------|-----|------|
| Quick best-practice check | `/improve-skill` | ~3 min |
| Some research on the domain | `/research-improve-skill` | ~8 min |
| **Maximum quality with adversarial review** | **`/deep-research-improve-skill`** | **~15 min** |

Use this when the skill is important enough to warrant thorough review, when you want evidence-based improvements rather than generic suggestions, or when you want to be sure proposed changes are actually improvements.

## Tools Used

| Tool | Purpose |
|------|---------|
| Read | Read existing skill files and references |
| Write | Apply improvements, create backups |
| Bash(python *) | Run validation script |
| Grep | Search for patterns in skill files |
| Glob | Find files in skill directory |
| WebSearch | Research the skill's domain |
| WebFetch | Fetch full page content when needed |

## Safety: Anti-Recursion Guards

All sub-agents are spawned as `deep-researcher` type (never `general-purpose`), which restricts their tool access to WebSearch, WebFetch, Read, Write, Grep, and Glob. This structurally prevents agents from spawning further sub-agents or invoking skills. Every agent prompt also includes an explicit anti-recursion instruction as defense-in-depth.

## Limitations & Edge Cases

- **Time cost**: ~15 minutes per skill. Use `/improve-skill` for quick fixes where deep research isn't needed.
- **Improvement bias**: Despite the skeptic, the skill may still suggest changes that aren't strictly necessary. Always review before applying.
- **Domain coverage**: Research quality depends on how well-documented the skill's domain is online.
- **Backup safety**: Always creates `.bak` backup before changes, but verify the backup exists before applying.
- **Won't change purpose**: The skill improves execution, not purpose. If the fundamental approach is wrong, manual redesign is needed.

## Sources & References

- [Deep Research Agent Survey (arXiv)](https://arxiv.org/pdf/2508.12752) — Multi-round architecture for iterative investigation
- [Heterogeneous Agent Debate (Springer)](https://link.springer.com/article/10.1007/s44443-025-00353-3) — Diverse model tiers improve accuracy (~91% vs ~82%)
- [LLM Debate Limitations (arXiv)](https://arxiv.org/html/2511.07784v1) — "Minority correction asymmetry" — why skeptic must challenge majority
- [Adversarial Debate for Hallucination Reduction (MDPI)](https://www.mdpi.com/2076-3417/15/7/3676) — Cross-verification via voting mechanisms
- [D3 Framework (arXiv)](https://arxiv.org/abs/2410.04663) — Role-specialized adversarial evaluation
- [Red Teaming Guide (Promptfoo)](https://www.promptfoo.dev/docs/red-team/) — Multi-turn adversarial patterns for finding weaknesses
- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Official quality standards for skills

## Installation

This skill is part of the core toolkit. To install manually:

```bash
cp -r output/deep-research-improve-skill ~/.claude/skills/deep-research-improve-skill
```

Or: `/implement-skill deep-research-improve-skill`

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Python 3.6+ (for validation script)
- Internet access (for research phases)

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit) (deep-research mode)_
