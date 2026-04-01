# Roadmap -- MCPGuard: AI-Powered MCP Security Auditor

**Prototype target**: End-to-end MCP security scanning -- 4-layer detection pipeline, PydanticAI semantic analysis, CLI with Rich streaming, MCP server mode, SARIF output, self-evaluation benchmark with F1 metrics.
**Budget**: $0-20 total. Free-tier LLM APIs (Gemini Flash + Groq). 80%+ detection is zero-cost rule-based.
**LLMs**: Gemini 2.5 Flash (free: 1,000 RPD) primary + Groq Llama 3.3 70B (free: 14,400 RPD) fallback.
**Out of scope for prototype**: Web dashboard, real-time monitoring, enterprise multi-tenant mode.

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Language | Python 3.10+ | PydanticAI/FastMCP ecosystem, broad OS support |
| Agent Framework | PydanticAI v1.70+ | Type-safe structured outputs; native MCP client/server |
| MCP Server | FastMCP (via PydanticAI) | Standard MCP framework; decorator-based |
| CLI | Typer | Type-hint CLI; Pydantic ecosystem alignment |
| Terminal Output | Rich | Tables, progress bars, streaming, severity colors |
| LLM (primary) | Gemini 2.5 Flash (free) | 1,000 RPD free; cheapest semantic analysis |
| LLM (fallback) | Groq Llama 3.3 70B (free) | 14,400 RPD free; fast inference |
| Evaluation | pydantic-evals | PydanticAI-native; Dataset/Case/Evaluator |
| Observability | Pydantic Logfire | OTel-native; 10M spans/month free |
| Hashing | hashlib (stdlib) | SHA-256 tool pinning; zero dependencies |
| HTTP Client | httpx | Async HTTP; PydanticAI dependency |
| Testing | pytest + pytest-asyncio | Standard Python async testing |
| Linting | ruff | Fast, opinionated |
| Type Checking | mypy (strict) | Catch type errors before runtime |
| CI/CD | GitHub Actions | Free; SARIF upload support |
| Packaging | Hatchling + PyPI Trusted Publishers | Zero-token OIDC publishing |

---

## Budget

| Resource | Tier | Est. Cost |
|----------|------|-----------|
| Gemini 2.5 Flash | Free tier (1,000 RPD) | $0 |
| Groq Llama 3.3 70B | Free tier (14,400 RPD) | $0 |
| Gemini Flash paid overflow | $0.15/M tokens | $0-3 |
| Pydantic Logfire | Free tier (10M spans/month) | $0 |
| GitHub Actions | Free (public repo) | $0 |
| PyPI | Free | $0 |
| **Total** | | **~$3 of $20 budget** |

---

## Spec Folder Convention

Each spec has a dedicated folder under `specs/`:

```
specs/
  spec-S1.1-dependency-declaration/
    spec.md        <- detailed specification
    checklist.md   <- implementation checklist / progress tracker
  spec-S1.2-developer-commands/
    spec.md
    checklist.md
  ...
```

---

## Phases Overview

| Phase | Name | Specs | Key Output |
|-------|------|-------|------------|
| 1 | Project Foundation | 5 | Runnable skeleton, config, Makefile, linting, packaging |
| 2 | Data Models and Contracts | 4 | Pydantic schemas for findings, reports, config, semantic analysis |
| 3 | Detection Rules and Patterns | 3 | Regex patterns, OWASP mapping, CVSS scoring |
| 4 | Static Detectors (Layer 1+2) | 7 | Poisoning, unicode, credentials, full-schema, SSRF, command injection, base detector |
| 5 | Integrity and Auth Detectors (Layer 4+) | 4 | Rug pull, auth compliance, transport security, cross-server shadowing |
| 6 | PydanticAI Agents (Layer 3) | 3 | Semantic analyzer, report generator, scan orchestrator |
| 7 | CLI Interface | 4 | Typer commands, Rich streaming, config auto-discovery, exit codes |
| 8 | Output Formatters | 3 | Rich tables, JSON output, SARIF 2.1.0 |
| 9 | MCP Server Mode | 3 | FastMCP server, tools, resources/prompts |
| 10 | Evaluation Framework | 4 | Benchmark dataset, vulnerable test fixtures, eval runner, CI gate |
| 11 | Observability | 2 | Logfire integration, cost tracking |
| 12 | Infrastructure and Deployment | 4 | GitHub Actions CI/CD, PyPI publish, MCP registry, documentation |

