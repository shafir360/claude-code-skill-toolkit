---
name: deep-research
description: 'Conducts exhaustive, multi-layered research using two rounds of parallel investigation with tiered model strategy. Round 1 spawns broad-sweep Sonnet agents across 4-6 themes. An Opus gap-analysis identifies weak spots, then Round 2 launches targeted collectors plus a dedicated Opus skeptic agent that challenges majority findings. Includes post-synthesis refinement and citation verification. Produces comprehensive cited reports with per-finding confidence levels, contradiction analysis, and source credibility assessment. Use when the user says "deep research", "exhaustive research", "thorough investigation", "deep dive into", "comprehensive analysis", or needs research that goes beyond a quick overview.'
argument-hint: <topic or question>
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Deep Research: $ARGUMENTS

You are conducting an exhaustive, multi-layered research investigation. This skill uses a **tiered model strategy**: Sonnet agents for fast parallel data collection, and Opus agents for high-quality analysis, synthesis, and adversarial review.

**Target: complete the entire pipeline in 10-12 minutes.**

**Time budget**: Phase 1 ~1min | Phase 2 ~3min | Phase 3 ~1min | Phase 4 ~3min | Phase 5 ~2min | Phase 5b ~1min | Phase 6-7 ~1.5min

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).
Use the report structure from [references/report-template.md](references/report-template.md).

---

## Phase 1: Scope & Plan (~1 minute)

Analyze the research topic and decompose it into **4-6 distinct research themes**. Prefer fewer, deeper themes over more shallow ones. Each theme should cover a non-overlapping aspect of the topic.

For each theme, define:
- A clear research question (1 sentence)
- 2-3 sub-questions to guide the agent
- A research lens (technical, skeptic/critic, industry/commercial, academic, historical, future outlook, user/practitioner)

Present the research plan to the user:

```
## Research Plan: [Topic]

I'll investigate this topic across [N] themes in two rounds:

### Round 1: Broad Sweep
1. **[Theme]** — [research question] (lens: [lens])
2. **[Theme]** — [research question] (lens: [lens])
...

### Round 2: Targeted Deep Dives
Will be determined after Round 1 gap analysis — targeting weak spots, contradictions, and under-explored areas.

Proceed with this plan? (or suggest changes)
```

If the user provides modifications, adjust the plan. If they confirm or don't respond within a reasonable time, proceed immediately.

## Phase 2: Broad Sweep — Round 1 (~3 minutes)

Spawn one **deep-researcher** agent for EACH theme. Launch ALL agents in parallel in a single message.

**Critical rules for EVERY Round 1 agent:**
- Set `model: "sonnet"` on every agent (Sonnet handles search/fetch efficiently)
- Each agent gets a unique theme and lens — NO overlap between agents
- Each agent's prompt MUST include this instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Structure your response using these exact sections:

FINDINGS:
- [3-5 bullet points, one sentence each with an inline citation URL]

SOURCES:
- [Top 5 source URLs, each with a credibility rating: HIGH/MEDIUM/LOW]

SURPRISES:
- [Any contradictions, under-sourced claims, or unexpected discoveries — or 'None']

Do NOT include source tables, contradiction tables, or lengthy analysis paragraphs. Keep each section concise. IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Each agent's prompt must also include:
- The overall research topic
- Its specific assigned theme, lens, and 2-3 sub-questions
- Instruction to note any surprising contradictions or claims that seem under-sourced

Wait for all agents to return before proceeding.

**If an agent fails or returns empty**: Skip it. If fewer than 3 agents return usable results, note the coverage gap and consider launching 1-2 replacement agents with adjusted search terms before proceeding.

## Phase 3: Gap Analysis & Round 2 Planning (~1 minute)

This is a critical analytical phase. Use the **best available model** for this work.

Spawn a single **deep-researcher** agent with `model: "opus"` to perform gap analysis:

The agent's prompt MUST include:
- All findings from Round 1 (concatenated)
- These explicit instructions:

"You are analyzing Round 1 research findings to plan Round 2 targeted deep dives. Perform the following analysis:

1. **Coverage Assessment**: Which aspects of the topic are well-covered (3+ sources agree)? Which are thin (single source only)?

2. **Contradiction Detection**: Where do Round 1 findings conflict with each other? List specific contradictions with the agents/sources involved.

3. **Single-Source Claims**: Flag any finding backed by only one source — these need independent verification in Round 2.

4. **Missing Angles**: What important aspects of the topic were NOT covered by any Round 1 agent?

