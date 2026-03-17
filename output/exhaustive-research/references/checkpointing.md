# Checkpointing & Progress Reporting

## Checkpoint Schema

Save a JSON checkpoint file after each major phase completes. Location: `{save_dir}/checkpoints/`

```json
{
  "skill": "exhaustive-research",
  "topic": "<research topic>",
  "depth": "standard|deep|exhaustive",
  "phase_completed": 3,
  "phase_name": "pre-screening",
  "timestamp": "2026-03-16T14:32:00Z",
  "elapsed_minutes": 18,
  "data": {
    "bootstrap_sources": 12,
    "search_queries_executed": 45,
    "candidates_screened": 247,
    "sources_passed": 89,
    "sources_borderline": 34,
    "sources_failed": 124,
    "reader_agents_completed": 0,
    "mini_reports_saved": 0,
    "intermediate_reports_saved": 0
  },
  "files": {
    "search_results": "checkpoints/phase2_search_results.json",
    "screening_verdicts": "checkpoints/phase3_screening_verdicts.json",
    "passed_sources": "checkpoints/phase3_passed_sources.json"
  },
  "agent_stats": {
    "haiku_spawned": 6,
    "haiku_completed": 6,
    "haiku_failed": 0,
    "sonnet_spawned": 3,
    "sonnet_completed": 3,
    "sonnet_failed": 0,
    "opus_spawned": 0,
    "opus_completed": 0,
    "opus_failed": 0
  },
  "failures": [],
  "search_retry_executed": false,
  "agent_retries": {
    "batch_5": {"retries": 1, "status": "TIMED_OUT"},
    "batch_12": {"retries": 1, "status": "TIMED_OUT"}
  },
  "wave_status": [
    {"phase": 4, "wave": 1, "spawned": 10, "completed": 9, "timed_out": ["batch_5"]},
    {"phase": 4, "wave": 2, "spawned": 10, "completed": 10, "timed_out": []}
  ]
}

**Note**: Only include fields relevant to the completed phase. Omit fields that haven't been populated yet (e.g., no `reader_agents_completed` at Phase 2). On resume, the presence/absence of fields indicates what data is available.

**Per-agent retry rule**: On resume, do NOT re-run any agent with `retries >= 1` in `agent_retries`. Treat it as a permanent coverage gap. This prevents infinite retry loops for persistently failing agents.

**Search retry flag**: `search_retry_executed` tracks whether Phase 2b's "retry with broader queries" has been used. On resume from Phase 2, check this flag before retrying — if true, skip directly to Phase 3.
```

## Checkpoint Save Points

| After Phase | Checkpoint File | What It Preserves |
|---|---|---|
| Phase 0 (Bootstrap) | `checkpoint_p0.json` | Bootstrap context, extracted source URLs |
| Phase 1 (Clarify) | `checkpoint_p1.json` | Research plan, themes, depth, save location |
| Phase 2 (Search) | `checkpoint_p2.json` | All search queries + raw result snippets |
| Phase 3 (Screen) | `checkpoint_p3.json` | Screening verdicts, PASS/BORDERLINE/FAIL lists |
| Phase 4 (Read) | `checkpoint_p4.json` | All mini-report file paths + validation results |
| Phase 5 (Merge) | `checkpoint_p5.json` | All intermediate report file paths |
| Phase 6 (Gap) | `checkpoint_p6.json` | Gap analysis, Round 2 targets, skeptic claims |
| Phase 7 (Round 2) | `checkpoint_p7.json` | Collector + skeptic results |
| Phase 8 (Synthesis) | `checkpoint_p8.json` | Final synthesis output |

## Resume Logic

On skill invocation, before Phase 0:

1. Check if `{save_dir}/checkpoints/` exists
2. If yes, find the highest-numbered `checkpoint_p*.json`
3. Read it and display: "Found checkpoint at Phase [N] ([name]) from [timestamp]. Resume from here? (Y/n)"
4. **Validate checkpoint**: verify all output files referenced in the checkpoint still exist and are non-empty. If any are missing or corrupted, offer: (a) resume from the previous phase instead, (b) start fresh.
5. If user confirms and files valid: load the checkpoint data, skip to Phase N+1
6. If user declines: start fresh, archive old checkpoints to `checkpoints/archived/`

## Implicit File Checkpointing

Each agent's output file serves as an implicit sub-phase checkpoint:
- Mini-reports: `{save_dir}/mini-reports/batch_{N}.md`
- Intermediate reports: `{save_dir}/intermediate/group_{N}.md`
- Round 2 collector reports: `{save_dir}/round2/collector_{N}.md`
- Skeptic report: `{save_dir}/round2/skeptic.md`

On phase failure, check which output files already exist. Only re-run agents whose output files are missing. This provides per-agent recovery without per-agent checkpoint overhead.

## Wave-Level Checkpointing (Exhaustive Depth)

At Exhaustive depth, agent spawning is broken into waves. Mini-reports and intermediate reports are written to disk **after each wave completes** (not just at the end of the phase). This means:
- If the skill is interrupted mid-phase, completed waves are preserved
- On resume, check which `batch_{N}.md` / `group_{N}.md` files already exist
- Only re-run agents for batches whose output files are missing
- Timed-out agents from a prior wave are NOT re-run (they are coverage gaps, not failures)

Wave progress is reflected in the Phase Recap with an additional line:
```
- Waves: [completed]/[total] (wave size: [N])
```

## Progress Reporting Template

After each phase completes, emit a Phase Recap block in chat. Use this exact format:

```
---
## Phase [N] Complete: [Phase Name]
- Agents: [completed]/[total] ([model tier])
- Sources: [processed] screened | [passed] passed | [failed] filtered
- Time: [elapsed] min (cumulative: [total] min)
- Issues: [count] flagged, [count] failed, [count] skipped
- Next: Phase [N+1] — [name] (est. [time] min)
---
```

For phases with parallel agents, also show a brief recap:

```
### Agent Recap
- Batch 1-5: completed (3 PASS, 1 FLAG, 1 PASS)
- Batch 6-10: completed (4 PASS, 1 REJECT — no citations)
- Batch 11: timeout — skipped, coverage gap noted
```

## Early Termination Triggers

Pause and ask the user before continuing if:

1. **Low pass rate**: Phase 3 screening shows <20% of candidates passing → "Only [N]% of sources passed screening. This suggests the search queries may not be well-targeted. Options: (a) Continue with [N] sources at reduced depth, (b) Refine the topic and re-search, (c) Abort"
2. **High failure rate**: >30% of agents in any phase fail → "Over 30% of agents failed in Phase [N]. Options: (a) Continue with partial results, (b) Retry failed agents once, (c) Abort and save partial report"
3. **Budget concern**: If more than 60% of the depth-level agent budget has been consumed before Phase 6 → "Agent budget is running high. Consider reducing Round 2 scope."
