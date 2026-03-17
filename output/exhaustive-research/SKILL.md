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

## Context Management (Critical for Deep/Exhaustive Depth)

The orchestrator's context window fills rapidly during Exhaustive runs (~1,001K tokens without mitigation — overflows 1M context). To prevent overflow and "lost in the middle" quality degradation:

**1. Save-and-release pattern**: After each agent wave completes in Phases 2-7:
   - Save all agent responses to disk (mini-reports, intermediate reports, verdicts, etc.)
   - Keep only a **compact manifest entry** in context: `batch_N.md — [1-sentence summary of key findings]`
   - Do NOT hold full report text in context after saving to disk

**2. Load-on-demand pattern**: When a downstream phase needs prior reports:
   - Read reports from disk using the Read tool (not from context memory)
   - Only load the specific subset needed (e.g., Phase 5 merge agents need 5 mini-reports, not all 40)
   - After sending reports to an agent, release them from active consideration

**3. Synthesis receives summaries, not full reports**: Phase 8 Opus synthesis should receive:
   - The compact manifest (file paths + 1-line summaries for all reports)
   - Full text of ONLY the highest-level tree outputs (Level 2 condensed reports, or Level 1 if no Level 2)
   - Gap analysis output (full)
   - Round 2 collector + skeptic results (full)
   - NOT all 40 mini-reports, NOT all 8 intermediate reports

**4. Context budget targets** (see [references/depth-config.md](references/depth-config.md)):
   - Standard: stay under 300K tokens
   - Deep: stay under 500K tokens
   - Exhaustive: stay under 700K tokens (leaves 300K headroom in 1M context)

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

**Smart-skip**: If the user's initial prompt already specifies depth level, scope/focus, and target decision (e.g., "exhaustive research on X for Y purpose, focusing on Z"), skip clarification questions entirely and proceed to Phase 1d. Only ask questions for genuinely missing pieces. If bootstrap context is rich AND the original prompt specifies depth, skip Phase 1c.

Ask **2-4 targeted questions** based on the topic and any bootstrap context (only for missing information):
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

Spawn **1** Sonnet `deep-researcher` agent with `model: "sonnet"` for all depth levels. The single agent receives:
- ALL research plan themes
- BOOTSTRAP_CONTEXT (so it avoids already-searched areas)
- Instruction to generate diverse queries using academic, practitioner, contrarian, and historical perspectives
- Query count target: 15-25 (Standard), 40-60 (Deep), 80-120 (Exhaustive)
- The expanded anti-recursion instruction from [references/tree-reduction.md](references/tree-reduction.md)

The query-gen agent prompt MUST end with: "Return only a numbered list of search query strings. Do NOT run searches yourself. Do NOT use Agent, Skill, WebSearch, or WebFetch tools. Just produce the query list."

**Sub-timeout**: If the query-gen agent doesn't return within 5 minutes, proceed with whatever queries the orchestrator can generate from the research plan themes directly.

Collect all queries. Deduplicate (exact match + semantic similarity). Cap at depth-level maximum from [references/depth-config.md](references/depth-config.md).

### 2b: Execute searches

Run all search queries using WebSearch. Collect all result snippets (URL + title + snippet text). Deduplicate by URL (exact match). This produces the candidate pool for screening.

If the candidate pool is smaller than expected (< 50% of depth target), generate 10-20 additional queries with broader terms and search again. Do this at most once. Track this retry with a flag in the Phase 2 checkpoint: `"search_retry_executed": true`. On resume from Phase 2: check this flag before retrying — if already true, skip retry and proceed to Phase 3.

**Zero results abort**: If total search results < 10 across all queries (including retry), ABORT: "Search returned near-zero results. The topic may be too niche for web research. Suggest broadening the topic or trying a different angle."

**Checkpoint**: Save search results to `checkpoints/phase2_search_results.json`. Emit Phase Recap (see [references/checkpointing.md](references/checkpointing.md)).

**Context release (Deep/Exhaustive)**: After saving search results to disk, keep only the deduplicated candidate list in context (URL + title + composite score — ~1 line per source). Release full snippet text from active context. Phase 3 screeners will receive snippets by reading from `phase2_search_results.json`.

---

## Phase 3: Source Pre-Screening (~5-20 minutes)

