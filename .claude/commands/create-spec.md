---
description: Create spec.md and checklist.md for an MCPGuard spec
argument-hint: spec-id [slug] or spec-id-slug (e.g., S1.1 dependency-declaration)
allowed-tools: Read, Write, Edit, Grep
---

Create spec documentation for: $ARGUMENTS

## Step 1: Resolve Spec Identity
Parse spec_id and slug from arguments. Read `roadmap.md` to get Spec Location, Feature, Location, Depends On, Notes.

## Step 2: Create spec.md and checklist.md
Create spec folder and write both files using templates:

**spec.md**: Overview, Dependencies, Target Location, Functional Requirements (FR-1, FR-2...), Tangible Outcomes, Test-Driven Requirements (tests to write first, mocking strategy for LLM APIs/MCP connections/Logfire).

**checklist.md**: Phase 1 (Setup), Phase 2 (Tests First/TDD), Phase 3 (Implementation), Phase 4 (Integration), Phase 5 (Verification).

## Step 3: Populate from Roadmap
Fill placeholders from roadmap data. Every FR maps to a test. Every outcome is testable.

## Step 4: Update Roadmap Status
Change status from `pending` to `spec-written` in **both** Phase table and Master Spec Index.

## Rules
1. Extract from roadmap -- do not invent
2. Every FR must map to at least one test
3. Spec folder path must match roadmap
4. Always update roadmap.md status to `spec-written`
5. Do NOT create `learning-log.md` during spec creation -- it is created automatically by learning commands (`/grillme`, `/learn-predict`, `/learn-mimic`, etc.) when they run against this spec
