# Reusable Prompts for Spec-Driven TDD Project Setup

Use these prompts with Claude Code to bootstrap any new project following the spec-driven development pattern.

---

## Prompt 1: Create Project Folder, Roadmap, and Full Setup

```
I have a project idea: [DESCRIBE YOUR PROJECT].

Create the complete project setup following the spec-driven pattern:
1. Create folder, requirements.md, design.md, roadmap.md, CLAUDE.md
2. Create .claude/commands/ with 5 spec-driven commands
3. Create .claude/settings.json with safe permissions
See scholargraph/prompts.md for full template.
```

## Prompt 2: Roadmap Only (Design and Requirements Already Exist)

```
Read design.md and requirements.md, create roadmap.md with spec-driven phases.
```

## Prompt 3: Add a New Feature (Spec-Driven)

```
Add [FEATURE] to the project. Update roadmap.md with new specs.
Run /project:start-spec-dev for each new spec.
```

## Prompt 4: Fix a Bug (Spec-Driven)

```
Bug: [DESCRIBE]. Write failing test, fix, verify with /project:verify-spec.
```

## Prompt 5: Project Health Check

```
Read roadmap.md, run make check, report specs done/pending, coverage, next spec to implement.
```