Spawn **Haiku `deep-researcher` agents** with `model: "haiku"`, one per batch of ~40-50 snippets. Each agent uses the **condensed** screening rubric from [references/screening-rubric.md](references/screening-rubric.md) (the short version, not the full reference doc).

Each screener evaluates every snippet for relevance (1-10), credibility (HIGH/MEDIUM/LOW), and information density (HIGH/MEDIUM/LOW), returning a verdict: PASS, BORDERLINE, or FAIL.

**Wave-batching for Exhaustive depth**: At Exhaustive depth (8-12 screeners), launch agents in waves of 6. After each wave: collect all returned results, note any non-returning agents as timed-out (coverage gap), then start the next wave. For Standard and Deep depths (≤6 agents), launch all at once.

**After all screeners (or waves) return:**
1. Collect all PASS sources. Sort by composite score (relevance x credibility_weight x density_weight)
2. Take top N sources where N = depth-level target from [references/depth-config.md](references/depth-config.md)
3. If PASS count < target: promote BORDERLINE sources by composite score
4. Exclude any URLs already in BOOTSTRAP_CONTEXT (already read in Round 0)
5. Log all screened sources with verdicts for the methodology section

**Timeout**: If screener agents don't return within phase timeout, proceed with whatever results are available. If fewer than 3 screeners returned, fall back to search-engine ranking (top N by position).

**Early termination checks**:
- If 0 sources pass screening: ABORT immediately. "No sources passed quality screening. The topic may be too niche or queries poorly targeted."
- If <5 sources pass: offer (a) abbreviated single-round synthesis (skip tree reduction), (b) generate 20 additional broader queries and re-search ONCE (this counts as the Phase 2b retry — no further retries allowed even if results are still sparse), (c) abort.
- If <20% of candidates passed: pause and ask: "Only [N]% passed screening — queries may be poorly targeted. Continue with reduced depth, refine topic, or abort?"

**Checkpoint**: Save screening verdicts to `checkpoints/phase3_screening_verdicts.json`. Emit Phase Recap.

**Context release (Deep/Exhaustive)**: After saving verdicts, keep only the PASS source list in context (URLs + composite scores). Release BORDERLINE and FAIL verdict details from active context.

**Early-start optimization (Deep/Exhaustive only)**: Phase 4 readers may begin spawning as soon as the first screening wave returns at least 5 PASS sources. Do not wait for all screeners to complete before starting the first reader wave. Track which sources have been assigned to readers to avoid double-reading. Continue screening remaining waves concurrently with reader waves.

---

## Phase 4: Deep Reading — Round 1 (~10-40 minutes)

### 4a: Assign sources to reader agents

Divide PASS sources into batches of 5-7. Each batch will be assigned to one Sonnet reader agent using the Level 0 reader prompt from [references/tree-reduction.md](references/tree-reduction.md).

Each reader:
- WebFetches up to 2 sources — prioritize the 2 highest composite scores from pre-screening (uses search snippets for the remaining 3-5). If WebFetch fails, continue with snippet only.
- Extracts key claims, data, statistics with citation URLs
- Notes contradictions within its batch
- Produces a structured mini-report (max 800 words)
- Saves mini-report to `{save_dir}/mini-reports/batch_{N}.md`

**Wave-batching (required for Exhaustive depth; optional for Deep; not needed for Standard):**

For Exhaustive depth (25-50 reader agents), launch readers in **waves of 10**:

```
For each wave of up to 10 agents:
  1. Spawn all agents in the wave in a single parallel message
  2. Collect results as they return
  3. Once all other agents in the wave have returned, the wave is effectively complete.
     Any agent that has not returned by then is considered TIMED-OUT — do not wait further.
     (The non-returning agent had the entire duration of all other agents' processing to respond.)
  4. Mark timed-out agents as TIMED-OUT, note coverage gap, do NOT retry now
  5. Write mini-reports to disk for all completed agents in this wave
  6. **Context release**: After writing mini-reports to disk, release full report text from active context.
     Keep only a manifest line per report: `batch_{N}.md — [1-line summary: top claim + source count]`
     Do NOT reference the full mini-report text again until Phase 5 reads it from disk.
  7. Emit a wave-level progress note: "Wave [N]/[total] complete: [X]/[10] agents returned"
  8. Start next wave immediately — do not wait for timed-out agents
```

