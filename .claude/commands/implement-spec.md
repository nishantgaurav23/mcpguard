---
description: Implement an MCPGuard spec following TDD and best practices
argument-hint: spec-id (e.g., S1.1, S4.2, S10.3)
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Implement spec: $ARGUMENTS

## Step 1: Load Spec Context
Read spec.md, checklist.md, roadmap.md row, CLAUDE.md rules.

## Step 2: Verify Prerequisites
Dependencies implemented, target files exist or can be created.

## Step 3: Follow TDD Strictly
**Red -> Green -> Refactor**
1. Write failing tests. Mock: LLM APIs, MCP server connections, Logfire, file system for baselines.
2. Implement minimal code to pass.
3. Refactor, re-run tests.

Update checklist.md progressively after each phase.

## Step 4: Implementation Rules

| Rule | Action |
|------|--------|
| Async | async def, await for MCP connections and LLM calls |
| Config | All secrets from .env, never hardcode |
| Models | Pydantic v2 for all in/out |
| Detectors | Extend BaseDetector ABC, register in DetectorRegistry |
| Errors | try/except on external calls, never crash the scan |
| Security | Sanitize server responses before LLM processing |
| Lint | ruff; run `make lint` before done |
| Types | mypy strict; run `make typecheck` before done |
| Immutability | Never mutate, always create new copies |
| Cost | LLM only for ambiguous findings, rule-based first |
| Baselines | 0600 permissions for ~/.mcpguard/ files |

## Step 5: Verification
All tests pass, lint clean, typecheck clean, all outcomes met.

## Step 6: Update Checklist & Roadmap
Finalize checklist.md (all items checked). Update roadmap.md status to `done` in both tables.