---

## Phase 1 -- Project Foundation

Bootstraps the project: dependency declaration, environment config, Makefile, packaging setup.
Output: `make check` runs lint + type-check + test -- all green.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S1.1 | `specs/spec-S1.1-dependency-declaration/` | -- | `pyproject.toml`, `.env.example` | Dependency declaration | Runtime: pydantic-ai[mcp], typer, rich, httpx, logfire. Dev: pytest, pytest-asyncio, pytest-cov, ruff, mypy. Entry point: mcpguard CLI. Hatchling build backend | done |
| S1.2 | `specs/spec-S1.2-developer-commands/` | -- | `Makefile` | Developer commands | Targets: venv, install, install-dev, check, test, lint, typecheck, format, eval, serve, scan | done |
| S1.3 | `specs/spec-S1.3-config/` | S1.1 | `src/mcpguard/models/config.py` | ScanConfig + settings | ScanConfig dataclass: target, severity_threshold, enable_llm, enable_auth_check, baseline_path, findings, llm_calls. Environment: GEMINI_API_KEY, GROQ_API_KEY, LOGFIRE_TOKEN. All from .env | done |
| S1.4 | `specs/spec-S1.4-package-init/` | S1.1 | `src/mcpguard/__init__.py` | Package initialization | __version__, package metadata. Verify `python -m mcpguard` works | done |
| S1.5 | `specs/spec-S1.5-logging-setup/` | S1.3 | `src/mcpguard/utils/logging.py` | Structured logging | Logfire or structlog setup. LOG_LEVEL from env. Span context for scan tracing | pending |

---

## Phase 2 -- Data Models and Contracts

All Pydantic schemas for findings, reports, and semantic analysis. Defined before any implementation.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S2.1 | `specs/spec-S2.1-finding-models/` | S1.1 | `src/mcpguard/models/findings.py` | VulnerabilityFinding + ServerAuditReport | VulnerabilityFinding (rule_id, severity, cvss_score, title, description, affected_tool, evidence, remediation, owasp_mapping, detector). ServerAuditReport (server_name, version, scan_timestamp, overall_risk_score, risk_level, findings, finding_counts, tool_count, resource_count, auth_status, transport, transport_secure, tool_hashes, scan_duration_ms, llm_calls_made, estimated_cost_usd) | pending |
| S2.2 | `specs/spec-S2.2-semantic-models/` | S1.1 | `src/mcpguard/models/semantic.py` | SemanticAnalysis model | SemanticAnalysis (verdict: safe/suspicious/malicious, confidence: 0.0-1.0, reasoning: str, suggested_severity: Literal or None). Used by PydanticAI semantic agent output | pending |
| S2.3 | `specs/spec-S2.3-tool-definition-model/` | S1.1 | `src/mcpguard/models/tool_def.py` | ToolDefinition model | ToolDefinition (name, description, parameters_json_schema). ServerInventory (tools, resources, prompts, server_info, capabilities). Consistent representation of MCP introspection results | pending |
| S2.4 | `specs/spec-S2.4-scan-events/` | S1.1 | `src/mcpguard/models/events.py` | Streaming event models | ConnectionEvent, ToolScanEvent, FindingEvent, LLMCallEvent, ScanCompleteEvent. For real-time CLI streaming via Rich | pending |

---

## Phase 3 -- Detection Rules and Patterns

