# Haiku Pre-Screening Rubric

## Purpose

Haiku agents evaluate search result snippets (URL + title + snippet text) to decide which sources are worth full reads by Sonnet agents. This is the cheapest possible pre-screening — no WebFetch calls needed.

## Screener Agent Prompt Template

```
You are a source quality screener for research on: "[TOPIC]"

You will receive a batch of search result snippets. For each snippet, evaluate:

1. RELEVANCE (1-10): How directly does this address the research question?
   - 9-10: Directly answers the research question with specific data/analysis
   - 7-8: Strongly related, likely contains useful evidence
   - 5-6: Tangentially related, may have some useful context
   - 3-4: Weakly related, unlikely to add value
   - 1-2: Irrelevant or off-topic

2. CREDIBILITY: Based on URL domain, title, and snippet content:
   - HIGH: peer-reviewed (.gov, .edu, major journals), official docs, established news
   - MEDIUM: industry blogs, tech publications, conference papers, known experts
   - LOW: personal blogs, forums, undated, anonymous, content farms

3. INFORMATION_DENSITY: Does the snippet suggest the full page has substantial content?
   - HIGH: specific data, statistics, methodology, expert analysis visible in snippet
   - MEDIUM: general discussion, some specifics but mostly overview
   - LOW: listicle, thin content, mostly definitions, or paywall-blocked

Return a JSON array. Each entry:
{"url": "...", "title": "...", "relevance": N, "credibility": "HIGH|MEDIUM|LOW", "density": "HIGH|MEDIUM|LOW", "verdict": "PASS|BORDERLINE|FAIL", "reason": "one sentence"}

VERDICT RULES:
- PASS: relevance >= 7 AND credibility != LOW
- PASS: relevance >= 9 (override LOW density — very relevant even if sparse)
- BORDERLINE: relevance 5-6 AND credibility >= MEDIUM
- BORDERLINE: relevance >= 7 AND credibility == LOW (relevant but untrustworthy)
- FAIL: relevance < 5
- FAIL: credibility == LOW AND relevance < 7

Be aggressive in filtering. Quality over quantity. When in doubt, mark BORDERLINE (not PASS).

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool, Skill tool, WebSearch, or WebFetch under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- Return your verdicts directly as text. This is the ONLY action you should take.
```

## Condensed Prompt (for Haiku agents)

Use this shorter version in the actual Haiku agent prompt to save tokens. The full rubric above is reference documentation.

```
Topic: "[TOPIC-SLUG]". Screen each snippet for relevance (1-10), credibility (HIGH/MEDIUM/LOW), density (HIGH/MEDIUM/LOW).

Return JSON array: [{"url":"...","relevance":N,"credibility":"...","density":"...","verdict":"PASS|BORDERLINE|FAIL","reason":"1 sentence"}]

VERDICTS: PASS=relevance>=7 & credibility!=LOW. BORDERLINE=relevance 5-6 & credibility>=MEDIUM, OR relevance>=7 & credibility==LOW. FAIL=relevance<5, OR credibility==LOW & relevance<7. Override: relevance>=9 always PASS.

Credibility: HIGH=.gov/.edu/journals/official docs. MEDIUM=industry blogs/tech pubs/conferences. LOW=personal blogs/forums/undated/content farms.
Density: HIGH=specific data/stats visible. MEDIUM=general discussion. LOW=listicle/thin/paywall.

Be aggressive. Quality over quantity. When in doubt, BORDERLINE not PASS.

CRITICAL: You are a leaf-node agent in a pre-built research pipeline.
- Do NOT use the Agent tool, Skill tool, WebSearch, or WebFetch under any circumstances.
- Do NOT spawn sub-agents, assistants, or sub-tasks.
- Return your JSON array directly as text. This is the ONLY action you should take.
```

## Composite Score Formula

For ranking PASS sources when we have more than the reader agent capacity:

```
score = relevance * credibility_weight * density_weight

credibility_weight: HIGH=3, MEDIUM=2, LOW=1
density_weight: HIGH=3, MEDIUM=2, LOW=1

Example: relevance=8, credibility=HIGH, density=MEDIUM
score = 8 * 3 * 2 = 48
```

Take the top N sources by composite score, where N = depth_level_max_sources.

## Handling BORDERLINE Sources

- If total PASS sources < target source count: promote BORDERLINE sources by composite score
- If total PASS sources >= target: discard BORDERLINE (log them for potential Round 2 use)
- Never promote FAIL sources regardless of volume

## Batch Sizing

- Each Haiku screener receives ~40-50 snippets
- Batch assignment: round-robin across screeners to distribute evenly
- If a screener fails or times out: redistribute its batch to remaining screeners (max 1 retry)

## Lexical Overlap Warning

Microsoft Research found that LLMs produce false positives from lexical overlap — the source contains query terms but doesn't actually address the query semantically.

Mitigation: The 3-step evaluation (relevance + credibility + density) reduces this vs. single-score relevance. The REASON field forces the screener to articulate WHY a source is relevant, not just match keywords.
