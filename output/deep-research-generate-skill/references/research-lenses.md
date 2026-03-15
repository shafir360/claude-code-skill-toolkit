# Research Lenses for Deep Research Skill Generation

Research lenses define the angles from which agents investigate a skill's domain. Each lens targets a different type of insight. Use 4-6 lenses for the two-round deep research process — pick the ones most relevant to the skill's domain.

## Lenses for Skill Generation (Round 1: Broad Sweep)

### 1. Prior Art
**Purpose**: Discover existing tools, scripts, CLI utilities, or Claude Code skills that solve the same or similar problem.

Example sub-questions:
- What tools already exist for this task? What do they do well? What do they do poorly?
- Are there Claude Code skills, VS Code extensions, or CLI tools that overlap?
- What patterns do successful tools in this space share?

**How to use findings**: Inform the skill's approach — borrow proven patterns, avoid known failures, differentiate from existing tools.

### 2. Domain Patterns
**Purpose**: Identify established conventions, standards, and best practices in the skill's target domain.

Example sub-questions:
- What are the standard workflows practitioners follow for this task?
- Are there industry standards, specs, or conventions that apply?
- What input/output formats are expected?

**How to use findings**: Shape the skill's phase structure and output format to match domain conventions.

### 3. Pitfalls & Failure Modes
**Purpose**: Find common mistakes, edge cases, and failure modes when building or using tools in this domain.

Example sub-questions:
- What goes wrong most often when people attempt this task?
- What edge cases cause tools in this space to break?
- What are the security, performance, or correctness risks?

**How to use findings**: Add specific items to the skill's Rules section. Design phases to guard against known failure modes. Prioritize HIGH-confidence pitfalls.

### 4. Input/Output Patterns
**Purpose**: Understand the data formats, structures, and variations the skill will encounter.

Example sub-questions:
- What input formats do users typically provide?
- What output format do users expect?
- What are the boundary cases (empty input, huge files, special characters)?

**How to use findings**: Define the skill's argument-hint, input validation, and output template.

### 5. User Workflow Context
**Purpose**: Understand how practitioners currently perform this task manually — what's tedious, error-prone, or time-consuming.

Example sub-questions:
- What steps do people follow when doing this manually today?
- Which steps are most error-prone or tedious?
- What would make this task 10x easier?

**How to use findings**: Prioritize automating the most painful steps. Design the skill to fit naturally into existing workflows.

---

## Lenses for Round 2: Targeted Deep Dives

Round 2 lenses are dynamically determined by the Opus gap analysis agent based on Round 1 findings. Common patterns include:

### Gap-Filling Collector Lenses
- **Thin Coverage Areas**: Topics where Round 1 found only 1 source — seek independent verification
- **Citation Chain Following**: Starting from key Round 1 sources, find papers/articles that cite or respond to them
- **Contradictory Evidence**: Seek evidence that challenges the prevailing Round 1 findings

### Skeptic Lens
- **Assumption Challenge**: The Opus skeptic agent receives the 2-3 strongest Round 1 claims and actively tries to disprove or nuance them
- **Counter-Evidence Search**: Looks for criticisms, rebuttals, alternative explanations, disputed sources
- **Boundary Testing**: Tests whether "always true" claims hold in all contexts

---

## Agent Prompt Template

When spawning research agents, each agent's prompt MUST include:

1. The overall research topic (what skill is being generated)
2. The specific lens assigned to this agent (from above)
3. 2-3 sub-questions from that lens
4. This instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs."

## Fallback

If fewer than 3 agents return usable results in Round 1, skip Round 2 and proceed to generation using existing knowledge and Round 1 findings. Note in the output that research was limited.
