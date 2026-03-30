---
description: Full spec lifecycle -- create, check deps, implement, and verify a spec in one go
argument-hint: spec-id [slug] (e.g., S1.1 dependency-declaration)
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Run the full spec development lifecycle for: $ARGUMENTS

## Execution Mode: Step-by-Step with Context Clearing

This command runs in step-by-step mode. Do NOT ask for permission between steps -- show results and continue automatically. Only stop if a step fails (blocked deps, test failures, etc.).

**Context clearing**: After Steps 1-2 (create + deps), run `/clear` to free up context. After Steps 3-4 (implement + verify), run `/clear` again.

---

## Phase A: Spec Setup (then /clear)

### Step 1: Create Spec
Run `/project:create-spec $ARGUMENTS`

### Step 2: Check Dependencies
Run `/project:check-spec-deps {spec_id}`
- If **BLOCKED**: Stop and report. Do NOT continue.
- If **READY**: Continue.

### After Phase A: Run `/clear`

---

## Phase B: Implementation (then /clear)

### Step 3: Implement Spec
Run `/project:implement-spec {spec_id}`

### Step 4: Verify Spec
Run `/project:verify-spec {spec_id}`

### After Phase B: Run `/clear`

---

## Step 5: Final Report

```
=== Spec {spec_id} -- Full Lifecycle Complete ===
1. Create Spec:    DONE -- specs/spec-{id}-{slug}/
2. Check Deps:     DONE -- all dependencies satisfied
3. Implement:      DONE -- all tests passing
4. Verify:         {PASS/FAIL} -- see verification report above

Roadmap status: done
```

## Rules
1. Parse spec_id from $ARGUMENTS (first arg, e.g., S1.1)
2. On any step failure, stop and report -- do not blindly continue
3. Always update checklist.md and roadmap.md as each sub-command requires
4. Do NOT ask for permission between steps -- only stop on failure
