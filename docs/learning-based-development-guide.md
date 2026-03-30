# Learning-Based Development Guide

A complete reference for using the Claude Code learning system to build skills while developing MCPGuard.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Setup Checklist](#setup-checklist)
3. [The 7 Learning Strategies](#the-7-learning-strategies)
4. [Continuous Learning Infrastructure](#continuous-learning-infrastructure)
5. [Instinct Commands Reference](#instinct-commands-reference)
6. [Daily Workflow](#daily-workflow)
7. [Weekly Review Workflow](#weekly-review-workflow)
8. [Learning-Mode Spec Development](#learning-mode-spec-development)
9. [Instinct Lifecycle](#instinct-lifecycle)
10. [Configuration Reference](#configuration-reference)
11. [Troubleshooting](#troubleshooting)
12. [External Resources](#external-resources)

---

## System Overview

The learning system has two layers:

**Layer 1: Interactive Learning Commands (Manual)**
Seven slash commands that transform Claude from "do it for me" to "teach me while we build." You invoke these deliberately when you want to learn.

**Layer 2: Continuous Learning Infrastructure (Automatic)**
Background hooks that observe every tool call, extract patterns into atomic "instincts," and evolve them into reusable skills/commands/agents over time.

```
                    YOU
                     |
        +------------+------------+
        |                         |
  Manual Learning           Automatic Learning
  (7 strategies)            (instinct system)
        |                         |
  /learn-predict            PreToolUse hook
  /learn-explain            PostToolUse hook
  /learn-debug                    |
  /learn-rebuild            observations.jsonl
  /learn-socratic                 |
  /learn-mimic              observer agent
  /learn-noai                     |
        |                   instincts (0.3-0.9)
        |                         |
        +------------+------------+
                     |
              /learn-eval
              /evolve
              /promote
                     |
              skills / commands / agents
```

---

## Setup Checklist

All steps have been completed. This section documents what was done for future reference.

### 1. Observation Hooks (in ~/.claude/settings.json)

Two hooks were added to capture tool call events:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [{
          "type": "command",
          "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh pre"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [{
          "type": "command",
          "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh post"
        }]
      }
    ]
  }
}
```

These fire on EVERY tool call (matcher: `*`), capturing:
- Tool name
- Tool input (truncated to 5000 chars)
- Tool output (truncated to 5000 chars)
- Session ID
- Project context (auto-detected via git remote)
- Timestamp

Secrets are automatically scrubbed before persisting.

### 2. Homunculus Directory Structure

Created at `~/.claude/homunculus/`:

```
~/.claude/homunculus/
  instincts/
    personal/           <- Global auto-learned instincts
    inherited/          <- Global imported instincts
  evolved/
    agents/             <- Global generated agents
    skills/             <- Global generated skills
    commands/           <- Global generated commands
  projects/
    <project-hash>/     <- Per-project (auto-created on first observation)
      project.json      <- Project metadata
      observations.jsonl
      observations.archive/
      instincts/
        personal/       <- Project-specific auto-learned
        inherited/      <- Project-specific imported
      evolved/
        skills/
        commands/
        agents/
```

### 3. Background Observer (in config.json)

Located at `~/.claude/skills/continuous-learning-v2/config.json`:

```json
{
  "version": "2.1",
  "observer": {
    "enabled": true,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20
  }
}
```

The observer:
- Runs every 5 minutes in the background (Haiku model)
- Waits until 20+ observations accumulate before first analysis
- Creates/updates instincts based on detected patterns
- Signals via SIGUSR1 every 20 tool calls

### 4. Project Detection

Automatic detection priority:
1. `CLAUDE_PROJECT_DIR` env var (highest priority)
2. `git remote get-url origin` -- hashed to 12-char ID (portable across machines)
3. `git rev-parse --show-toplevel` -- fallback using repo path
4. `global` -- if no project context detected

MCPGuard gets its own project scope automatically when you work in its directory.

---

## The 7 Learning Strategies

### Strategy 1: Predict First (`/learn-predict`)

**Purpose**: Design your approach BEFORE Claude implements. Builds architectural intuition.

**When to use**: Before starting any new spec or feature.

**How to invoke**:
```
/learn-predict S2.1 semantic-agent
/learn-predict implement the SSRF detector
/learn-predict design the SARIF output formatter
```

**Modes**:
- **A) Quick Prediction** -- for a single function/module. Claude asks "How would you approach this?", waits, then compares.
- **B) Architecture Review** -- for larger features. Claude asks 3 targeted questions about your approach, then critiques.
- **C) Critique My Plan** -- when you already have an idea. Claude challenges your assumptions and edge cases.

**MCPGuard examples**:
- Before building a new detector: `/learn-predict how would you detect command injection in MCP tool descriptions`
- Before designing the scan pipeline: `/learn-predict design a 4-layer detection pipeline`

---

### Strategy 2: Explain Decisions (`/learn-explain`)

**Purpose**: Understand WHY code was written the way it was. Closes the "copy-paste gap."

**When to use**: After Claude generates code you want to deeply understand.

**How to invoke**:
```
/learn-explain the semantic agent we just built
/learn-explain the PydanticAI structured output pattern
```

**Modes**:
- **A) Decision Debrief** -- Claude explains core problem, key decisions, alternatives rejected, gotchas, and mental model.
- **B) Trade-Off Surfacing** -- What this approach optimizes for, what it sacrifices, when a different approach would be better.

---

### Strategy 3: Debug Myself (`/learn-debug`)

**Purpose**: Build debugging intuition by solving bugs with guidance, not handouts.

**When to use**: When tests fail or you hit a bug.

**How to invoke**:
```
/learn-debug TypeError: 'NoneType' object has no attribute 'findings'
/learn-debug the SSRF detector is producing false positives on internal URLs
```

**Escalation ladder**:
1. Attempt 1: You describe what you think is wrong -- Claude says warmer/colder
2. Attempt 2: You try a fix -- Claude says if it's on track
3. Attempt 3 (stuck): Claude explains root cause, you implement the fix

**Post-mortem mode**: After fixing a bug, analyze root cause category, mental model gap, prevention rule, and the test you should have written.

---

### Strategy 4: Blind Rebuild (`/learn-rebuild`)

**Purpose**: Test whether you actually learned what was built, not just watched it happen.

**When to use**: After completing a spec (wait a day or two for best retention testing).

**How to invoke**:
```
/learn-rebuild the poisoning detector
/learn-rebuild the PydanticAI semantic agent
/learn-rebuild the Rich output formatter
```

**Modes**:
- **A) Rebuild Quiz** -- Claude gives you only function signatures. You implement from memory. Claude compares.
- **B) Simplification Challenge** -- Claude strips code to minimal ~20-30 line skeleton. You rebuild the full version.
- **C) Explain Without Looking** -- You explain components, interactions, data flow, edge cases from memory. Claude scores.

---

### Strategy 5: Socratic Tutor (`/learn-socratic`)

**Purpose**: Deep understanding through guided questioning. You remember answers you discovered.

**When to use**: Before implementing unfamiliar tech.

**How to invoke**:
```
/learn-socratic PydanticAI agents and structured outputs
/learn-socratic FastMCP server mode
/learn-socratic SARIF 2.1.0 format
/learn-socratic pydantic-evals evaluation framework
/learn-socratic Shannon entropy for secret detection
```

**Modes**:
- **A) Concept Prerequisites** -- Claude identifies 3-5 concepts, asks one question per concept. Waits for answers. Fills gaps only after you attempt.
- **B) Socratic Q&A** -- 5-8 rounds of questions to expose and fill understanding gaps.
- **C) Critique My Understanding** -- You explain a concept, Claude identifies what's right, what's wrong, and asks a hard question.

---

### Strategy 6: Scaffolded Independence (`/learn-mimic`)

**Purpose**: Graduate from "Claude writes everything" to "I write everything" through 3 phases.

**When to use**: During implementation. Choose the phase based on familiarity.

**How to invoke**:
```
/learn-mimic implement the credentials detector phase 1
/learn-mimic implement the unicode detector phase 2
/learn-mimic implement the auth detector phase 3
```

**Phases**:
- **Phase 1** (Full Code then Rewrite): Claude writes full code, lists 3 things you'll likely forget, tells you to rewrite from memory. Use when NEW to the pattern.
- **Phase 2** (Signatures + Hints): Claude gives only function signatures + one-line logic comments. You fill in all logic. Use when you've SEEN similar before.
- **Phase 3** (Pseudocode Only): Claude gives only pseudocode. You make every implementation decision. Use when CONFIDENT.

**Progression guide**:
- Phase 1: First time seeing PydanticAI, FastMCP, etc.
- Phase 2: Second detector, second formatter, etc.
- Phase 3: Third+ detector, confident on the pattern
- Skip all: You can implement without reference (graduated)

---

### Strategy 7: No-AI Zone (`/learn-noai`)

**Purpose**: Find where Claude has been carrying you, then build those skills independently.

**When to use**: Weekly (recommended: Friday or end of week).

**How to invoke**:
```
/learn-noai gaps                    # Identify blind spots
/learn-noai PydanticAI agents       # Self-study plan for specific topic
/learn-noai async Python patterns   # Retention check quiz
```

**Modes**:
- **A) Knowledge Gap Identification** -- Claude identifies 3 areas where it's been doing the heavy lifting. For each: the gap, evidence, one resource, one exercise, verification criteria.
- **B) Self-Study Spec** -- 1-week plan (Mon-Fri) with specific resources and exercises. NO AI assistance. Friday checkpoint question.
- **C) Retention Check** -- 5 rapid-fire questions. Score: 5/5 move on, 3-4/5 review gaps, 0-2/5 need self-study.

---

## Continuous Learning Infrastructure

### How Observations Flow

```
Every tool call in Claude Code
        |
        v
observe.sh fires (PreToolUse + PostToolUse)
        |
        v
Extracts: tool name, input, output, session, project context
Scrubs: secrets (API keys, tokens, passwords)
Truncates: input/output to 5000 chars
        |
        v
Appends to: ~/.claude/homunculus/projects/<hash>/observations.jsonl
        |
        v (every 20 observations, SIGUSR1 signal)
Background observer agent (Haiku) analyzes patterns
        |
        v
Creates/updates instincts in: projects/<hash>/instincts/personal/
```

### What Is an Instinct?

An instinct is a small, atomic learned behavior:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "mcpguard"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach on 2025-01-15
```

**Properties**:
- **Atomic**: one trigger, one action
- **Confidence-weighted**: 0.3 = tentative, 0.5 = moderate, 0.7 = strong, 0.9 = near-certain
- **Domain-tagged**: code-style, testing, git, debugging, workflow, security, etc.
- **Evidence-backed**: tracks observations that created it
- **Scope-aware**: project (default) or global

### Confidence Scoring

| Score | Meaning | Behavior |
|-------|---------|----------|
| 0.3 | Tentative | Suggested but not enforced |
| 0.5 | Moderate | Applied when relevant |
| 0.7 | Strong | Auto-approved for application |
| 0.9 | Near-certain | Core behavior |

**Confidence increases** when:
- Pattern is repeatedly observed
- User doesn't correct the suggested behavior
- Similar instincts from other sources agree

**Confidence decreases** when:
- User explicitly corrects the behavior
- Pattern isn't observed for extended periods
- Contradicting evidence appears

### Scope Decision Guide

| Pattern Type | Scope | Examples |
|-------------|-------|---------|
| Language/framework conventions | **project** | "Use PydanticAI for LLM calls", "BaseDetector ABC pattern" |
| File structure preferences | **project** | "Tests in tests/test_detectors/", "Models in models/" |
| Code style | **project** | "Immutable Pydantic models", "Async everywhere" |
| Error handling strategies | **project** | "try/except wraps all external calls" |
| Security practices | **global** | "Validate user input", "Sanitize SQL" |
| General best practices | **global** | "Write tests first", "Always handle errors" |
| Tool workflow preferences | **global** | "Grep before Edit", "Read before Write" |
| Git practices | **global** | "Conventional commits", "Small focused commits" |

---

## Instinct Commands Reference

### `/instinct-status` -- View Learned Instincts

Shows all instincts (project-scoped + global) grouped by domain with confidence bars.

```
/instinct-status
```

**Output example**:
```
============================================================
  INSTINCT STATUS - 12 total
============================================================

  Project: mcpguard (a1b2c3d4e5f6)
  Project instincts: 8
  Global instincts:  4

## PROJECT-SCOPED (mcpguard)
  ### WORKFLOW (3)
    |||||||...  70%  grep-before-edit [project]
              trigger: when modifying code

## GLOBAL (apply to all projects)
  ### SECURITY (2)
    |||||||||.  85%  validate-user-input [global]
              trigger: when handling user input
```

**When to run**: After 2-3 working sessions (need observations to accumulate first).

---

### `/evolve` -- Cluster Instincts into Skills/Commands/Agents

Analyzes instincts and clusters related ones into higher-level structures.

```
/evolve                    # Analyze and suggest evolutions
/evolve --generate         # Also generate files
```

**Evolution rules**:
- **To Command** (user-invoked): When instincts describe repeatable action sequences
- **To Skill** (auto-triggered): When instincts describe behaviors that should happen automatically
- **To Agent** (needs depth): When instincts describe complex multi-step processes

**When to run**: Weekly, after enough instincts accumulate.

---

### `/promote` -- Project to Global

Promotes instincts from project scope to global scope when they apply everywhere.

```
/promote                          # Auto-detect promotion candidates
/promote --dry-run                # Preview without changes
/promote --force                  # Promote all qualified without prompt
/promote grep-before-edit         # Promote one specific instinct
```

**Auto-promotion criteria**:
- Same instinct ID appears in 2+ projects
- Average confidence >= 0.8

**When to run**: When you notice patterns that apply across all your projects.

---

### `/instinct-export` -- Share Instincts

Exports instincts to a shareable YAML file.

```
/instinct-export                           # Export all
/instinct-export --domain testing          # Export only testing instincts
/instinct-export --min-confidence 0.7      # Only high-confidence
/instinct-export --scope project           # Current project only
/instinct-export --output my-instincts.yaml
```

---

### `/instinct-import` -- Import Instincts

Imports instincts from a file or URL.

```
/instinct-import team-instincts.yaml
/instinct-import https://example.com/instincts.yaml
/instinct-import team-instincts.yaml --dry-run
/instinct-import team-instincts.yaml --scope global --force
/instinct-import team-instincts.yaml --min-confidence 0.7
```

**Merge behavior**: Higher-confidence import updates existing; equal/lower is skipped. Imported instincts are marked with `source: inherited`.

---

### `/projects` -- List Projects

Shows all tracked projects with instinct and observation counts.

```
/projects
```

---

### `/learn-eval` -- Manual Pattern Extraction

Manually extract reusable patterns mid-session with quality gate.

```
/learn-eval
```

**Process**:
1. Reviews session for extractable patterns
2. Determines save location (Global vs Project)
3. Drafts skill file with frontmatter
4. Runs quality gate (overlap check, reusability check)
5. Verdict: Save / Improve then Save / Absorb into existing / Drop
6. Saves after confirmation

---

### `/learn` -- Quick Pattern Extraction

Simpler version of `/learn-eval` without the quality gate.

```
/learn
```

Saves patterns to `~/.claude/skills/learned/`.

---

## Daily Workflow

### Before Starting a New Spec or Feature

```
Step 1: /learn-socratic <unfamiliar concept>
        Example: /learn-socratic PydanticAI structured outputs

Step 2: /learn-predict <spec description>
        Example: /learn-predict S2.1 design the semantic analysis agent

Step 3: Choose scaffolding level:
        /learn-mimic <task> phase 1   (new pattern)
        /learn-mimic <task> phase 2   (seen similar before)
        /learn-mimic <task> phase 3   (confident)
```

### After Implementation

```
Step 4: /learn-explain
        Understand the key decisions in what was just built

Step 5: /learn-eval
        Extract any reusable patterns from the session
```

### When You Hit a Bug

```
/learn-debug <error message or description>
        Get hints, not fixes. Escalate only when truly stuck.
```

### Full Learning-Mode Spec (All-in-One)

```
/learn-spec S2.1 semantic-agent
```

This combines all strategies into a single workflow (takes 2-3x longer but you learn deeply).

---

## Weekly Review Workflow

### Friday Routine (30-60 min)

```
Step 1: /instinct-status
        Review what the system has learned about your patterns

Step 2: /learn-noai gaps
        Identify your 3 biggest blind spots

Step 3: /evolve
        Cluster instincts into reusable skills

Step 4: /promote (if working on multiple projects)
        Promote universal patterns to global scope

Step 5: /learn-noai <weakest area>
        Generate a self-study plan for the week ahead
```

### Monthly Review

```
Step 1: /projects
        See all tracked projects and their instinct counts

Step 2: /instinct-export --min-confidence 0.8 --output monthly-review.yaml
        Export high-confidence instincts for review

Step 3: /evolve --generate
        Generate evolved skills/commands/agents from mature instincts
```

---

## Learning-Mode Spec Development

Use `/learn-spec` instead of `/start-spec-dev` when you want to learn, not just ship.

### The Full Lifecycle

```
/learn-spec S1.1 dependency-declaration
```

**Phase A: Understand Before Building**
1. Socratic Concept Check (Strategy 5) -- 3-5 concept questions
2. Predict First (Strategy 1) -- design your approach

**Phase B: Create Spec**
3. Creates spec.md + checklist.md (standard process)
4. Checks dependencies (standard process)

**Phase C: Learn While Building**
5. Choose Mimicking Phase (Strategy 6) -- Phase 1, 2, or 3
6. Explain Decisions (Strategy 2) -- understand the key choices

**Phase D: Verify and Retain**
7. Verify Spec (standard process)
8. Retention Quiz (Strategy 4) -- 3 questions from memory

**Phase E: Post-Mortem**
9. Learning Report with scores

**Time**: Takes 2-3x longer than normal spec development. That is the point.

---

## Instinct Lifecycle

```
Stage 1: OBSERVATION
  Tool calls captured by hooks -> observations.jsonl
  (automatic, every tool call)

Stage 2: DETECTION
  Observer agent reads observations (every 5 min)
  Identifies: user corrections, error resolutions, repeated workflows
  Creates instincts at confidence 0.3

Stage 3: REINFORCEMENT
  Same pattern observed again -> confidence increases
  User corrects behavior -> confidence decreases
  No observation for extended period -> confidence decays

Stage 4: MATURITY
  Instinct reaches confidence 0.7+ -> strong behavior
  Appears in 2+ projects -> promotion candidate

Stage 5: EVOLUTION
  /evolve clusters related instincts:
    2-3 instincts -> Skill (auto-triggered)
    3-5 instincts -> Command (user-invoked)
    5+ instincts -> Agent (complex multi-step)

Stage 6: PROMOTION
  /promote moves universal instincts from project -> global scope
```

---

## Configuration Reference

### ~/.claude/settings.json (Hooks)

| Hook | Matcher | Purpose |
|------|---------|---------|
| PreToolUse | `*` | Capture tool start events for observation |
| PostToolUse | `*` | Capture tool completion events for observation |

### ~/.claude/skills/continuous-learning-v2/config.json

| Key | Default | Description |
|-----|---------|-------------|
| `observer.enabled` | `true` | Enable background observer agent |
| `observer.run_interval_minutes` | `5` | How often observer analyzes observations |
| `observer.min_observations_to_analyze` | `20` | Minimum observations before first analysis |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLAUDE_PROJECT_DIR` | Override project detection |
| `CLV2_PYTHON_CMD` | Override Python interpreter |
| `CLV2_CONFIG` | Override config.json path |
| `ECC_SKIP_OBSERVE` | Set to `1` to skip observation |
| `ECC_OBSERVER_SIGNAL_EVERY_N` | Throttle observer signals (default: 20) |

### File Size Management

- Observations auto-archive at 10MB per file
- Archived observations auto-purge after 30 days
- Secrets are scrubbed before persisting

---

## Troubleshooting

### No instincts appearing after several sessions

1. Check hooks are registered: `grep observe ~/.claude/settings.json`
2. Check observations are being written: `ls -la ~/.claude/homunculus/projects/`
3. Check observer is enabled: `cat ~/.claude/skills/continuous-learning-v2/config.json`
4. Check observe.sh is executable: `ls -la ~/.claude/skills/continuous-learning-v2/hooks/observe.sh`
5. Check Python is available: `python3 --version`

### Observer not starting

1. Check config: `observer.enabled` must be `true`
2. Check PID file: `ls ~/.claude/homunculus/projects/*/.observer.pid`
3. Check for stale PID: the hook auto-cleans stale PIDs

### Observations file growing too large

The system auto-archives at 10MB and auto-purges archives after 30 days. No manual intervention needed.

### Hooks slowing down Claude Code

The observe.sh script is lightweight (pure shell + Python one-liners). If you notice slowdowns:
- Check `ECC_OBSERVER_SIGNAL_EVERY_N` -- increase to reduce signaling frequency
- The observer only analyzes every 5 minutes, not on every tool call

### Disable temporarily

```bash
touch ~/.claude/homunculus/disabled    # Disables all observation
rm ~/.claude/homunculus/disabled       # Re-enables
```

---

## External Resources

### MCPGuard Tech Stack

| Technology | Documentation |
|------------|--------------|
| PydanticAI | https://ai.pydantic.dev/ |
| PydanticAI Agents | https://ai.pydantic.dev/agents/ |
| PydanticAI Tools | https://ai.pydantic.dev/tools/ |
| PydanticAI Evals | https://ai.pydantic.dev/evals/ |
| FastMCP | https://github.com/jlowin/fastmcp |
| MCP Protocol | https://modelcontextprotocol.io/ |
| MCP Security | https://modelcontextprotocol.io/specification/2025-03-26/security |
| Pydantic v2 | https://docs.pydantic.dev/latest/ |
| SARIF 2.1.0 | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html |
| GitHub SARIF | https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning |
| Typer | https://typer.tiangolo.com/ |
| Rich | https://rich.readthedocs.io/en/latest/ |
| pytest | https://docs.pytest.org/en/stable/ |
| pytest-asyncio | https://pytest-asyncio.readthedocs.io/en/latest/ |
| Hatchling | https://hatch.pypa.io/latest/ |
| PyPI Trusted Publishers | https://docs.pypi.org/trusted-publishers/ |

### MCP Security Research

| Resource | Link |
|----------|------|
| OWASP ML Security Top 10 | https://owasp.org/www-project-machine-learning-security-top-10/ |
| CyberArk Tool Poisoning | https://www.cyberark.com/resources/threat-research-blog/mcp-prompt-injection |
| Invariant Labs MCP Scanner | https://github.com/invariantlabs-ai/mcp-scan |
| Trail of Bits MCP Analysis | https://blog.trailofbits.com/ |

### Learning System References

| Resource | Link |
|----------|------|
| ECC Longform Guide (continuous learning section) | https://x.com/affaanmustafa/status/2014040193557471352 |
| Skill Creator (generate instincts from repo history) | https://skill-creator.app |
| Homunculus (inspired instinct architecture) | Community project referenced in ECC |

### Python Deep Learning Resources

| Topic | Resource |
|-------|----------|
| Async Python | https://docs.python.org/3/library/asyncio.html |
| Type Hints | https://docs.python.org/3/library/typing.html |
| ABC Pattern | https://docs.python.org/3/library/abc.html |
| hashlib | https://docs.python.org/3/library/hashlib.html |
| Shannon Entropy | https://en.wikipedia.org/wiki/Entropy_(information_theory) |

---

## Grill Me (Assessment Gate)

The `/grillme` command puts Claude in senior-engineer-interviewer mode. No code gets written until you prove you understand the problem, the design, and the implementation plan.

### Usage

```
/grillme implement the SSRF detector
/grillme easy PydanticAI agent basics
/grillme hard design the 4-layer detection pipeline
/grillme brutal the scan orchestration engine
```

### How It Works

**Phase 1: Problem Understanding (3-5 questions)**
- What are we solving? Who's affected? What does success look like?
- Constraints? Blast radius of a bug?

**Phase 2: Design Interrogation (3-5 questions)**
- Architecture? Data flow? Edge cases?
- Failure modes? Alternatives considered?

**Phase 3: Implementation Readiness (3-5 questions)**
- Dependencies checked? Testing strategy? Integration points?
- Risk assessment? Definition of done?

**Phase 4: Verdict**
- READY (12+ SOLID): Proceed to implementation
- ALMOST (8-11 SOLID): Address specific gaps first
- NOT READY (< 8 SOLID): Study and re-grill

### Difficulty Modes

| Mode | Flag | Style |
|------|------|-------|
| Easy | `/grillme easy <task>` | Simpler questions, forgiving scoring |
| Standard | `/grillme <task>` | Senior engineer interview |
| Hard | `/grillme hard <task>` | Adversarial, challenges assumptions |
| Brutal | `/grillme brutal <task>` | Principal engineer, every answer gets a follow-up |

### When to Use

- Before any spec implementation (pairs well with `/learn-predict`)
- When you're unsure if you understand a problem well enough
- As a self-assessment before writing code without Claude
- When returning to a spec after time away

---

## Quick Reference Card

```
BEFORE building something new:
  /grillme <task>               -- Prove you understand before coding
  /learn-socratic <concept>     -- Learn underlying concepts first
  /learn-predict <task>         -- Design your approach before Claude

DURING implementation:
  /learn-mimic <task> phase N   -- Scaffolded independence (1/2/3)
  /learn-debug <error>          -- Get hints, not fixes

AFTER implementation:
  /learn-explain                -- Understand WHY decisions were made
  /learn-rebuild <module>       -- Test retention from memory
  /learn-eval                   -- Extract reusable patterns

ALL-IN-ONE:
  /learn-spec <spec-id> <slug>  -- Full learning-mode spec development

WEEKLY:
  /instinct-status              -- What has the system learned?
  /learn-noai gaps              -- Where is Claude carrying me?
  /evolve                       -- Cluster instincts into skills
  /promote                      -- Move universal patterns to global

MAINTENANCE:
  /projects                     -- List all tracked projects
  /instinct-export              -- Share instincts
  /instinct-import <file>       -- Import instincts from others
```
