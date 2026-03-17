# Depth Level Configuration

## Depth Levels

The user selects depth via argument (e.g., `/exhaustive-research deep: <topic>`) or when prompted.

| Parameter | Standard (~1hr) | Deep (~2hr) | Exhaustive (~4hr) |
|---|---|---|---|
| **Search queries** | 15-25 | 40-60 | 80-120 |
| **Sources pre-screened** | 80-150 | 200-350 | 400-600 |
| **Sources deeply read** | 30-50 | 80-150 | 200-400 |
| **Haiku screener agents** | 2-3 | 4-6 | 8-12 |
| **Snippets per screener** | ~40 | ~50 | ~50 |
| **Sonnet reader agents (Level 0)** | 5-8 | 12-20 | 25-50 |
| **Sources per reader** | 5-7 | 5-7 | 5-7 |
| **Level 1 merge agents** | 2-3 | 4-5 | 6-10 |
| **Level 2 merge agents** | 0 | 0-1 | 2-3 |
| **Tree depth** | 2 | 2-3 | 3 |
| **Validation gates** | 1 (after leaves) | 2 (leaves + merge) | 3 (leaves + each merge) |
| **Round 2 collectors** | 3-4 | 5-6 | 8-10 |
| **Skeptic agents (Opus)** | 1 | 1 | 2 |
| **Query gen agents** | 1 | 1 | 1 |
| **Opus calls total** | 1 (final synthesis) | 2 (skeptic + final) | 3 (2 skeptics + final) |
| **Total agents** | ~15-20 | ~30-40 | ~55-80 |
| **Per-phase timeout** | 15 min | 25 min | 40 min |
| **Overall hard cap** | 75 min | 150 min | 270 min |
| **Estimated tokens** | 500K-1M | 1.5M-3M | 4M-8M |
| **Reader wave size** | all at once (≤8) | all at once (≤20) | 10 per wave |
| **Screener wave size** | all at once (≤3) | all at once (≤6) | 6 per wave |
| **Merge wave size** | all at once (≤3) | all at once (≤5) | 5 per wave |
| **Collector wave size** | all at once (≤4) | all at once (≤6) | 5 per wave |
| **Budget warning threshold** | 60% of 750K | 60% of 2.25M | 60% of 6M |
| **Orchestrator context target** | <300K | <500K | <700K |
| **Orchestrator context hard cap** | 400K | 600K | 800K |

## Depth Selection Logic

1. If user specifies depth in arguments (e.g., `deep: climate change impact`), use that
2. If user provides `/deep-research` bootstrap output, default to `deep` (they already did basic research)
3. If no depth specified, ask: "What depth level? Standard (~1hr, ~40 sources), Deep (~2hr, ~100 sources), or Exhaustive (~4hr, ~300 sources)?"
4. If user says "just go" or gives no preference, default to `standard`

## Dynamic Scaling

Within a depth level, scale agent counts based on actual source volume:
- If pre-screening yields fewer sources than expected, reduce reader agent count proportionally
- If pre-screening yields more, cap at the depth level maximum
- Formula: `reader_agents = min(ceil(passing_sources / 6), depth_max_readers)`

## Model Tier Allocation by Phase and Depth

Note: "Search execution" refers to WebSearch calls made by the orchestrator, not agents.
Query GENERATION (Phase 2a) uses Sonnet because generating diverse research perspectives requires higher reasoning.

| Phase | Standard | Deep | Exhaustive |
|---|---|---|---|
| Search execution (WebSearch) | Orchestrator | Orchestrator | Orchestrator |
| Query generation (Phase 2a) | 1 Sonnet | 1 Sonnet | 1 Sonnet |
| Pre-screening (Phase 3) | Haiku | Haiku | Haiku |
| Deduplication | Orchestrator | Orchestrator | Orchestrator |
| Source reading (Phase 4a) | Sonnet | Sonnet | Sonnet |
| Validation gates (Phase 4b, 5b) | **Haiku** | **Haiku** | Sonnet |
| Tree merge (Level 1, Phase 5a) | Sonnet | Sonnet | Sonnet |
| Tree merge (Level 2, Phase 5c) | — | Sonnet | Sonnet |
| Gap analysis (Phase 6) | Sonnet | Sonnet | Sonnet |
| Round 2 collectors (Phase 7) | Sonnet | Sonnet | Sonnet |
| Skeptic review (Phase 7) | Opus | Opus | Opus |
| Final synthesis (Phase 8) | Opus | Opus | Opus |