5. **Strongest Claims to Challenge**: Identify the 2-3 most confident/sweeping claims from Round 1 that the skeptic agent should specifically try to disprove or nuance.

Structure your response using these sections:

WELL_COVERED:
- [Aspects with 3+ agreeing sources]

THIN_COVERAGE:
- [Aspects with only 1 source — need Round 2 verification]

CONTRADICTIONS:
- [Specific conflicting findings with agents/sources involved]

ROUND_2_TARGETS:
- [3-5 specific research targets for collector agents, each with a clear question and why it matters]

SKEPTIC_CHALLENGES:
- [2-3 specific claims to challenge, with exact claim text and why it needs scrutiny]

CONFIDENCE:
- [Overall assessment of what we know well vs. poorly]

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

## Phase 4: Targeted Deep Dives — Round 2 (~3 minutes)

Based on the gap analysis, spawn two types of agents in parallel in a single message:

### Collector Agents (3-4 agents, `model: "sonnet"`)
Each targets a specific gap identified in Phase 3. Their prompts MUST:
- Reference the specific gap or question from the gap analysis
- Include any relevant context from Round 1 findings that should inform their search
- Follow citation chains: if Round 1 found a key source, the collector should search for papers/articles that cite or respond to it
- Include the same data-collection instruction as Round 1 agents (verbatim block above), BUT raise the WebFetch limit to 3 calls (Round 2 agents do targeted deep dives and may need more full-page reads)
- Include this additional instruction: "Also look for evidence that CONTRADICTS the prevailing findings from Round 1. Do not only seek confirming evidence."

### Skeptic Agent (1 **deep-researcher** agent, `model: "opus"`)
A dedicated adversarial agent that challenges the strongest Round 1 claims. Its prompt MUST include:
- The 2-3 specific claims identified for challenge in Phase 3
- This instruction verbatim:

"You are a skeptic and devil's advocate. Your job is NOT to confirm existing findings — it is to challenge them. For each claim you are given:

1. Search for evidence that CONTRADICTS or NUANCES the claim
2. Look for criticisms, rebuttals, or alternative explanations
3. Check if the claim's sources have been disputed or retracted
4. Consider whether the claim overgeneralizes or omits important caveats

Even if you cannot disprove a claim, identify its limitations and boundary conditions. A finding that 'X is always true' should be tested — is it true in all contexts, for all populations, in all time periods?

Challenge the majority position regardless of how confident it seems. Do not be swayed by the number of sources supporting a claim — look for quality counter-evidence. Every challenge MUST reference a specific source URL. Do not speculate without evidence — unsupported challenges will be discarded.

Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 600 words. Return: your challenges/counter-evidence for each claim (with citation URLs), and your top 5 source URLs with credibility ratings.

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Wait for all Round 2 agents to return before proceeding.

## Phase 5: Cross-Reference & Synthesize (~2 minutes)

This is the highest-quality analytical phase. Spawn a single **deep-researcher** agent with `model: "opus"` to perform final synthesis.

The agent's prompt MUST include:
- All Round 1 findings
- The gap analysis from Phase 3
- All Round 2 findings (collectors + skeptic)
- These explicit instructions:

"You are the final synthesizer for a deep research investigation. You have findings from two rounds of research plus a skeptic's challenges. Perform the following:

1. **Cross-Validation Matrix**: For each major finding, count how many independent sources support it. Cross-reference: does Agent A's finding agree or conflict with Agent B's?

2. **Per-Finding Confidence Assignment**:
   - **High**: 3+ independent sources from different agents agree, no credible counter-evidence
   - **Medium**: 2 independent sources agree, or 3+ agree but credible counter-evidence exists
   - **Low**: Single source only, OR multiple sources but skeptic found strong counter-evidence — MUST be flagged

3. **Contradiction Resolution**: For each contradiction found:
   - Compare source credibility (use HIGH/MEDIUM/LOW ratings)
   - Determine if both positions can be partially true (nuanced reconciliation)
   - If irreconcilable, present both positions with evidence strength

4. **Skeptic Integration**: How did the skeptic's challenges modify the findings?
   - Which claims survived scrutiny?
   - Which were nuanced or weakened?
   - Which were contradicted?

5. **Knowledge Gap Assessment**: What remains unknown after two rounds?

Return a structured synthesis document with:
- 12-20 key findings, each tagged [Confidence: HIGH/MEDIUM/LOW] with citation URLs
- Contradiction analysis (always present — state 'None found' if applicable)
- Knowledge gaps
- A complete source list with credibility ratings
- Areas where human expert verification is recommended

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

