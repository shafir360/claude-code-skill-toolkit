# Enhanced Design Brief: commit-review Skill Improvement
_Generated: 2026-03-16 | Sources: 25+ | Rounds: 2 (generation + improvement) | Confidence: HIGH_

## Improvement Research Summary

Two rounds of deep research across 10 agents investigated: best-in-class review tools, multi-agent architecture optimization, language-agnostic review patterns, solo developer workflows, and false positive reduction techniques.

## Key Improvements Applied

### 1. Confidence-Weighted Aggregation (replaced majority vote) `[Confidence: H]`
Majority vote is provably broken — 0% recovery on consensus-wrong cases (AgentAuditor, arxiv 2602.09341). Replaced with weighted scoring: HIGH 3x, MEDIUM 2x, LOW 1x, plus divergence auditing for disagreements.

### 2. Chain-of-Verification (CoVe) `[Confidence: H]`
ACL 2024 Findings paper shows 50-70% hallucination reduction. Added as Step 3 in consolidation: generates verification questions for BLOCKING/MAJOR findings, answers independently by re-reading code.

### 3. Evidence-Grounding `[Confidence: H]`
SGCR framework (IEEE ASE 2025) achieved 90.9% improvement in developer adoption with specification-grounded review. All findings now require file:line + code snippet. Ungrounded findings auto-downgraded to NIT.

### 4. Separated Judgment from Fix Generation `[Confidence: M]`
arxiv 2603.00539 showed GPT-4o false negative rate jumped from 26.2% to 73.2% when explanations/fixes required in same prompt. Agents now emit judgment-only verdicts; fix suggestions generated in separate pass for accepted findings only.

### 5. Method-Differentiated Agents `[Confidence: M]`
Replaced topic-based personas (correctness/security/architecture) with distinct verification methods (data-flow tracing / invariant checking / anti-pattern matching). Based on CMU S3D research on semi-formal reasoning prompts.

### 6. Randomized Diff Order `[Confidence: M]`
BugBot (Cursor) uses randomized diff ordering across parallel passes to break positional bias. Trivial to implement, high value for decorrelating agent errors.

### 7. Language-Specific Review Concerns `[Confidence: M]`
Added Phase 4 for language detection with specific review criteria for Python, TypeScript, React, Next.js, Go, and Rust. Based on CodeRabbit's "universal engine + language rules" pattern.

### 8. Adaptive Mode as Default `[Confidence: M]`
Removed confirmation prompt for auto-detected mode. Proceeds immediately unless user explicitly overrides. Based on NN/g research on mode usability.

### 9. Solo Developer Focus `[Confidence: M]`
Updated positioning as "second pair of eyes" for solo developers. Based on finding that no dedicated solo-dev review tooling exists — this fills a genuine gap.

## Contradictions Resolved

| Topic | Resolution |
|-------|-----------|
| Multi-agent vs single-agent | Kept 3 agents — Qodo F1 data supports, but replaced consolidation mechanism (the weakness was majority vote, not agent count) |
| Evidence-grounding helps vs hurts | Require code citations YES, but separate from explanation/fix generation (prevents overcorrection) |
| Architecture agent value with evidence | Architecture agent uses lighter evidence bar (file/pattern references, not exact line citations) |

## Skeptic's Impact
- Multi-agent architecture: **Kept** but consolidation fundamentally redesigned
- Evidence-grounding: **Kept with caveat** — separate judgment from explanation
- Quick/deep modes: **Kept** but made adaptive default, removed unnecessary confirmation

## Sources
| # | Source | Credibility | Impact on Skill |
|---|--------|-------------|-----------------|
| 1 | [AgentAuditor (arxiv 2602.09341)](https://arxiv.org/html/2602.09341v1) | HIGH | Replaced majority vote |
| 2 | [CoVe (ACL 2024)](https://aclanthology.org/2024.findings-acl.212/) | HIGH | Added verification step |
| 3 | [SGCR (arxiv 2512.17540)](https://arxiv.org/abs/2512.17540) | HIGH | Evidence-grounding design |
| 4 | [LLM Overcorrection (arxiv 2603.00539)](https://arxiv.org/abs/2603.00539) | MEDIUM | Separated judgment/fix |
| 5 | [BugBot Architecture (Cursor)](https://cursor.com/blog/building-bugbot) | HIGH | Randomized diff order |
| 6 | [Beyond Majority Voting (arxiv 2510.01499)](https://arxiv.org/abs/2510.01499) | HIGH | Weighted confidence design |
| 7 | [Mixture-of-Agents (arxiv 2406.04692)](https://arxiv.org/html/2406.04692v1) | HIGH | Validated agent differentiation |
| 8 | [CMU Semi-formal Reasoning](http://reports-archive.adm.cs.cmu.edu/anon/s3d2025/CMU-S3D-25-101.pdf) | HIGH | Method differentiation |
| 9 | [Google/MIT Agent Scaling](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) | HIGH | Validated 3-agent count |
| 10 | [Chroma Context Rot](https://research.trychroma.com/context-rot) | HIGH | Context limits |
| 11 | [CodeRabbit V3 Architecture](https://www.coderabbit.ai/blog/how-coderabbit-delivers-accurate-ai-code-reviews-on-massive-codebases) | HIGH | Evidence-grounding pattern |
| 12 | [Qodo Merge Benchmark](https://www.qodo.ai/blog/qodo-outperforms-claude-in-code-review-benchmark/) | MEDIUM | Multi-agent validation |
| 13 | [NN/g Modes Research](https://www.nngroup.com/articles/modes/) | HIGH | Adaptive mode UX |
| 14 | [Solo Dev Review (Dr. Greiler)](https://www.michaelagreiler.com/code-review-pitfalls-slow-down/) | HIGH | Solo dev positioning |
| 15 | [Graphite Severity System](https://graphite.com/guides/code-review-comment-types) | HIGH | Severity framework |