For Standard depth (≤8 agents) and Deep depth (≤20 agents): launch all agents at once in a single message (no wave overhead needed).

### 4b: Validation gate

**At Standard depth, validation gates are OPTIONAL** — the orchestrator may skip Phase 4b entirely to save cost, since downstream merge agents will catch structural issues during cross-referencing. At Deep/Exhaustive depth, validation gates remain active.

After all readers return, divide mini-reports into batches of 5. Spawn **1 Haiku `deep-researcher` validator per batch** with `model: "haiku"` (Sonnet for Exhaustive depth) to validate using the validation gate prompt from [references/tree-reduction.md](references/tree-reduction.md). Validators check STRUCTURAL properties only: citation URLs present? metadata block complete? word count in expected range (200-800)? response parseable into expected sections?

Reports marked REJECT are discarded. Reports marked FLAG are kept with warnings attached. Do NOT auto-reject based on semantic quality judgments — structural checks only, since automated semantic quality detection is only ~53% accurate and false positives can cascade.

**Validator sub-timeout**: 5 min (Standard), 8 min (Deep), 12 min (Exhaustive). If validators don't return by sub-timeout, skip validation and mark all reports UNVALIDATED. Proceed to Phase 5.

**Timeout**: With wave-batching, timed-out agents are handled wave by wave (see above) — never wait indefinitely. After all waves complete, if fewer than 50% of all reader agents returned, note the coverage gap. **If 0 readers return across all waves (100% failure)**: save partial report from prior phases, notify user: "Phase 4 complete failure — all reader agents failed. Saving partial report." Do not continue.

Do NOT retry entire batches — each agent's output file is an implicit checkpoint; only agents with missing output files need re-running, and only once.

**Checkpoint**: Save mini-report file paths to `checkpoints/phase4_mini_reports.json`. Emit Phase Recap with Agent Recap showing per-batch outcomes.

**Early-start optimization (Exhaustive only)**: Phase 5 Level 1 merge agents may begin spawning as soon as 5 mini-reports are available from completed reader waves. Do not wait for all readers to complete. As more mini-reports complete, spawn additional merge agents. Track which mini-reports have been assigned to merge agents to avoid double-processing. Continue reader waves concurrently with merge waves.

---

## Phase 5: Tree Reduction (~5-20 minutes)

### 5a: Level 1 merge

Group mini-reports into batches of 5. For each batch:
1. **Read the 5 mini-reports from disk** using Read tool: `{save_dir}/mini-reports/batch_{N}.md` through `batch_{N+4}.md`
2. Send them to a Sonnet merge agent using the Level 1 merge prompt from [references/tree-reduction.md](references/tree-reduction.md)
3. Receive the intermediate report response
4. Save intermediate report to disk: `{save_dir}/intermediate/group_{N}.md`
5. **Context release**: Release mini-report text and intermediate report text from active context. Keep only manifest: `group_{N}.md — [1-line summary]`

Each merger:
- Deduplicates claims across mini-reports
- Cross-references for convergent findings and contradictions
- Checks for circular sourcing (multiple reports citing the same original)
- Produces an intermediate report (max 1500 words)

**Wave-batching for Exhaustive depth**: At Exhaustive depth (6-10 merge agents), launch in waves of 5. After each wave: collect results, mark non-returning agents as timed-out, write `intermediate/group_{N}.md` for completed agents, start next wave. For Standard and Deep depths (≤5 agents), launch all at once.

### 5b: Validation gate (Deep/Exhaustive only)

Divide intermediate reports into batches of 5. Spawn 1 Haiku `deep-researcher` validator per batch with `model: "haiku"` (Sonnet for Exhaustive) to check intermediate reports. Sub-timeout: 5 min (Standard), 8 min (Deep), 12 min (Exhaustive). If exceeded, skip validation and proceed.

### 5c: Level 2 merge (Exhaustive only)

If more than 5 intermediate reports remain, repeat: group into batches of 5, spawn **Sonnet `deep-researcher` merge agents** with `model: "sonnet"`, produce condensed reports.

**Hard cap: Tree depth NEVER exceeds 3 levels.** If more than 5 reports remain after Level 2, pass them all directly to the Opus root synthesis in Phase 8.

### 5d: Timeout handling

