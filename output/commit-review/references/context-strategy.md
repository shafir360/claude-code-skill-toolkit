# Context Gathering Strategy

## Principles

Based on research into AI code review context retrieval (Microsoft CodePlan, Chroma Context Rot study, DiffScope architecture):

1. **Relevance density > raw coverage**: Including irrelevant files degrades review accuracy more than missing some context
2. **Active tooling > pre-loading**: Use grep/glob on-demand rather than pre-loading large file sets
3. **1-2 hop dependency traversal**: Follow imports and callers, but don't go deeper
4. **Cap at ~50K tokens**: Models degrade beyond this even with large context windows

## Context Gathering Checklist

### Always Read
- [ ] Each changed file in full (current version)
- [ ] Project README.md, CLAUDE.md, CONTRIBUTING.md (if they exist)

### Conditional Reads (based on diff content)
- [ ] Files that import from changed files (use grep for import/require statements)
- [ ] Files that changed functions call into (1 hop via grep)
- [ ] Test files matching changed files (`*test*`, `*spec*`, `*_test.*`)
- [ ] API route definitions (if endpoints changed)
- [ ] Database migration files (if models changed)
- [ ] Configuration files (if env/config references changed)
- [ ] Type definition files (if interfaces/types changed)

### Never Read
- node_modules/, vendor/, .git/
- Build output (dist/, build/, out/)
- Generated files (*.generated.*, *.auto.*)
- Binary files, images, fonts
- Lock files (package-lock.json, yarn.lock) unless the diff specifically changes them
- Large data files (*.csv, *.json fixtures over 1000 lines)

## File Reading Strategy

For large files (over 200 lines) that aren't directly changed:
- Read only the relevant function/class definition, not the entire file
- Use grep to locate the specific function, then read +-20 lines around it
- Read type signatures and interfaces in full (usually compact)

## Maximum Limits

| Metric | Limit | Rationale |
|--------|-------|-----------|
| Files beyond changed | 15 | Prevent context explosion |
| Lines per context file | 200 | Focus on relevant sections |
| Total context tokens | ~50K | Stay in reliable performance range |
| Dependency hops | 2 | Diminishing returns beyond this |
