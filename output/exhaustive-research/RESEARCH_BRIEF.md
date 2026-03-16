# Enhanced Design Brief: exhaustive-research Skill

## Executive Summary

This brief synthesizes 30+ findings from two research rounds plus skeptic challenges into actionable architecture decisions for a Claude Code skill implementing massively-scaled multi-agent research with hierarchical tree-reduction, 3-tier model routing, and configurable depth levels.

---

## 1. Prior Art

### What exists and what we can learn

**OpenAI Deep Research** uses o3 with multi-hop decomposition but has weak confidence calibration and struggles distinguishing authoritative sources from rumor. It represents the "monolithic large model" approach. [Source](https://openai.com/index/introducing-deep-research/)

**Gemini Deep Research** uses MoE architecture with Google Search in a "set-and-synthesize" pattern; **Perplexity** uses a hybrid retrieval-first loop. Both are closed-system, tightly integrated with proprietary search infrastructure. [Source](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)

**Anthropic's own multi-agent research system** uses Opus as orchestrator with Sonnet workers, reporting 90.2% improvement over single-agent on internal benchmarks. However, they discovered critical failure modes: spawning 50+ subagents for simple queries, duplicate work across agents, and context window overflow. Their key lesson was explicit task boundaries with breadth-first-then-narrow progression. [Source](https://www.anthropic.com/engineering/multi-agent-research-system)

**STORM (Stanford)** uses persona-based diverse query generation drawn from analogous Wikipedia articles, with LLM-based routing and vector similarity for soft-merge deduplication rather than hash-based dedup. Multi-perspective personas reduce overlap at the query-generation level. [Source](https://arxiv.org/abs/2402.14207)

**Cross-validation note**: The 90.2% improvement claim (Anthropic) is challenged by MAST-Data showing 41-86.7% failure rates across 7 multi-agent frameworks, and SWE-bench-Verified potentially overestimating by up to 100% due to insufficient test cases. The improvement likely applies to well-structured tasks with explicit coordination, not to general deployment.

### Design implication
Do not assume multi-agent automatically outperforms single-agent. The skill must include a complexity classifier that routes simple queries to single-agent mode and only escalates to multi-agent for genuinely complex research topics.

---

## 2. Domain Patterns

### 2.1 Hierarchical Tree-Reduction

**Finding [MEDIUM confidence]**: Hierarchical merging produces fewer omissions than flat summarization but introduces more inconsistency errors (BooookScore, ICLR 2024). Each level retains approximately 50-80% of information, meaning a 3-level tree retains 12.5-51.2% of original detail. [Sources](https://arxiv.org/abs/2310.00785)

**Finding [HIGH confidence]**: NexusSum (ACL 2025) demonstrates that specializing agent roles per tree level and using explicit compression control per level yields 30% BERTScore improvement over flat approaches. This is corroborated by Google Cloud's finding that injecting source snippets back into intermediate summaries reduces hallucination. [Sources](https://arxiv.org/abs/2505.24575), [Source 2](https://cloud.google.com/blog/products/ai-machine-learning/long-document-summarization-with-workflows-and-gemini-models)

**Finding [MEDIUM confidence]**: Chain of Agents (NeurIPS 2024) shows that parallel tree without lateral context underperforms sequential processing. Pure tree-parallelism loses cross-branch context. [Source](https://proceedings.neurips.cc/paper_files/paper/2024/file/ee71a4b14ec26710b39ee6be113d7750-Paper-Conference.pdf)

**Finding [LOW confidence]**: The "50-80% retention per level" figure comes from a single medium-credibility source. No peer-reviewed paper quantifies this precisely. The actual retention depends heavily on compression ratio, domain, and model capability.

**Optimal group size**: LangChain defaults to ~3000 tokens/bucket for map-reduce. Broader literature suggests 800-2048 tokens per chunk for summarization tasks with 10-30% overlap. No canonical "optimal group size" has been established in peer-reviewed work.

### Design implication
- Use 2-level tree maximum for standard depth, 3-level for deep/exhaustive
- Inject key source snippets (not just summaries) upward through tree levels
- Pass lateral context between sibling branches before merging (sequential-aware tree)
- Target 5-8 sources per leaf group, ~2000-3000 tokens of source material per group
- Each merge level should have explicit compression targets (e.g., Level 1: 60% retention, Level 2: 40% retention)

### 2.2 Source Pre-Screening & Relevance Scoring

**Finding [HIGH confidence]**: LLMs achieve 0.94-0.95 sensitivity/specificity for title+abstract screening (multiple independent studies: Rayyan, JMIR, Claude 3.5 Sonnet benchmarks). However, the "0% false-negative" claim from JMIR is contested by SIGIR research showing LLM judgments create a ceiling on measurable system performance. [Sources](https://pmc.ncbi.nlm.nih.gov/articles/PMC12657656/), [Source 2](https://www.jmir.org/2025/1/e67488), [Counter](https://pmc.ncbi.nlm.nih.gov/articles/PMC11984504/)

**Finding [HIGH confidence]**: JudgeRank's 3-step decomposed scoring (query analysis, document analysis, relevance judgment) outperforms flat single-prompt scoring. Microsoft confirms TREC-quality but notes false positives from lexical overlap. [Sources](https://arxiv.org/html/2412.05579v2), [Source 2](https://www.microsoft.com/en-us/research/wp-content/uploads/2023/09/LLMs_for_relevance_labelling__SIGIR_24_-2.pdf)

### Design implication
- Use Haiku-tier for initial relevance screening (title + snippet + URL)
- Implement 3-step decomposed scoring (JudgeRank pattern), not single-prompt
- Never assume 0% false-negative; include a "borderline" category that gets human review or Sonnet-tier re-evaluation
- Accept ~5% false positive rate as cost of high recall

### 2.3 Model Tiering & Budget Routing

**Finding [HIGH confidence]**: Difficulty-aware routing saves 36% cost with 11.21% accuracy improvement (multiple sources confirm). RouteLLM achieves 85% cost reduction while maintaining 95% of top-model performance. Trained routers generalize to unseen LLMs. [Sources](https://arxiv.org/html/2509.11079v1), [Source 2](https://github.com/lm-sys/RouteLLM)

**Finding [MEDIUM confidence]**: 70-80% of traffic can go through budget tier. However, BudgetMLAgent shows that truly free/minimal models have zero/very poor success rates. There is a quality floor: top SLMs (3B) achieve 96.7% factual consistency matching 70B, but worst SLMs (460M) score below 40 BertScore. Haiku-class models sit above this floor but the margin matters. [Sources](https://sparkco.ai/blog/optimize-llm-api-costs-token-strategies-for-2025), [Counter](https://arxiv.org/html/2411.07464v1), [Source 3](https://arxiv.org/html/2502.00641v2)

**Finding [HIGH confidence]**: Minor inaccuracies from budget-tier models solidify into system-level false consensus in multi-agent pipelines. "From Spark to Fire" (2026) shows defense success as low as 0.32 without mitigation, recoverable to 0.89 with structured validation. Unstructured networks amplify errors 17.2x. [Sources](https://arxiv.org/abs/2603.04474v1), [Source 2](https://galileo.ai/blog/multi-agent-llm-systems-fail)

### Design implication
- **Haiku tier**: Web search execution, initial relevance screening, source metadata extraction, simple fact extraction. Target: 70-80% of all API calls.
- **Sonnet tier**: Source summarization, cross-source synthesis at tree leaves, query diversification, intermediate merge. Target: 15-25% of calls.
- **Opus tier**: Final synthesis only, contradiction resolution, confidence calibration, executive summary. Target: 2-5% of calls.
- CRITICAL: Every Haiku output that feeds into tree merging must pass through a Sonnet-tier validation gate. Do not let Haiku outputs cascade unchecked.

### 2.4 Query Diversification

**Finding [MEDIUM confidence]**: STORM's persona-based diversification is the most validated approach. Anthropic recommends breadth-first short queries then narrow deep-dives. [Sources](https://arxiv.org/abs/2402.14207), [Source 2](https://www.anthropic.com/engineering/multi-agent-research-system)

**Finding [MEDIUM confidence]**: PICO decomposition research shows that searching all facets of a query actually reduces recall. Use 2-3 most discriminating facets only. LLM query expansion degrades on unfamiliar/ambiguous domains. [Sources](https://pubmed.ncbi.nlm.nih.gov/32679315/), [Source 2](https://arxiv.org/html/2505.12694v1)

### Design implication
- Generate 3-5 diverse search perspectives (persona-based, a la STORM)
- For each perspective, generate 2-3 discriminating queries (not exhaustive facet decomposition)
- Total search budget: standard=15-25 queries, deep=40-60, exhaustive=80-120
- Include a "query effectiveness" feedback loop: if early results are poor, regenerate queries with domain-adapted expansion

### 2.5 Deduplication

**Finding [MEDIUM confidence]**: SimHash (Hamming distance <=3/64 bits = duplicate) is the standard for near-duplicate detection. MinHash LSH outperforms SimHash on binary features. STORM uses soft-merge via vector similarity rather than hard dedup. Over-deduplication can harm quality by reducing source diversity. [Sources](https://research.google.com/pubs/archive/33026.pdf), [Source 2](https://milvus.io/blog/minhash-lsh-in-milvus-the-secret-weapon-for-fighting-duplicates-in-llm-training-data.md), [Source 3](https://arxiv.org/html/2411.04257v3)

### Design implication
- Use URL-based exact dedup first (trivial, no cost)
- Use LLM-based semantic similarity (Haiku tier) for soft-merge: flag duplicates but merge their unique claims rather than discarding
- Do NOT hard-delete near-duplicates; annotate them and let the merge step decide
- Dedup at query-generation level too (STORM pattern): check new queries against already-issued queries

### 2.6 Confidence Calibration

**Finding [HIGH confidence]**: LLMs are poor self-assessors with <30% calibration accuracy. Confidence actually increases with contradictory evidence (anti-Bayesian behavior). This is a fundamental limitation, not a fixable bug. [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC12249208/)

**Finding [MEDIUM confidence]**: RA-RAG's source-reliability-weighted aggregation outperforms baseline RAG. BayesRAG uses Dempster-Shafer evidence theory. Post-hoc calibration partially corrects, but best methods (hidden-state probes) require white-box access unavailable via API. [Sources](https://arxiv.org/abs/2410.22954), [Source 2](https://arxiv.org/abs/2601.07329), [Source 3](https://aclanthology.org/2024.naacl-long.366/)

### Design implication
- Do NOT rely on model self-reported confidence scores
- Implement source-agreement-based confidence: count independent sources per claim
- Use a simple 3-tier scheme: HIGH (3+ independent sources agree), MEDIUM (2 sources or counter-evidence exists), LOW (single source)
- Weight by source credibility tier (peer-reviewed > news > blog > social media)
- Flag anti-consensus claims explicitly rather than averaging them away

---

## 3. Pitfalls to Avoid

### [HIGH confidence] Error cascading in multi-agent pipelines
Multiple independent sources (MAST taxonomy, "From Spark to Fire", Galileo, TDS 17x error analysis) confirm that errors compound catastrophically in multi-agent systems. Unstructured topologies amplify errors 17.2x. Single atomic error seeds cause widespread failure. **Mitigation**: structured coordination topology, independent validation layers between every tree level, circuit breakers.

### [HIGH confidence] Context overflow and agent drift
Anthropic's own system discovered 50+ subagent spawning. Agent drift (progressive semantic/coordination/behavioral degradation) is documented across long-running agent sessions. **Mitigation**: hard caps on agent count, explicit termination conditions, periodic context refresh.

### [HIGH confidence] Silent downstream contamination
Bad output treated as valid input is the most dangerous failure mode. Semantic errors pass validation checks in loosely-typed agent-to-agent communication. **Mitigation**: every inter-agent message must include structured metadata (source count, confidence tier, key claims) that downstream agents can validate.

### [MEDIUM confidence] Hallucination amplification in recursive merging
ROUGE scores decrease with multi-stage zero-shot processing. Abstractive summarization at merge nodes introduces mixed-context hallucinations not present in any source. **Mitigation**: use extractive snippets at leaf level, abstractive only at final synthesis. Include source-grounding checks at each merge.

### [MEDIUM confidence] Over-engineering debate mechanisms
"Stop Overvaluing MAD" (2025) shows multi-agent debate doesn't beat simpler baselines. Sycophancy causes stronger agents to flip to incorrect answers under weaker peer pressure. Accuracy decreases with more rounds on commonsense tasks. **Mitigation**: do NOT implement debate. Use structured disagreement logging and let the Opus synthesis layer resolve contradictions.

### [MEDIUM confidence] Query expansion failure on unfamiliar domains
LLM query expansion degrades on ambiguous/niche topics. Searching all facets reduces recall. **Mitigation**: start with broad queries, use retrieved results to inform narrower queries (iterative refinement, not upfront expansion).

---

## 4. Recommended Approach

### Architecture Overview

```
[User Query]
    |
    v
[OPUS] Intent Analysis & Complexity Classification
    |
    +--> Simple: Single-agent Sonnet research (skip multi-agent)
    +--> Complex: Multi-agent pipeline below
    |
    v
[SONNET] Query Diversification (3-5 perspectives, 2-3 queries each)
    |
    v
[HAIKU x N] Parallel Web Search Execution
    |
    v
[HAIKU] Source Pre-Screening (3-step decomposed scoring)
    |  Discard irrelevant, flag borderline
    v
[HAIKU] Source Dedup (URL exact + semantic soft-merge)
    |
    v
[SONNET] Leaf-Level Extraction & Summarization (groups of 5-8 sources)
    |  Extractive snippets + structured metadata
    v
[SONNET] Validation Gate (fact-check leaf summaries against sources)
    |
    v
[SONNET] Tree Merge Level 1 (merge 3-5 leaf groups, inject key snippets upward)
    |  Lateral context passed between sibling branches
    v
[SONNET] Validation Gate
    |
    v
[OPUS] Final Synthesis + Confidence Calibration + Contradiction Resolution
    |
    v
[Output with source-agreement confidence scores]
```

### Depth Level Configuration

| Parameter | Standard (~1hr) | Deep (~2hr) | Exhaustive (~4hr) |
|---|---|---|---|
| Search queries | 15-25 | 40-60 | 80-120 |
| Max sources processed | 30-50 | 80-150 | 200-400 |
| Tree levels | 2 | 2-3 | 3 |
| Leaf group size | 5-8 sources | 5-8 sources | 5-8 sources |
| Validation gates | 1 (after leaves) | 2 (leaves + merge) | 3 (leaves + each merge) |
| Opus calls | 1 (final only) | 2 (mid + final) | 3 (plan + mid + final) |
| Estimated token budget | 500K-1M | 1.5M-3M | 4M-8M |

### Checkpointing Strategy

Based on LangGraph's production patterns, implement file-based checkpointing:
- Save state after each major phase (search, screening, leaf extraction, each merge level)
- Each checkpoint: JSON file with timestamp, phase ID, accumulated sources, intermediate summaries
- On resume: detect last valid checkpoint, display progress summary, continue from that phase
- Checkpoint location: `output/exhaustive-research/{topic-slug}/checkpoints/`

### Safety Mechanisms

1. **Circuit breaker**: If any agent produces output with <2 cited sources or flags uncertainty >70%, escalate to Sonnet/Opus for re-evaluation rather than propagating
2. **Token budget enforcement**: Hard caps per tier per depth level. If budget exceeded, gracefully degrade (reduce source count, not quality)
3. **Agent count cap**: Maximum 10 concurrent Haiku agents, 5 Sonnet, 1 Opus
4. **Timeout per phase**: Standard=15min/phase, Deep=25min, Exhaustive=40min. If exceeded, checkpoint and report partial results
5. **Duplicate work detection**: Hash all search queries and source URLs; reject duplicates before execution
6. **Structured inter-agent messages**: Every message between agents must include: `{sources_cited: int, confidence: HIGH|MEDIUM|LOW, key_claims: string[], contradictions: string[]}`

---

## 5. Contradictions & Open Questions

### Resolved Contradictions

**Multi-agent vs single-agent performance**: The 90.2% improvement claim applies specifically to well-structured coding tasks (SWE-bench) with explicit coordination. General deployment shows 41-86.7% failure rates. **Resolution**: Multi-agent is valuable ONLY with structured topology, explicit task boundaries, and validation layers. The skill must include a complexity gate that prevents multi-agent overhead on simple queries.

**0% false-negative screening**: The JMIR claim is contested by SIGIR and MDPI research showing LLMs should enhance, not replace, expert judgment. **Resolution**: Treat LLM screening as a high-recall first pass (~95% sensitivity) but never as authoritative. Include a "borderline" category and human-reviewable confidence metadata.

**Budget tier viability**: 70-80% Haiku routing is feasible for search and screening but dangerous for synthesis. "From Spark to Fire" shows minor errors solidify into false consensus. **Resolution**: Use Haiku only for tasks with verifiable outputs (search, URL dedup, metadata extraction). All synthesis and merging at Sonnet minimum.

### Unresolved Contradictions

**Debate value**: ICML 2024 says debate improves factuality; 2025 papers say it doesn't beat baselines. No clear resolution. **Decision**: Skip debate in favor of structured disagreement logging. Lower risk, lower cost.

**Extractive vs abstractive at merge levels**: Extractive has no hallucination risk but loses nuance. Abstractive introduces mixed-context hallucinations. **Decision**: Hybrid approach -- extractive at leaf level, abstractive at merge levels with source-grounding validation.

### Open Questions (insufficient evidence)

1. **Optimal group size for tree leaves**: No peer-reviewed consensus. Our recommendation of 5-8 sources is based on LangChain defaults and general chunking literature, not empirical optimization.
2. **Exact information loss per tree level**: The 50-80% retention figure is from a single medium-credibility source. Real retention depends on compression ratio, domain, and model.
3. **Lateral context passing between branches**: Chain of Agents (NeurIPS 2024) suggests sequential beats parallel, but no one has tested "parallel with lateral context injection" specifically.
4. **Checkpointing overhead**: No data on how much time/tokens checkpointing adds to Claude Code agent workflows specifically.

---

## 6. Knowledge Gaps

| Gap | Impact | Mitigation |
|---|---|---|
| No empirical data on Haiku-class factual accuracy for source screening specifically | Could over/underestimate error rate at leaf level | Build in validation gates; measure in production |
| No benchmark for hierarchical research synthesis (only summarization benchmarks exist) | Cannot objectively evaluate output quality | Define custom evaluation criteria: source coverage, claim accuracy, contradiction detection |
| Token costs for Claude model tiers may shift | Budget estimates may be wrong | Make token budgets configurable parameters, not hardcoded |
| No data on Claude Code's actual agent spawning limits | May hit platform constraints | Test with small scale first; implement graceful degradation |
| Query diversification effectiveness is domain-dependent | May generate poor queries for niche topics | Implement iterative query refinement based on result quality |

---

## 7. Top 20 Sources

| # | Source | Credibility | Round | Key Contribution |
|---|---|---|---|---|
| 1 | [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) | HIGH | R1 | Opus orchestrator pattern, failure modes, 90.2% claim |
| 2 | [From Spark to Fire: Error Cascades](https://arxiv.org/abs/2603.04474v1) | HIGH | R2 | Error amplification quantification, defense success rates |
| 3 | [MAST: Why Multi-Agent Systems Fail](https://arxiv.org/abs/2503.13657) | HIGH | R1/R2 | Failure taxonomy, 41-86.7% failure rates |
| 4 | [NexusSum (ACL 2025)](https://arxiv.org/abs/2505.24575) | HIGH | R1 | Hierarchical 3-agent pipeline, 30% BERTScore gain |
| 5 | [BooookScore (ICLR 2024)](https://arxiv.org/abs/2310.00785) | HIGH | R1 | Hierarchical summarization tradeoffs |
| 6 | [STORM (Stanford)](https://arxiv.org/abs/2402.14207) | HIGH | R1/R2 | Persona-based query diversification |
| 7 | [Difficulty-Aware Multi-LLM Routing](https://arxiv.org/html/2509.11079v1) | HIGH | R1 | 36% cost savings, 11.21% accuracy gain |
| 8 | [LLM Calibration Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12249208/) | HIGH | R2 | <30% calibration accuracy, anti-Bayesian behavior |
| 9 | [Claude 3.5 Screening Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12657656/) | HIGH | R1 | 0.95 sensitivity for title+abstract screening |
| 10 | [JudgeRank](https://arxiv.org/html/2412.05579v2) | HIGH | R1 | 3-step decomposed relevance scoring |
| 11 | [Chain of Agents (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/ee71a4b14ec26710b39ee6be113d7750-Paper-Conference.pdf) | HIGH | R1 | Sequential > parallel tree without lateral context |
| 12 | [Google Cloud Long-Doc Summarization](https://cloud.google.com/blog/products/ai-machine-learning/long-document-summarization-with-workflows-and-gemini-models) | MEDIUM | R1 | Source snippet injection into summaries |
| 13 | [Stop Overvaluing MAD (2025)](https://arxiv.org/abs/2502.08788) | HIGH | R1 | Debate doesn't beat simpler baselines |
| 14 | [Galileo: 17x Error Trap](https://galileo.ai/blog/multi-agent-llm-systems-fail) | MEDIUM | R1/R2 | 17.2x error amplification, coordination failures |
| 15 | [RA-RAG](https://arxiv.org/abs/2410.22954) | HIGH | R2 | Source-reliability-weighted aggregation |
| 16 | [BayesRAG](https://arxiv.org/abs/2601.07329) | HIGH | R2 | Dempster-Shafer evidence theory for confidence |
| 17 | [Agent Drift](https://arxiv.org/abs/2601.04170) | HIGH | R2 | Progressive degradation in long-running agents |
| 18 | [RouteLLM](https://github.com/lm-sys/RouteLLM) | MEDIUM | Cross | 85% cost reduction, 95% quality retention |
| 19 | [JMIR LLM Screening](https://www.jmir.org/2025/1/e67488) | HIGH | R1 | 95.5% time reduction (contested 0% false-neg) |
| 20 | [LangGraph Persistence](https://docs.langchain.com/oss/javascript/langgraph/persistence) | MEDIUM | Cross | Checkpointing patterns for long-running workflows |

---

## 8. Key Architectural Decisions Summary

| Decision | Rationale | Confidence |
|---|---|---|
| 3-tier model routing (Haiku/Sonnet/Opus) | Multiple sources confirm 36-85% cost savings with minimal quality loss when routing is difficulty-aware | HIGH |
| 2-3 level tree (not deeper) | Each level loses 20-50% information; 4+ levels would retain <10% | MEDIUM |
| No multi-agent debate | Research shows debate doesn't beat baselines and introduces sycophancy risk | HIGH |
| Validation gates between every tree level | Error cascading is the #1 documented failure mode in multi-agent systems | HIGH |
| Source-agreement confidence (not self-reported) | LLMs have <30% calibration accuracy and show anti-Bayesian behavior | HIGH |
| Extractive at leaves, abstractive at merge | Balances hallucination risk (extractive) with synthesis quality (abstractive) | MEDIUM |
| Persona-based query diversification (STORM pattern) | Best-validated approach; avoids over-expansion that reduces recall | MEDIUM |
| File-based checkpointing per phase | Enables resume for 1-4 hour workflows; production-proven pattern | MEDIUM |
| Complexity gate before multi-agent | Prevents 15x cost overhead on simple queries; matches Anthropic's own lessons | HIGH |
| Soft-merge dedup (not hard delete) | Over-deduplication harms diversity; soft-merge preserves unique claims | MEDIUM |