Rule databases, OWASP mapping, and risk scoring.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S3.1 | `specs/spec-S3.1-regex-patterns/` | S1.1 | `src/mcpguard/rules/patterns.py` | All regex patterns | DIRECTIVE_PATTERNS (~30 poisoning patterns), SECRET_PATTERNS (25+ credential regexes from TruffleHog/Gitleaks), SSRF_PARAM_NAMES (~15 keywords), INJECTION_PATTERNS (~20 patterns), UNICODE_CODEPOINTS (~10 ranges), SUSPICIOUS_PARAM_NAME_PATTERNS | pending |
| S3.2 | `specs/spec-S3.2-owasp-mapping/` | S1.1 | `src/mcpguard/rules/owasp_mapping.py` | OWASP MCP Top 10 mapping | Map each rule_id to OWASP MCP category. MCP-01 through MCP-10. Include CWE references where applicable | pending |
| S3.3 | `specs/spec-S3.3-cvss-scoring/` | S2.1 | `src/mcpguard/rules/cvss.py` | Risk scoring logic | Calculate overall_risk_score (0-10) from findings. Severity weights: critical=10, high=7, medium=4, low=1. Risk level mapping. CVSS-aligned per-finding scoring | pending |

---

## Phase 4 -- Static Detectors (Layer 1 + Layer 2)

Zero-cost rule-based and heuristic detectors.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S4.1 | `specs/spec-S4.1-base-detector/` | S2.1, S2.3 | `src/mcpguard/detectors/base.py`, `src/mcpguard/detectors/__init__.py` | BaseDetector ABC + registry | Abstract base class: scan(tool: ToolDefinition) -> list[Finding]. DetectorRegistry: register, get_all, run_all. Detector metadata: name, layer, cost | pending |
| S4.2 | `specs/spec-S4.2-poisoning-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/poisoning.py` | Tool description poisoning detector | Layer 1. Scan description field for DIRECTIVE_PATTERNS. Detect directive tags, file exfiltration, cross-tool manipulation, attacker URLs. Returns Finding or Ambiguous | pending |
| S4.3 | `specs/spec-S4.3-unicode-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/unicode.py` | Unicode steganography detector | Layer 1. Scan all text fields for invisible codepoints: U+200B, U+200C, U+200D, U+200E, U+FEFF, etc. Report position and count | pending |
| S4.4 | `specs/spec-S4.4-credential-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/credentials.py` | Credential/secret detector | Layer 1. Scan descriptions, defaults, examples, enum values for SECRET_PATTERNS. 25+ secret types: AWS, GitHub, Slack, Stripe, PEM, JWT, generic API keys | pending |
| S4.5 | `specs/spec-S4.5-full-schema-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/full_schema.py` | CyberArk-style full-schema detector | Layer 2. Scan ALL schema fields: parameter name entropy, parameter name keywords, default value analysis, enum value inspection. Shannon entropy > 4.5 threshold | pending |
| S4.6 | `specs/spec-S4.6-ssrf-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/ssrf.py` | SSRF risk detector | Layer 2. Identify parameters accepting arbitrary URLs. Match SSRF_PARAM_NAMES. Check for missing type/format constraints. Flag unrestricted string URL inputs | pending |
| S4.7 | `specs/spec-S4.7-command-injection-detector/` | S4.1, S3.1 | `src/mcpguard/detectors/command_injection.py` | Command injection detector | Layer 2. Detect shell references in descriptions (os.system, subprocess, exec, eval). Flag suspicious param names (cmd, exec, command, payload). Check defaults for shell metacharacters | pending |

---

## Phase 5 -- Integrity and Auth Detectors (Layer 4+)

Hash verification, authentication compliance, transport security, cross-server analysis.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S5.1 | `specs/spec-S5.1-rug-pull-detector/` | S4.1, S2.3 | `src/mcpguard/detectors/rug_pull.py`, `src/mcpguard/utils/hashing.py` | Rug pull detector + hash pinning | Layer 4. SHA-256 hash of canonical tool definition (name + description + schema). Store in ~/.mcpguard/baselines.json. Compare on subsequent scans. Mismatch = rug pull finding. First scan = record baseline | pending |
| S5.2 | `specs/spec-S5.2-auth-detector/` | S4.1 | `src/mcpguard/detectors/auth.py` | OAuth 2.1 compliance detector | HTTP-transport only. Probe /.well-known/oauth-protected-resource, /.well-known/oauth-authorization-server. Verify PKCE (S256). Check 401 + WWW-Authenticate header. Classify: oauth, api_key, none, unknown | pending |
| S5.3 | `specs/spec-S5.3-transport-detector/` | S4.1 | `src/mcpguard/detectors/transport.py` | Transport security detector | HTTP: verify HTTPS, Origin header, rate limit headers, session ID quality. Stdio: verify no 0.0.0.0 binding | pending |
| S5.4 | `specs/spec-S5.4-shadowing-detector/` | S4.1, S4.2 | `src/mcpguard/detectors/shadowing.py` | Cross-server shadowing detector | Multi-server config scans. Analyze tool descriptions across servers for cross-references. Detect server A's descriptions injecting instructions targeting server B's tools | pending |

