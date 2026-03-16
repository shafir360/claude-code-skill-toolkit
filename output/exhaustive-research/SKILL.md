---
name: exhaustive-research
description: 'Conducts massive-scale, multi-layered research using a 3-tier model strategy (Haiku pre-screening, Sonnet data collection, Opus synthesis) with hierarchical tree-reduction to process hundreds of sources without overloading any single agent. Accepts optional /deep-research output as bootstrap context. Configurable depth levels: standard (~1hr, ~40 sources), deep (~2hr, ~100 sources), or exhaustive (~4hr, ~300 sources). Produces comprehensive cited reports with per-finding confidence levels, cross-source contradiction analysis, circular sourcing detection, and source quality scoring. Use when the user says "exhaustive research", "massive research", "scale up research", "go deeper", "research everything about", "exhaustive analysis", or needs research far beyond what /deep-research provides.'
argument-hint: "<topic or question> [depth: standard|deep|exhaustive]"
---

# Exhaustive Research: $ARGUMENTS

You are conducting massive-scale research that processes hundreds of sources through a hierarchical tree of agents. This skill uses a **3-tier model strategy**: Haiku for cheap pre-screening, Sonnet for data collection and tree merging, Opus for final synthesis and adversarial review.

Rate source credibility using [references/source-evaluation.md](references/source-evaluation.md).
Use depth parameters from [references/depth-config.md](references/depth-config.md).
Use tree-reduction algorithm from [references/tree-reduction.md](references/tree-reduction.md).
Use screening rubric from [references/screening-rubric.md](references/screening-rubric.md).
Use report template from [references/report-template.md](references/report-template.md).
Use checkpointing and progress reporting from [references/checkpointing.md](references/checkpointing.md).

---

## Pre-Phase: Resume Check

Before starting, check if `{save_dir}/checkpoints/` exists from a prior run:
1. If checkpoint found: display phase reached, timestamp, and source counts. Ask: "Resume from Phase [N+1]? (Y/n)"
2. If user confirms: load checkpoint data, skip to that phase
3. If no checkpoint or user declines: start fresh

---

## Phase 0: Bootstrap Ingestion (~1 minute)

Check if the user provided `/deep-research` output (pasted text or file path).

**If bootstrap provided:**
1. Read the deep-research report
2. Validate: must contain recognizable findings and be >100 words. If malformed, warn user: "Bootstrap input appears incomplete. Starting fresh instead." Set BOOTSTRAP_CONTEXT to empty and proceed.
3. Extract: topic, scope, key findings with confidence levels, source URLs already consulted, known contradictions, knowledge gaps, skeptic results
4. Store as BOOTSTRAP_CONTEXT for all subsequent phases
5. These sources are "Round 0" — do NOT re-fetch any URL listed in the bootstrap
6. Knowledge gaps from the bootstrap become priority targets for Phase 2

**If no bootstrap:**
1. Note: "Starting fresh — no prior research to build on"
2. Set BOOTSTRAP_CONTEXT to empty
3. The skill will work but Phase 2 will generate broader queries to compensate

---

## Phase 1: Objective Clarification (~2-5 minutes)

### 1a: Parse depth from arguments

Check if the user specified depth (e.g., `deep: climate change`). If not, ask.

### 1b: Confirm save location

Ask: "Where should I save the final report?" Offer:
1. `./research-output/<topic-slug>-<date>/` (default — current working directory)
2. Custom path
3. `~/Desktop/<topic-slug>-<date>/`

Store the confirmed path for Phase 9. Immediately create the output directory structure:
- `{save_dir}/mini-reports/` — Phase 4 reader outputs
- `{save_dir}/intermediate/` — Phase 5 merge outputs
- `{save_dir}/round2/` — Phase 7 collector + skeptic outputs
- `{save_dir}/checkpoints/` — Phase checkpoint JSONs

### 1c: Clarify research objective

Ask **2-4 targeted questions** based on the topic and any bootstrap context:
1. "Should I go wide across many subtopics, or deep into specific aspects?"
2. "What decision or action will this research inform?"
3. "Which aspects matter most?" (list 3-4 angles derived from bootstrap or topic)
4. "Are there sources, viewpoints, or time periods to include or exclude?"

If bootstrap context is rich, reduce to 2 questions (depth level + priority angles).

