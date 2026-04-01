---
description: Post-phase comprehensive review -- debug, resolve deps, optimize, and harden an entire phase's code
argument-hint: phase-number (e.g., 1, 2, 3)
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Run a comprehensive post-phase review for Phase $ARGUMENTS.

## Purpose

After all specs in a phase are complete, sweep the entire phase's codebase for issues that individual spec implementations may have missed. Specs are built incrementally -- this review looks at the WHOLE picture.

---

## Step 0: Verify Phase Complete

Read `roadmap.md`. Confirm ALL specs in the given phase have status `done`. If any spec is NOT done, STOP and report which specs are incomplete.

---

## Step 1: Full Test Suite + Lint + Typecheck

Run the complete quality gate:

```bash
make check  # or: ruff check + mypy + pytest
```

If anything fails, fix it before proceeding. Do NOT skip failures.

---

## Step 2: Debug Sweep

Scan all source files touched by this phase for:

1. **Runtime errors**: Import the modules, instantiate key classes, call key functions with edge-case inputs
2. **Uncaught exceptions**: grep for bare `except:` (too broad), missing error handling on external calls
3. **Silent failures**: grep for `pass` inside except blocks, swallowed errors without logging
4. **Test gaps**: Run `pytest --cov` and identify any lines/branches with 0% coverage in phase files
5. **Flaky tests**: Run tests 3 times -- any test that fails intermittently is flagged

Report findings as a table:

| File | Line | Issue | Severity | Fix |
|------|------|-------|----------|-----|

Fix all CRITICAL and HIGH issues. Report MEDIUM as recommendations.

---

## Step 3: Dependency Health

1. **Circular imports**: Attempt `python -c "import mcpguard"` -- if it fails, there's a circular import
2. **Unused dependencies**: Check `pyproject.toml` deps vs actual imports across all source files. Flag any declared but unused deps.
3. **Missing dependencies**: grep for all `import` and `from X import` statements. Verify every third-party package is in `pyproject.toml`
4. **Version conflicts**: Run `pip check` to detect incompatible versions
5. **Transitive vs direct**: Any package imported directly but not declared in `pyproject.toml` must be added

Fix any issues found.

---

## Step 4: Code Optimization

Review all phase source files for:

### Performance
- **Unnecessary computation**: Repeated work that can be cached or computed once
- **Startup latency**: Heavy imports at module level that should be lazy
- **Memory**: Large default collections, unbounded lists, missing `__slots__` on hot-path classes

### Structure
- **Dead code**: Unused functions, unreachable branches, commented-out code
- **Duplication**: Similar logic across files that should be extracted
- **File size**: Any file exceeding 400 lines should be flagged (800 max per CLAUDE.md)
- **Complexity**: Functions exceeding 50 lines or nesting > 4 levels deep

### Parallelization
- **Independent operations**: Identify any sequential operations that could run concurrently
- **Async readiness**: Flag sync code that will need to become async in future phases (document, don't change)

Report findings and apply fixes. For async-readiness notes, add `# TODO(S{future_spec}): convert to async` comments only.

---

## Step 5: Security Hardening

Review all phase source files for:

1. **Secret exposure**: Any path where API keys, tokens, or credentials could leak into logs, error messages, repr(), or serialization. Verify `SecretStr` is used consistently.
2. **Input validation**: Any function accepting external input (CLI args, env vars, file paths) must validate before use
3. **Path traversal**: Any `Path` operations must not allow escaping intended directories
4. **Injection**: Any string interpolation with external input (f-strings in SQL, shell commands, log messages)
5. **Permissions**: Any file creation must use appropriate permissions (0600 for sensitive files per CLAUDE.md)
6. **Authentication hooks**: Identify where authentication/authorization checks will be needed in future phases. Add `# TODO(S{spec}): add auth check` comments.

Report findings as:

| File | Line | Vulnerability | OWASP | Severity | Fix |
|------|------|--------------|-------|----------|-----|

Fix all CRITICAL and HIGH immediately. Document MEDIUM as TODOs.

---

## Step 6: Cross-Module Integration Check

Verify that all modules in the phase work together correctly:

1. **Import chain**: Import every module in dependency order -- no errors
2. **Type consistency**: Types used across module boundaries match (e.g., `Severity` enum used the same way everywhere)
3. **Config flow**: Trace how `Settings` -> `ScanConfig` -> downstream modules connect
4. **Logging integration**: Verify `get_logger` is usable from every module without circular imports

---

## Step 7: Report

```
============================================================
  PHASE {N} REVIEW COMPLETE
============================================================

  Specs reviewed:     {count} ({list})
  Total tests:        {count} passing
  Coverage:           {X}%
  
  Debug issues:       {X} found, {Y} fixed
  Dependency issues:  {X} found, {Y} fixed
  Optimizations:      {X} applied
  Security issues:    {X} found, {Y} fixed
  
  Files changed:      {list}
  
  Status: CLEAN / NEEDS ATTENTION
============================================================
```

If any CRITICAL issues remain unfixed, status is NEEDS ATTENTION with action items.

---

## Rules

1. Do NOT refactor architecture or add features -- this is review and hardening only
2. Do NOT change public APIs -- only internal improvements
3. All fixes must pass existing tests -- no regressions
4. Run `make check` after ALL changes to verify nothing broke
5. Keep changes minimal and focused -- this is a review, not a rewrite