---

## Phase 6 -- PydanticAI Agents (Layer 3)

Intelligent semantic analysis and report generation.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S6.1 | `specs/spec-S6.1-semantic-agent/` | S2.2, S1.3 | `src/mcpguard/agents/semantic_agent.py` | PydanticAI semantic analyzer | Agent with Gemini 2.5 Flash. Output: SemanticAnalysis. Analyzes ambiguous findings only. Determines if content is legitimate description or disguised instruction. retries=2. Fallback to Groq | pending |
| S6.2 | `specs/spec-S6.2-report-agent/` | S2.1, S3.3, S1.3 | `src/mcpguard/agents/report_agent.py` | PydanticAI report generator | Agent with Gemini 2.5 Flash. Output: ServerAuditReport. Synthesizes all findings into structured report. Risk score, OWASP mapping, remediation. retries=2 | pending |
| S6.3 | `specs/spec-S6.3-scan-orchestrator/` | S6.1, S6.2, S4.1, S5.1 | `src/mcpguard/scanner.py` | Main scan orchestration | run_scan(config) -> ServerAuditReport. Connect to target MCP server. Enumerate tools/resources. Run all detectors per tool (Layer 1 -> 2 -> 3 -> 4). Generate report. Stream events. Async generator pattern | pending |

---

## Phase 7 -- CLI Interface

Typer-based CLI with Rich streaming output.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S7.1 | `specs/spec-S7.1-cli-skeleton/` | S1.1 | `src/mcpguard/cli.py` | Typer CLI entry point | Subcommands: scan, baseline, eval, serve, rules. Global options: --format (rich/json/sarif), --severity-threshold, --timeout, --no-llm. Version flag | pending |
| S7.2 | `specs/spec-S7.2-scan-command/` | S7.1, S6.3 | `src/mcpguard/cli.py` | scan subcommand | `mcpguard scan <config-path>`, `--url <server-url>`, `--cmd "<command>"`. Invoke scanner, stream findings via Rich, apply severity threshold, set exit code | pending |
| S7.3 | `specs/spec-S7.3-config-discovery/` | S7.1 | `src/mcpguard/utils/config_loader.py` | Config file auto-discovery + parsing | Auto-detect: ~/.config/claude/claude_desktop_config.json, .cursor/mcp.json, .vscode/mcp.json, mcp.json. Parse mcpServers entries. Support stdio + HTTP transports | pending |
| S7.4 | `specs/spec-S7.4-other-commands/` | S7.1, S5.1 | `src/mcpguard/cli.py` | baseline + eval + serve + rules commands | baseline: create/update hash baselines. eval: run pydantic-evals benchmark. serve: start MCP server mode. rules: list all detection rules with IDs and descriptions | pending |

---

## Phase 8 -- Output Formatters

Multiple output formats for different use cases.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S8.1 | `specs/spec-S8.1-rich-formatter/` | S2.1, S2.4 | `src/mcpguard/formatters/rich_output.py` | Rich terminal rendering | Severity-colored findings table. Real-time streaming with Progress spinner. Summary Panel with risk score, finding counts, pass/fail verdict. SEVERITY_COLORS map | pending |
| S8.2 | `specs/spec-S8.2-json-formatter/` | S2.1 | `src/mcpguard/formatters/json_output.py` | JSON formatter | Machine-readable JSON. Full finding details, evidence, remediation, OWASP mappings. ServerAuditReport.model_dump_json() | pending |
| S8.3 | `specs/spec-S8.3-sarif-formatter/` | S2.1, S3.2 | `src/mcpguard/formatters/sarif.py` | SARIF 2.1.0 generator | OASIS-standard format. Compatible with github/codeql-action/upload-sarif@v3. Each rule maps to rules[] entry with CWE/OWASP tags. Artifact locations as mcp:// URIs | pending |