**Wait for user response before continuing.**

### 1d: Research plan

Decompose the topic into **6-10 research themes** (more than deep-research's 4-6). For each theme, define 2-3 search perspectives (STORM persona pattern). Present the plan briefly, then proceed.

---

## Phase 2: Query Generation & Search (~3-10 minutes)

### 2a: Generate diverse search queries

Spawn Sonnet `deep-researcher` agents with `model: "sonnet"` — **1 agent** for Standard, **2** for Deep, **3-4** for Exhaustive. Each agent receives:
- The research plan themes (divided across agents)
- BOOTSTRAP_CONTEXT (so they avoid already-searched areas)
- Instruction to generate 10-30 diverse queries using different perspectives (academic, practitioner, contrarian, historical)
- The anti-recursion instruction from [references/tree-reduction.md](references/tree-reduction.md)

**Sub-timeout**: If query-gen agents don't return within 5 minutes, proceed with whatever queries have been collected.

Collect all queries. Deduplicate (exact match + semantic similarity). Cap at depth-level maximum from [references/depth-config.md](references/depth-config.md).

### 2b: Execute searches

Run all search queries using WebSearch. Collect all result snippets (URL + title + snippet text). Deduplicate by URL (exact match). This produces the candidate pool for screening.

If the candidate pool is smaller than expected (< 50% of depth target), generate 10-20 additional queries with broader terms and search again. Do this at most once.

**Zero results abort**: If total search results < 10 across all queries (including retry), ABORT: "Search returned near-zero results. The topic may be too niche for web research. Suggest broadening the topic or trying a different angle."

**Checkpoint**: Save search results to `checkpoints/phase2_search_results.json`. Emit Phase Recap (see [references/checkpointing.md](references/checkpointing.md)).

---

## Phase 3: Source Pre-Screening (~5-20 minutes)

Spawn **Haiku `deep-researcher` agents** with `model: "haiku"`, one per batch of ~40-50 snippets. Each agent uses the **condensed** screening rubric from [references/screening-rubric.md](references/screening-rubric.md) (the short version, not the full reference doc).

Each screener evaluates every snippet for relevance (1-10), credibility (HIGH/MEDIUM/LOW), and information density (HIGH/MEDIUM/LOW), returning a verdict: PASS, BORDERLINE, or FAIL.

**After all screeners return:**
1. Collect all PASS sources. Sort by composite score (relevance x credibility_weight x density_weight)
2. Take top N sources where N = depth-level target from [references/depth-config.md](references/depth-config.md)
3. If PASS count < target: promote BORDERLINE sources by composite score
4. Exclude any URLs already in BOOTSTRAP_CONTEXT (already read in Round 0)
5. Log all screened sources with verdicts for the methodology section

**Timeout**: If screener agents don't return within phase timeout, proceed with whatever results are available. If fewer than 3 screeners returned, fall back to search-engine ranking (top N by position).

**Early termination checks**:
- If 0 sources pass screening: ABORT immediately. "No sources passed quality screening. The topic may be too niche or queries poorly targeted."
- If <5 sources pass: offer (a) abbreviated single-round synthesis (skip tree reduction), (b) broaden topic and re-search, (c) abort.
- If <20% of candidates passed: pause and ask: "Only [N]% passed screening — queries may be poorly targeted. Continue with reduced depth, refine topic, or abort?"

**Checkpoint**: Save screening verdicts to `checkpoints/phase3_screening_verdicts.json`. Emit Phase Recap.

---

## Phase 4: Deep Reading — Round 1 (~10-40 minutes)

### 4a: Assign sources to reader agents

Divide PASS sources into batches of 5-7. Spawn **Sonnet `deep-researcher` agents** with `model: "sonnet"`, one per batch. Each agent uses the Level 0 reader prompt from [references/tree-reduction.md](references/tree-reduction.md).

Each reader:
- WebFetches up to 2 sources — prioritize the 2 highest composite scores from pre-screening (uses search snippets for the remaining 3-5). If WebFetch fails, continue with snippet only.
- Extracts key claims, data, statistics with citation URLs
- Notes contradictions within its batch
- Produces a structured mini-report (max 800 words)
- Saves mini-report to `{save_dir}/mini-reports/batch_{N}.md`

Launch ALL reader agents in parallel in a single message.

### 4b: Validation gate

After all readers return, spawn **1-2 Haiku `deep-researcher` agents** with `model: "haiku"` (Sonnet for Exhaustive depth) to validate the mini-reports using the validation gate prompt from [references/tree-reduction.md](references/tree-reduction.md). Validators check STRUCTURAL properties only: citation URLs present? metadata block complete? word count in expected range (200-800)? response parseable into expected sections?

Reports marked REJECT are discarded. Reports marked FLAG are kept with warnings attached. Do NOT auto-reject based on semantic quality judgments — structural checks only, since automated semantic quality detection is only ~53% accurate and false positives can cascade.

**Validator sub-timeout**: 5 min (Standard), 8 min (Deep), 12 min (Exhaustive). If validators don't return by sub-timeout, skip validation and mark all reports UNVALIDATED. Proceed to Phase 5.

**Timeout**: If readers don't complete within phase timeout, proceed with available mini-reports. If fewer than 50% return, skip missing agents and note the coverage gap. **If 0 readers return (100% failure)**: save partial report from prior phases, notify user: "Phase 4 complete failure — all reader agents failed. Saving partial report." Do not continue.

Do NOT retry entire batches — each agent's output file is an implicit checkpoint; only agents with missing output files need re-running, and only once.

**Checkpoint**: Save mini-report file paths to `checkpoints/phase4_mini_reports.json`. Emit Phase Recap with Agent Recap showing per-batch outcomes.

---

## Phase 5: Tree Reduction (~5-20 minutes)

### 5a: Level 1 merge

Group mini-reports into batches of 5. Spawn **Sonnet `deep-researcher` agents** with `model: "sonnet"`, one per batch. Each agent uses the Level 1 merge prompt from [references/tree-reduction.md](references/tree-reduction.md).

Each merger:
- Deduplicates claims across mini-reports
- Cross-references for convergent findings and contradictions
- Checks for circular sourcing (multiple reports citing the same original)
- Produces an intermediate report (max 1500 words)

Launch ALL merge agents in parallel.

### 5b: Validation gate (Deep/Exhaustive only)

Spawn 1 Haiku `deep-researcher` validator with `model: "haiku"` (Sonnet for Exhaustive) to check intermediate reports. Sub-timeout: 5 min (Standard), 8 min (Deep), 12 min (Exhaustive). If exceeded, skip validation and proceed.

### 5c: Level 2 merge (Exhaustive only)

If more than 5 intermediate reports remain, repeat: group into batches of 5, spawn **Sonnet `deep-researcher` merge agents** with `model: "sonnet"`, produce condensed reports.

**Hard cap: Tree depth NEVER exceeds 3 levels.** If more than 5 reports remain after Level 2, pass them all directly to the Opus root synthesis in Phase 8.

### 5d: Timeout handling

If any merge agent doesn't return within phase timeout, skip it. If fewer than 50% of merge agents return, the parent concatenates available mini-reports inline as a fallback (lower quality but functional). **If 0 merge agents return (100% failure)**: save partial report from Phase 4 data, notify user. Do not continue.

**High failure check**: If >30% of agents in Phase 5 fail, pause and ask: "Over 30% of merge agents failed. Continue with partial results, or abort and save what we have?"

**Checkpoint**: Save intermediate report file paths to `checkpoints/phase5_intermediate.json`. Emit Phase Recap.

---

## Phase 6: Gap Analysis & Round 2 Planning (~3-10 minutes)

Spawn a single **`deep-researcher` agent** — with `model: "sonnet"` for Standard depth, `model: "opus"` for Deep/Exhaustive — to analyze all intermediate reports.

The agent's prompt MUST include all intermediate reports and these instructions:

"Analyze the intermediate research reports and identify:
1. COVERAGE: Which aspects are well-covered (3+ sources)? Which are thin (single source)?
2. CONTRADICTIONS: Where do findings conflict? List specific contradictions with sources.
3. CIRCULAR_SOURCING: Where does apparent consensus trace to a single original source?
4. MISSING: What important aspects were NOT covered?
5. CLAIMS_TO_CHALLENGE: Identify 3-5 most confident claims for the skeptic to pressure-test.

Return:
- 4-6 specific research targets for Round 2 collectors (question + why it matters)
- 3-5 specific claims for the skeptic (exact claim text + source)
- Overall confidence assessment

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly."

**Timeout**: If Opus doesn't return within phase timeout, skip Round 2 entirely. Proceed to Phase 8 synthesis with Round 1 data only. Note the limitation in the report.

**Checkpoint**: Save gap analysis and Round 2 targets to `checkpoints/phase6_gap_analysis.json`. Emit Phase Recap.

---

## Phase 7: Targeted Deep Dives — Round 2 (~10-40 minutes)

Based on the gap analysis, spawn two types of agents in parallel in a single message:

### Collector agents (Sonnet)

Spawn 3-10 **`deep-researcher` agents** with `model: "sonnet"` (count based on depth level). Each targets a specific gap from Phase 6. Their prompts MUST:
- Reference the specific gap and why it matters
- Include relevant context from Round 1 that should inform their search
- Include the list of Phase 4 source URLs already read — instruct: "Before WebFetching, check if the URL was already read in Round 1. If so, reference that analysis instead of re-fetching."
- Instruct: "Also look for evidence that CONTRADICTS prevailing Round 1 findings"
- Allow up to 2 WebFetch calls (reduced from 3 to save tokens on already-covered territory)
- Include the anti-recursion instruction
- Keep response under 800 words

### Skeptic agent(s) (Opus)

Spawn 1-2 **`deep-researcher` agents** with `model: "opus"` (2 for Exhaustive depth). Each receives specific claims from Phase 6 and this instruction:

"You are a skeptic. Your job is NOT to confirm — it is to challenge. For each claim:
1. Search for evidence that CONTRADICTS or NUANCES the claim
2. Look for criticisms, rebuttals, alternative explanations
3. Check if the claim's sources have been disputed
4. Check for circular sourcing: do multiple 'independent' sources trace to one original?
5. Consider whether the claim overgeneralizes

Every challenge MUST reference a specific source URL. Unsupported challenges will be discarded. Do not exceed 2 WebFetch calls. Keep response under 600 words.

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly."

**Timeout**: If Round 2 agents don't complete within phase timeout, proceed with available results. If Round 1 completed with 3+ intermediate reports, synthesis can proceed even if Round 2 fails entirely.

**Checkpoint**: Save collector + skeptic results to `checkpoints/phase7_round2.json`. Emit Phase Recap.

---

## Phase 8: Final Synthesis (~5-15 minutes)

Spawn a single **`deep-researcher` agent** with `model: "opus"` to produce the final synthesis.

The agent receives: ALL intermediate reports from tree reduction, gap analysis, ALL Round 2 findings, skeptic results, and BOOTSTRAP_CONTEXT.

"Synthesize all research into a final report. Perform:
1. CROSS-VALIDATION: For each finding, count independent sources. Note agreements and conflicts.
2. PER-FINDING CONFIDENCE: HIGH (3+ independent sources, no counter-evidence), MEDIUM (2 sources or counter-evidence exists), LOW (single source — flag it).
3. CONTRADICTION RESOLUTION: Present both sides with evidence strength. Check for circular sourcing.
4. SKEPTIC INTEGRATION: Which claims survived? Which were nuanced? Which were contradicted?
5. BOOTSTRAP INTEGRATION: How do findings build on/revise the initial deep-research?

Format each finding as: `N. **[Claim]** \`[Confidence: HIGH/MEDIUM/LOW]\` \`[Sources: N]\` — [Evidence sentence] [URL1](link) [URL2](link)`
Format each contradiction as a row: `[Claim] | [Position A + source URL] | [Position B + source URL] | [Evidence strength] | [Circular: Yes/No] | [Resolution]`

Return: 20-40 key findings in the format above, contradiction table, knowledge gaps, and confidence assessment.

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly."

**Synthesis validation**: If Opus returns fewer than 3 key findings or an empty/malformed response, fall back to using the highest-level intermediate reports from Phase 5 as the basis for the report. Log: "Opus synthesis produced insufficient output; using tree-merged results instead."

**Timeout**: If Opus synthesis fails, the orchestrator produces a simpler report by concatenating intermediate reports with a brief executive summary.

---

## Phase 9: Report Generation & Self-Check (~5-15 minutes)

### 9a: Generate report

Using the Opus synthesis output, generate the full report following [references/report-template.md](references/report-template.md).

### 9b: Self-check audit

Before saving, verify:
1. **Citation audit**: Does every finding have a URL from a research agent? Remove any that don't.
2. **Citation-claim match**: For critical findings, verify the claim appeared in agent results. Flag mismatches.
3. **Single-source flag**: Is any HIGH-confidence claim backed by only 1 source? Downgrade to MEDIUM.
4. **Circular sourcing check**: Any "consensus" tracing to one original? Note it.
5. **LOW-credibility check**: Any claim supported only by LOW-credibility sources? Mark "unverified."
6. **Contradiction completeness**: Are all contradictions noted?
7. **Human verification flag**: Findings requiring expert review? Flag explicitly.

### 9c: Save report

Write 3 files to the confirmed save location from Phase 1:
1. `report.md` — The full research report
2. `sources.md` — Complete source list with quality scores and metadata
3. `methodology.md` — Detailed methodology (agent counts, timing, tree structure, failures)

If pipeline failed partway, save partial report with `[PARTIAL]` in the title.

### 9d: Present summary

Display in chat:
- Report file path
- Key statistics (sources screened/read, agents, time, depth)
- Top 3-5 findings with confidence levels
- Any limitations or failures that occurred

---

## Rules

1. **NEVER generate citation URLs from memory** — only use URLs that research agents explicitly returned. Citation failure rates exceed 60% in AI systems.
2. **All agents MUST be `deep-researcher` subagent type** — this structurally prevents sub-agent spawning and skill invocation. No exceptions.
3. **Every agent prompt MUST include the anti-recursion instruction** verbatim from [references/tree-reduction.md](references/tree-reduction.md). This is Layer 2 defense-in-depth.
4. **No agent receives information about other agents or the tree structure** — agents are isolated leaf nodes that think they're doing standalone tasks (Layer 3: information isolation).
5. **Tree depth hard cap: 3 levels** — even if group math suggests more, stop at 3. Pass remaining reports directly to Opus synthesis.
6. **Skip-and-note over retry storms** — max 1 retry per agent, only on timeout (never on bad output). If an agent returns bad output, skip it and note the coverage gap. Retrying bad output risks cost explosions (documented: $10+/day from naive retries on large contexts). Never retry entire batches.
7. **Phase timeouts are hard** — if an agent hasn't returned by phase timeout, skip it and proceed. No agent is waited on indefinitely. Overall hard caps: Standard=75min, Deep=150min, Exhaustive=270min.
8. **Use tiered models per depth level**: Haiku for screening and validation gates (Sonnet validation for Exhaustive only). Sonnet for data collection, merging, query generation, and gap analysis at Standard depth. Opus for gap analysis (Deep/Exhaustive), skeptic, and final synthesis. See [references/depth-config.md](references/depth-config.md) for the full per-phase model table. Never use Haiku for synthesis or Opus for search.
9. **Validation gates are structural-only** — check: citation URLs present? metadata block complete? word count in range? sections parseable? Do NOT auto-reject based on semantic quality judgments (only ~53% accurate). Flag suspicious outputs for downstream awareness, don't kill them.
10. **Confidence is source-agreement-based, not self-reported** — LLMs have <30% calibration accuracy. Count independent sources per claim: 3+ = HIGH, 2 = MEDIUM, 1 = LOW.
11. **Deduplication is soft-merge** — flag duplicates and merge unique claims, don't hard-delete. Over-deduplication reduces source diversity.
12. **Always save the report** — even if the pipeline fails partway, save a partial report with whatever data was collected. Never lose completed work.
13. **Checkpoint after every phase** — save a JSON checkpoint file per [references/checkpointing.md](references/checkpointing.md). Each agent's output file is an implicit sub-phase checkpoint. On failure, only re-run agents whose output files are missing.
14. **Emit Phase Recap after every phase** — display phase name, agent counts, source counts, elapsed time, issues, and next phase per the template in [references/checkpointing.md](references/checkpointing.md). Users need visibility during 1-4 hour runs.
15. **Pause on high failure rates** — if >30% of agents in any phase fail, or <20% of sources pass screening, pause and ask the user before continuing. Do not silently degrade on catastrophic failures.
