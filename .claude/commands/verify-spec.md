---
description: Verify a spec is fully implemented -- tests, lint, outcomes, wiring
argument-hint: spec-id (e.g., S1.1, S4.2)
allowed-tools: Read, Bash, Grep, Glob
---

Verify that spec $ARGUMENTS is fully and correctly implemented.

## Step 1: Load Spec Context
Read spec.md (Tangible Outcomes, FRs), checklist.md, roadmap.md row.

## Step 2: Code Existence
Check all files in Target Location exist and have expected public functions/classes.

## Step 3: Test Suite
Find and run matching test files. Report total/passed/failed.

## Step 4: Lint and Type Check
Run ruff check and mypy on spec's target files only.

## Step 5: Tangible Outcomes Audit
For each outcome: check test exists, check implementation satisfies it. Mark PASS/FAIL/UNCLEAR.

## Step 6: Integration Check
- Detector: registered in DetectorRegistry (__init__.py)
- Agent: importable, correct output model
- CLI command: registered in Typer app
- MCP tool: registered in FastMCP server
- Formatter: usable via --format flag
- Config: fields exist in ScanConfig
- Evaluation: included in benchmark dataset

## Step 7: Report

```
Verification Report -- Spec {spec_id}: {feature}
----------------------------------------------------
Code files:      OK All present
Tests:           OK 8/8 passing
Lint:            OK Clean
Type Check:      OK Clean
Outcomes:        OK 3/3 verified
Integration:     OK Wired correctly
Checklist:       OK All items checked

VERDICT: PASS
```

If PASS: suggest updating roadmap.md status to `done`.
If FAIL: list what needs fixing, in priority order.