---

## Phase 9 -- MCP Server Mode

MCPGuard itself as an MCP server for IDE integration.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S9.1 | `specs/spec-S9.1-mcp-server-tools/` | S6.3 | `src/mcpguard/mcp_server.py` | FastMCP server with tools | scan_server (stdio), scan_http_server (HTTP), check_tool_description (single tool, no connection), list_rules. Structured JSON responses | pending |
| S9.2 | `specs/spec-S9.2-mcp-resources-prompts/` | S9.1 | `src/mcpguard/mcp_server.py` | MCP resources + prompts | Resources: mcpguard://rules, mcpguard://latest-report, mcpguard://baseline/{server_name}. Prompt: security_review_prompt (guided comprehensive review) | pending |
| S9.3 | `specs/spec-S9.3-ide-config/` | S9.1 | -- | Claude Desktop / Cursor config | JSON config for mcpServers. Document uvx-based installation. Verify stdio transport works with Claude Desktop. Test with Cursor | pending |

---

## Phase 10 -- Evaluation Framework

Self-evaluation benchmark with precision/recall/F1.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S10.1 | `specs/spec-S10.1-benchmark-dataset/` | S2.1, S2.3 | `evaluation/benchmark.yaml` | pydantic-evals benchmark | 50+ labeled cases: 25+ benign (expect clean), 25+ malicious (tool poisoning, credentials, SSRF, injection, unicode, schema poisoning, cross-tool). Evaluators: Contains, MaxDuration | pending |
| S10.2 | `specs/spec-S10.2-test-fixtures/` | S1.1 | `evaluation/fixtures/clean_server.py`, `evaluation/fixtures/poisoned_server.py`, etc. | Vulnerable FastMCP test servers | 7+ fixtures: clean, poisoned, credential_leak, ssrf, injection, unicode, no_auth. Each is a minimal FastMCP server with intentional vulnerability. Used in pytest | pending |
| S10.3 | `specs/spec-S10.3-eval-runner/` | S10.1, S6.3 | `evaluation/run_eval.py` | Benchmark runner | Run MCPGuard against benchmark dataset. Compute per-category precision/recall/F1. Rich terminal table output. JSON export. Logfire dashboard integration | pending |
| S10.4 | `specs/spec-S10.4-eval-ci-gate/` | S10.3 | `.github/workflows/eval.yml` | CI evaluation gate | Weekly benchmark run in GitHub Actions. Fail if overall F1 < 0.85. Post results as PR comment. Store results in eval_history | pending |

---

## Phase 11 -- Observability

Tracing and cost tracking.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S11.1 | `specs/spec-S11.1-logfire-integration/` | S1.3 | `src/mcpguard/observability/logfire_setup.py` | Pydantic Logfire setup | OpenTelemetry TracerProvider with Logfire exporter. Spans: connect_server, enumerate_tools, scan_tool, each detector, semantic_analysis, generate_report. GenAI semantic conventions for LLM calls | pending |
| S11.2 | `specs/spec-S11.2-cost-tracker/` | S2.1 | `src/mcpguard/observability/cost_tracker.py` | Cost tracking | Track LLM token usage per scan. Estimate cost per model (Gemini Flash $0.15/M, Groq free). Include in ServerAuditReport.estimated_cost_usd | pending |

---

## Phase 12 -- Infrastructure and Deployment

CI/CD, PyPI publishing, MCP registry, documentation.

| Spec | Spec Location | Depends On | Location | Feature | Notes | Status |
|------|--------------|-----------|----------|---------|-------|--------|
| S12.1 | `specs/spec-S12.1-github-actions-ci/` | S1.2 | `.github/workflows/ci.yml` | CI pipeline | On push/PR: lint (ruff), type-check (mypy), test (pytest --cov), coverage (80%). Python 3.10, 3.11, 3.12 matrix | pending |
| S12.2 | `specs/spec-S12.2-pypi-publish/` | S1.1 | `.github/workflows/publish.yml` | PyPI Trusted Publisher | On release tag: build with Hatchling, publish to PyPI via OIDC (zero-token). Verify `pip install mcpguard` works. Verify `uvx mcpguard scan .` works | pending |
| S12.3 | `specs/spec-S12.3-mcp-registry/` | S9.1 | -- | MCP registry listing | Publish to official MCP registry + Smithery + Glama. Include proper metadata, screenshots, usage examples | pending |
| S12.4 | `specs/spec-S12.4-documentation/` | S12.3 | `README.md`, `docs/rules.md`, `docs/owasp-mapping.md`, `docs/ci-cd-integration.md` | Documentation | README with F1 benchmark table, architecture diagram, quickstart. Rules reference. OWASP mapping coverage. CI/CD integration guide with GitHub Actions SARIF example | pending |