## Phase 5b: Refinement Pass (~1 minute)

After synthesis, perform a quick self-critique of the synthesis output:

1. Are there any HIGH-confidence findings backed by only 1 source? (Should be MEDIUM)
2. Are there unresolved contradictions that could be clarified with one more search?
3. Are there knowledge gaps where a targeted search could fill the hole?

If **2 or more issues** are found, spawn 1-2 targeted **deep-researcher** agents with `model: "sonnet"` to fill the specific gaps. Their prompts should reference the exact gap from the synthesis and include the same structured output format as Round 1. Cap at 1 refinement round — do NOT iterate further.

If the synthesis is clean (0-1 minor issues), skip directly to Phase 6.

Integrate any refinement findings into the synthesis before proceeding.

## Phase 6: Report Generation (~1 minute)

Using the synthesis from Phase 5, generate the full report following the template in [references/report-template.md](references/report-template.md).

**Report requirements:**
- Executive Summary: 2-3 paragraphs, lead with the answer, state overall confidence
- Key Findings: 12-20 numbered, each with `[Confidence: HIGH/MEDIUM/LOW]` and citation
- Deep Dive Sections: 2-3 thematic sections from Round 2 targeted research
- Contradictions & Debates: ALWAYS present, even if "No major contradictions found"
- Knowledge Gaps: What couldn't be determined and why
- Source Quality Assessment: Table with credibility tiers
- Methodology Note: Number of agents, rounds, total sources consulted, time taken

## Phase 7: Self-Check & Output (~30 seconds)

Quick quality review before presenting:

1. **Citation audit**: Does every finding have a citation URL that came from an agent? Remove any that don't. NEVER generate a URL from memory.
2. **Citation-claim match**: For each critical finding, verify the claim attributed to the citation actually appeared in the agent's search results. If a claim seems too specific or too perfectly aligned with the narrative, flag it as potentially mismatched and downgrade confidence.
3. **Single-source flag**: Is any HIGH-confidence claim backed by only one source? Downgrade to MEDIUM.
4. **LOW-credibility check**: Is any claim supported only by LOW-credibility sources? Mark as "unverified" or remove.
5. **Source diversity check**: Are findings over-reliant on a single source type (e.g., all blogs, all from one institution)? Note any diversity gaps.
6. **Contradiction completeness**: Are all contradictions between findings noted? Add any missed.
7. **Human verification flag**: Are there findings where human expert review is essential? Flag them explicitly.

Present the final report to the user.

Then ask: "Would you like me to save this report to a file, dive deeper into any specific finding, or investigate any of the knowledge gaps further?"

---

## Rules

1. **NEVER generate citation URLs from memory** — only use URLs that agents explicitly returned. This is the single most important rule. AI citation failure rates exceed 60%.
2. **Every Round 2 agent prompt MUST include instruction to seek contradictory evidence** — counters the "Chat-Chamber effect" where AI confirms assumptions rather than challenging them.
3. **The Opus skeptic agent MUST challenge the strongest Round 1 claims regardless of confidence** — counters "minority correction asymmetry" where confident-but-wrong agents sway groups.
4. **Each agent MUST have a distinct, non-overlapping research focus** — multi-agent systems exhibit 0.41-0.50 work redundancy without explicit differentiation.
5. **Round 2 agents MUST reference specific gaps from Phase 3** — prevents context drift and ensures progressive knowledge accumulation.
6. **Use tiered models**: `model: "sonnet"` for data-gathering agents, `model: "opus"` for gap analysis, synthesis, and skeptic agents. All agents MUST use the **deep-researcher** subagent type — never use general-purpose.
7. **Per-finding confidence**: High (3+ independent sources), Medium (2 sources or counter-evidence exists), Low (single source — MUST be flagged).
8. **If Round 1 returns fewer than 3 usable agent results**, skip Round 2 and note the limitation prominently in the report.
9. **Contradiction section is ALWAYS present** — even if stating "No major contradictions found across [N] sources."
10. **Flag when human expert verification is essential** — especially for claims about medical, legal, financial, or safety-critical topics.
11. **Skeptic challenges MUST cite sources** — unsupported speculation degrades quality. Discard any skeptic challenge without a citation URL.
12. **Post-synthesis refinement is capped at 1 round** — diminishing returns after 2 total refinement passes. Skip if synthesis has 0-1 minor issues.