If any merge agent doesn't return within phase timeout, skip it. If fewer than 50% of merge agents return, the parent concatenates available mini-reports inline as a fallback (lower quality but functional). **If 0 merge agents return (100% failure)**: save partial report from Phase 4 data, notify user. Do not continue.

**High failure check**: If >30% of agents in Phase 5 fail, pause and ask: "Over 30% of merge agents failed. Continue with partial results, or abort and save what we have?"

**Checkpoint**: Save intermediate report file paths to `checkpoints/phase5_intermediate.json`. Emit Phase Recap.

---

## Phase 6: Gap Analysis & Round 2 Planning (~3-10 minutes)

**Budget check**: Before Phase 6, estimate total tokens consumed so far (from checkpoint agent_stats). If consumed > 60% of depth-level token budget (Standard=750K, Deep=2.25M, Exhaustive=6M), warn user: "Token consumption is tracking high ([X]% of budget used before Round 2). Options: (a) Continue — may exceed budget, (b) Skip Round 2 and synthesize now with Round 1 data, (c) Abort." This is a pause, not a hard stop.

Spawn a single **`deep-researcher` agent** with `model: "sonnet"` for all depth levels — to analyze all intermediate reports. (Gap analysis identifies gaps and claims for Round 2; it does not require Opus-level reasoning.)

**Context-aware loading (Deep/Exhaustive)**: Do NOT pass all intermediate reports from context memory. Instead:
- Read only the **highest-level tree outputs** from disk (Level 2 condensed reports if available, otherwise Level 1 intermediate reports)
- Include the compact manifest of ALL reports (file paths + 1-line summaries) so the agent has visibility into the full scope
- This keeps Phase 6 input to ~6-18K tokens instead of ~30K+

The agent's prompt MUST include the reports read from disk and these instructions:

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

IMPORTANT: You are analyzing reports already collected. Do NOT use WebSearch, WebFetch, Agent, or Skill tools. Your gap analysis is based solely on the reports provided here. Note gaps in your output — the orchestrator (not you) will dispatch Round 2 agents to fill them.

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool or Skill tool under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- Do NOT use WebSearch or WebFetch under any circumstances.
- If you identify a gap or missing piece, note it in your output — do NOT attempt to fill it yourself.
- Return your findings directly as text. This is the ONLY action you should take."

**Timeout**: If Opus doesn't return within phase timeout, skip Round 2 entirely. Proceed to Phase 8 synthesis with Round 1 data only. Note the limitation in the report.

**Checkpoint**: Save gap analysis and Round 2 targets to `checkpoints/phase6_gap_analysis.json`. Emit Phase Recap.

---

## Phase 7: Targeted Deep Dives — Round 2 (~10-40 minutes)

Based on the gap analysis, spawn two types of agents concurrently. Spawn collector waves AND skeptic agents in **separate messages** (never mix Opus skeptics with Sonnet collectors in the same spawn message). Skeptics receive Phase 6 claims (not collector output), so they run independently and in parallel with collectors. If a skeptic hangs, it does not block collectors, and vice versa.

### Collector agents (Sonnet)

Spawn 3-10 **`deep-researcher` agents** with `model: "sonnet"` (count based on depth level). At Exhaustive depth (8-10 collectors), use **waves of 5**: spawn 5, collect results (marking any non-returning agents as timed-out), then spawn the next 5. For Standard/Deep (≤6 collectors), launch all at once.

Each collector agent prompt MUST follow this template:

"Topic: [TOPIC-SLUG]. You are filling a specific research gap identified in Round 1.

GAP: [specific gap from Phase 6]
WHY IT MATTERS: [reason from Phase 6]
CONTEXT FROM ROUND 1: [relevant findings that should inform your search]
ALREADY-READ URLs (do NOT re-fetch these): [list of Phase 4 source URLs]

Instructions:
1. WebFetch up to 2 new sources that address this gap. Prioritize sources NOT in the already-read list.
2. Also look for evidence that CONTRADICTS prevailing Round 1 findings.
3. Extract key claims, data points, and statistics with citation URLs.

Keep response under 800 words.

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool or Skill tool under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- You MAY use WebFetch for up to 2 calls. Do NOT use WebSearch.
- If you identify further gaps, note them in your output — do NOT attempt to research further.
- Return your findings directly as text. This is the ONLY action you should take."