---

## Master Spec Index

| Spec | Phase | Location | Feature | Spec Location | Status |
|------|-------|----------|---------|--------------|--------|
| S1.1 | Project Foundation | `pyproject.toml`, `.env.example` | Dependency declaration | `specs/spec-S1.1-dependency-declaration/` | done |
| S1.2 | Project Foundation | `Makefile` | Developer commands | `specs/spec-S1.2-developer-commands/` | done |
| S1.3 | Project Foundation | `src/mcpguard/models/config.py` | ScanConfig + settings | `specs/spec-S1.3-config/` | done |
| S1.4 | Project Foundation | `src/mcpguard/__init__.py` | Package initialization | `specs/spec-S1.4-package-init/` | done |
| S1.5 | Project Foundation | `src/mcpguard/utils/logging.py` | Structured logging | `specs/spec-S1.5-logging-setup/` | pending |
| S2.1 | Data Models | `src/mcpguard/models/findings.py` | VulnerabilityFinding + ServerAuditReport | `specs/spec-S2.1-finding-models/` | pending |
| S2.2 | Data Models | `src/mcpguard/models/semantic.py` | SemanticAnalysis model | `specs/spec-S2.2-semantic-models/` | pending |
| S2.3 | Data Models | `src/mcpguard/models/tool_def.py` | ToolDefinition model | `specs/spec-S2.3-tool-definition-model/` | pending |
| S2.4 | Data Models | `src/mcpguard/models/events.py` | Streaming event models | `specs/spec-S2.4-scan-events/` | pending |
| S3.1 | Detection Rules | `src/mcpguard/rules/patterns.py` | All regex patterns | `specs/spec-S3.1-regex-patterns/` | pending |
| S3.2 | Detection Rules | `src/mcpguard/rules/owasp_mapping.py` | OWASP MCP Top 10 mapping | `specs/spec-S3.2-owasp-mapping/` | pending |
| S3.3 | Detection Rules | `src/mcpguard/rules/cvss.py` | Risk scoring logic | `specs/spec-S3.3-cvss-scoring/` | pending |
| S4.1 | Static Detectors | `src/mcpguard/detectors/base.py` | BaseDetector ABC + registry | `specs/spec-S4.1-base-detector/` | pending |
| S4.2 | Static Detectors | `src/mcpguard/detectors/poisoning.py` | Tool poisoning detector | `specs/spec-S4.2-poisoning-detector/` | pending |
| S4.3 | Static Detectors | `src/mcpguard/detectors/unicode.py` | Unicode steganography detector | `specs/spec-S4.3-unicode-detector/` | pending |
| S4.4 | Static Detectors | `src/mcpguard/detectors/credentials.py` | Credential/secret detector | `specs/spec-S4.4-credential-detector/` | pending |
| S4.5 | Static Detectors | `src/mcpguard/detectors/full_schema.py` | Full-schema poisoning detector | `specs/spec-S4.5-full-schema-detector/` | pending |
| S4.6 | Static Detectors | `src/mcpguard/detectors/ssrf.py` | SSRF risk detector | `specs/spec-S4.6-ssrf-detector/` | pending |
| S4.7 | Static Detectors | `src/mcpguard/detectors/command_injection.py` | Command injection detector | `specs/spec-S4.7-command-injection-detector/` | pending |
| S5.1 | Integrity + Auth | `src/mcpguard/detectors/rug_pull.py`, `src/mcpguard/utils/hashing.py` | Rug pull detector | `specs/spec-S5.1-rug-pull-detector/` | pending |
| S5.2 | Integrity + Auth | `src/mcpguard/detectors/auth.py` | Auth compliance detector | `specs/spec-S5.2-auth-detector/` | pending |
| S5.3 | Integrity + Auth | `src/mcpguard/detectors/transport.py` | Transport security detector | `specs/spec-S5.3-transport-detector/` | pending |
| S5.4 | Integrity + Auth | `src/mcpguard/detectors/shadowing.py` | Cross-server shadowing | `specs/spec-S5.4-shadowing-detector/` | pending |
| S6.1 | PydanticAI Agents | `src/mcpguard/agents/semantic_agent.py` | Semantic analyzer | `specs/spec-S6.1-semantic-agent/` | pending |
| S6.2 | PydanticAI Agents | `src/mcpguard/agents/report_agent.py` | Report generator | `specs/spec-S6.2-report-agent/` | pending |
| S6.3 | PydanticAI Agents | `src/mcpguard/scanner.py` | Scan orchestrator | `specs/spec-S6.3-scan-orchestrator/` | pending |
| S7.1 | CLI Interface | `src/mcpguard/cli.py` | Typer CLI skeleton | `specs/spec-S7.1-cli-skeleton/` | pending |
| S7.2 | CLI Interface | `src/mcpguard/cli.py` | scan subcommand | `specs/spec-S7.2-scan-command/` | pending |
| S7.3 | CLI Interface | `src/mcpguard/utils/config_loader.py` | Config auto-discovery | `specs/spec-S7.3-config-discovery/` | pending |
| S7.4 | CLI Interface | `src/mcpguard/cli.py` | baseline + eval + serve + rules | `specs/spec-S7.4-other-commands/` | pending |
| S8.1 | Output Formatters | `src/mcpguard/formatters/rich_output.py` | Rich terminal rendering | `specs/spec-S8.1-rich-formatter/` | pending |
| S8.2 | Output Formatters | `src/mcpguard/formatters/json_output.py` | JSON formatter | `specs/spec-S8.2-json-formatter/` | pending |
| S8.3 | Output Formatters | `src/mcpguard/formatters/sarif.py` | SARIF 2.1.0 generator | `specs/spec-S8.3-sarif-formatter/` | pending |
| S9.1 | MCP Server | `src/mcpguard/mcp_server.py` | FastMCP server tools | `specs/spec-S9.1-mcp-server-tools/` | pending |
| S9.2 | MCP Server | `src/mcpguard/mcp_server.py` | Resources + prompts | `specs/spec-S9.2-mcp-resources-prompts/` | pending |
| S9.3 | MCP Server | -- | IDE config | `specs/spec-S9.3-ide-config/` | pending |
| S10.1 | Evaluation | `evaluation/benchmark.yaml` | Benchmark dataset | `specs/spec-S10.1-benchmark-dataset/` | pending |
| S10.2 | Evaluation | `evaluation/fixtures/` | Vulnerable test servers | `specs/spec-S10.2-test-fixtures/` | pending |
| S10.3 | Evaluation | `evaluation/run_eval.py` | Eval runner | `specs/spec-S10.3-eval-runner/` | pending |
| S10.4 | Evaluation | `.github/workflows/eval.yml` | CI eval gate | `specs/spec-S10.4-eval-ci-gate/` | pending |
| S11.1 | Observability | `src/mcpguard/observability/logfire_setup.py` | Logfire integration | `specs/spec-S11.1-logfire-integration/` | pending |
| S11.2 | Observability | `src/mcpguard/observability/cost_tracker.py` | Cost tracking | `specs/spec-S11.2-cost-tracker/` | pending |
| S12.1 | Infrastructure | `.github/workflows/ci.yml` | CI pipeline | `specs/spec-S12.1-github-actions-ci/` | pending |
| S12.2 | Infrastructure | `.github/workflows/publish.yml` | PyPI publish | `specs/spec-S12.2-pypi-publish/` | pending |
| S12.3 | Infrastructure | -- | MCP registry listing | `specs/spec-S12.3-mcp-registry/` | pending |
| S12.4 | Infrastructure | `README.md`, `docs/` | Documentation | `specs/spec-S12.4-documentation/` | pending |
