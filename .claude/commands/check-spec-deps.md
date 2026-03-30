---
description: Verify all prerequisite specs for a given spec are implemented and passing
argument-hint: spec-id (e.g., S4.1, S7.4)
allowed-tools: Read, Bash, Grep, Glob
---

Check whether all dependencies for spec $ARGUMENTS are satisfied.

## Step 1: Resolve Spec
Read `roadmap.md`, find spec row, extract Depends On column. If empty, report "No dependencies -- ready to implement" and stop.

## Step 2: For Each Dependency
- Check roadmap status (must be "done")
- Check code file exists (glob for Location)
- Check test file exists (glob tests/**/test_*.py)
- Run tests if they exist

## Step 3: Report

```
Dependency Check for {spec_id}
------------------------------
| Dep   | Status  | Code | Tests | Result    |
|-------|---------|------|-------|-----------|
| S1.3  | done    | OK   | OK 5/5| READY     |
| S2.4  | pending | OK   | FAIL  | BLOCKING  |
```

Final verdict: **READY** or **BLOCKED** (with which deps need work first).