### Skeptic agent(s) (Opus) — spawn concurrently with collectors

Spawn 1-2 **`deep-researcher` agents** with `model: "opus"` (2 for Exhaustive depth) in a separate message from collectors. If Opus skeptic agents don't return by the time all collector waves have completed and been processed: skip skeptics, note limitation ("Skeptic review skipped — agent did not return"), and proceed to Phase 8. Do NOT wait indefinitely for Opus.

Each skeptic receives specific claims from Phase 6 and this instruction:

"You are a skeptic. Your job is NOT to confirm — it is to challenge. For each claim:
1. Search for evidence that CONTRADICTS or NUANCES the claim
2. Look for criticisms, rebuttals, alternative explanations
3. Check if the claim's sources have been disputed
4. Check for circular sourcing: do multiple 'independent' sources trace to one original?
5. Consider whether the claim overgeneralizes

Every challenge MUST reference a specific source URL. Unsupported challenges will be discarded. Keep response under 600 words.

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool or Skill tool under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- You MAY use WebFetch for up to 2 calls to find counter-evidence. Do NOT use WebSearch.
- If you identify additional gaps, note them in your output — do NOT attempt to research further.
- Return your findings directly as text. This is the ONLY action you should take."

**Timeout**: If Round 2 agents don't complete within phase timeout, proceed with available results. If Round 1 completed with 3+ intermediate reports, synthesis can proceed even if Round 2 fails entirely.

**Checkpoint**: Save collector + skeptic results to `checkpoints/phase7_round2.json`. Emit Phase Recap.

---

## Phase 8: Final Synthesis (~5-15 minutes)

Spawn a single **`deep-researcher` agent** with `model: "opus"` to produce the final synthesis.

**Context-aware loading**: The agent receives (read from disk, NOT from orchestrator context memory):
- **Compact manifest** of ALL mini-reports and intermediate reports (file paths + 1-line summaries — gives visibility into full scope)
- **Full text of ONLY the highest-level tree outputs** (Level 2 condensed reports if available, otherwise Level 1 intermediate reports — read from disk)
- **Gap analysis output** (full — read from `checkpoints/phase6_gap_analysis.json`)
- **Round 2 collector results** (full — read from `{save_dir}/round2/collector_{N}.md`)
- **Skeptic results** (full — read from `{save_dir}/round2/skeptic.md`)
- **BOOTSTRAP_CONTEXT** (if available)

This keeps Phase 8 input to ~40-60K tokens instead of ~200K+.

"Synthesize all research into a final report. Perform:
1. CROSS-VALIDATION: For each finding, count independent sources. Note agreements and conflicts.
2. PER-FINDING CONFIDENCE: HIGH (3+ independent sources, no counter-evidence), MEDIUM (2 sources or counter-evidence exists), LOW (single source — flag it).
3. CONTRADICTION RESOLUTION: Present both sides with evidence strength. Check for circular sourcing.
4. SKEPTIC INTEGRATION: Which claims survived? Which were nuanced? Which were contradicted?
5. BOOTSTRAP INTEGRATION: How do findings build on/revise the initial deep-research?

Format each finding as: `N. **[Claim]** \`[Confidence: HIGH/MEDIUM/LOW]\` \`[Sources: N]\` — [Evidence sentence] [URL1](link) [URL2](link)`
Format each contradiction as a row: `[Claim] | [Position A + source URL] | [Position B + source URL] | [Evidence strength] | [Circular: Yes/No] | [Resolution]`

Return: 20-40 key findings in the format above, contradiction table, knowledge gaps, and confidence assessment.

IMPORTANT: Synthesize only from the data provided here. Do NOT use WebSearch, WebFetch, Agent, or Skill tools. If you identify knowledge gaps, list them in your output — the orchestrator will handle follow-up. Do NOT attempt to fill gaps by fetching or researching further.

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool or Skill tool under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- Do NOT use WebSearch or WebFetch under any circumstances.
- Return your synthesis directly as text. This is the ONLY action you should take."

**Synthesis validation**: If Opus returns fewer than 3 key findings or an empty/malformed response, fall back to using the highest-level intermediate reports from Phase 5 as the basis for the report. Log: "Opus synthesis produced insufficient output; using tree-merged results instead."

