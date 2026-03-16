# Severity Classification Guide

## Severity Tiers

This guide helps reviewers consistently classify findings. Based on the Graphite four-tier model and Netlify Feedback Ladder.

### BLOCKING (Must Fix)
Commit cannot proceed. These are correctness or safety issues that will cause harm.

**Examples**:
- SQL injection via unsanitized user input
- Hardcoded secrets or API keys in source
- Null pointer dereference on a guaranteed code path
- Data loss (overwriting without backup, truncating without confirmation)
- Authentication bypass
- Broken database migration that can't be rolled back
- Crash on startup or common code path

**NOT BLOCKING** (commonly over-classified):
- Missing input validation on internal-only functions
- Theoretical race condition with no realistic trigger
- Code smell or poor naming

### MAJOR (Should Fix)
Significant issues that affect functionality or maintainability but don't cause immediate harm.

**Examples**:
- Off-by-one error in loop boundary
- Missing error handling that swallows exceptions silently
- Broken test that will fail in CI
- API contract change without updating consumers
- Missing pagination on a query that could return unbounded results
- Incorrect type assertion that will fail at runtime

**NOT MAJOR** (commonly over-classified):
- Style inconsistency
- Missing optional error handling for unlikely cases
- Verbose but correct code

### MINOR (Consider Fixing)
Quality improvements that don't affect correctness.

**Examples**:
- Inconsistent naming convention
- Missing type annotation on a public function
- Duplicated code that could be extracted
- TODO comment without a tracking issue
- Unused import or variable

### NIT (Noted)
Trivial preferences. Only surface these if no higher-severity findings exist.

**Examples**:
- Whitespace formatting preference
- Comment wording suggestion
- Variable name synonym preference
- Import ordering

## Decision Framework

When unsure about severity, ask:
1. **Will this cause a bug in production?** → BLOCKING
2. **Will this cause a test failure or break a consumer?** → MAJOR
3. **Will a future developer be confused by this?** → MINOR
4. **Is this just my preference?** → NIT

## False Positive Indicators

Downgrade or suppress a finding if:
- The "issue" is already handled by a guard clause or try/catch you didn't initially see
- The code follows an established pattern in the codebase (even if you'd do it differently)
- The "vulnerability" requires an attacker to already have access they shouldn't have
- The "missing validation" is on an internal function that only receives pre-validated input