**Timeout / no-return fallback**: If Opus synthesis does not return (rate limit, context overflow, or other failure), do NOT wait indefinitely. Instead:
1. Take the top 5 intermediate reports from Phase 5 tree reduction
2. Write a brief orchestrator-authored executive summary (3-5 paragraphs) covering the main convergent findings, contradictions, and knowledge gaps visible in those reports
3. Mark the report title as `[PARTIAL — Opus synthesis did not complete]`
4. Proceed to Phase 9 with this fallback synthesis

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
8. **Use tiered models per depth level**: Haiku for screening and validation gates (Sonnet validation for Exhaustive only). Sonnet for data collection, merging, query generation, and gap analysis (all depths). Opus for skeptic and final synthesis only. See [references/depth-config.md](references/depth-config.md) for the full per-phase model table. Never use Haiku for synthesis or Opus for search.
9. **Validation gates are structural-only** — check: citation URLs present? metadata block complete? word count in range? sections parseable? Do NOT auto-reject based on semantic quality judgments (only ~53% accurate). Flag suspicious outputs for downstream awareness, don't kill them.
10. **Confidence is source-agreement-based, not self-reported** — LLMs have <30% calibration accuracy. Count independent sources per claim: 3+ = HIGH, 2 = MEDIUM, 1 = LOW.
11. **Deduplication is soft-merge** — flag duplicates and merge unique claims, don't hard-delete. Over-deduplication reduces source diversity.
12. **Always save the report** — even if the pipeline fails partway, save a partial report with whatever data was collected. Never lose completed work.
13. **Checkpoint after every phase** — save a JSON checkpoint file per [references/checkpointing.md](references/checkpointing.md). Each agent's output file is an implicit sub-phase checkpoint. On failure, only re-run agents whose output files are missing.
14. **Emit Phase Recap after every phase** — display phase name, agent counts, source counts, elapsed time, issues, and next phase per the template in [references/checkpointing.md](references/checkpointing.md). Users need visibility during 1-4 hour runs.
15. **Pause on high failure rates** — if >30% of agents in any phase fail, or <20% of sources pass screening, pause and ask the user before continuing. Do not silently degrade on catastrophic failures.
16. **Never wait indefinitely for a single non-returning agent** — when spawning agents in parallel waves, once all other agents in the wave have returned, the wave is complete. Any agent that has not returned by then is TIMED-OUT (it had the entire duration of all other agents' processing to respond). Write outputs for completed agents, note skipped agents as coverage gaps, and proceed immediately. Apply to ALL parallel-spawn phases (2, 3, 4, 5, 7). Never hold an entire wave hostage to one non-responding agent.
17. **Every agent prompt MUST explicitly forbid WebSearch and WebFetch UNLESS those tools are part of the agent's defined task.** Only reader agents (Phase 4) and collector/skeptic agents (Phase 7) are permitted to use WebFetch (max 2 calls each). All other agents — query-gen (Phase 2), screeners (Phase 3), merge agents (Phase 5), validators (Phase 4b/5b), gap analysis (Phase 6), synthesis (Phase 8) — MUST include "Do NOT use WebSearch or WebFetch" in their prompts. If an agent cannot verify a claim, it notes uncertainty in its output — it does not fetch.
18. **Phase 0 (Bootstrap) MUST NOT invoke any tools** — it only parses text the user pasted into their initial prompt, or reads a file path the user specified. Do NOT invoke Agent, Skill, WebSearch, or WebFetch during bootstrap ingestion. If the user wants to pass /deep-research output, they must paste it or provide a file path.
19. **Phase 7 is a single pass** — collector and skeptic results do NOT trigger additional rounds of data collection. Any new gaps or contradictions identified by skeptics are documented in the report as limitations, not fed back into a new collector round. There is no Phase 7b.
20. **Context-aware streaming (Deep/Exhaustive)** — the orchestrator MUST NOT hold all agent responses in context simultaneously. After each wave of agents completes and responses are saved to disk, release full report text from active context and keep only a compact manifest (file path + 1-line summary). When downstream phases need prior reports, read them from disk using the Read tool. Phase 8 synthesis receives only the highest-level tree outputs (not all mini-reports), plus the manifest, gap analysis, and Round 2 results. This prevents context overflow (~1,001K without mitigation) and "lost in the middle" quality degradation. See the Context Management section for full details.
