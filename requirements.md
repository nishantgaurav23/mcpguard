# MCPGuard — Requirements Document

**Version:** 1.0  
**Last Updated:** March 2026  
**Author:** Nishant  
**Status:** Draft

---

## 1. Project Overview

### 1.1 Problem Statement

The MCP ecosystem has exploded to 20,000+ servers since November 2024, yet security is catastrophically poor. Research by Astrix Security (5,200+ servers), Endor Labs (2,614 servers), and the MCPTox benchmark reveals: 53% of servers use insecure static secrets, 82% are vulnerable to path traversal, 43% have command injection flaws, and tool poisoning attacks succeed 60–73% of the time across 20 LLM agents. 30+ CVEs were filed in January–February 2026 alone, including CVSS 9.6 (mcp-remote RCE) and CVSS 9.4 (MCP Inspector unauthenticated RCE). OWASP published a dedicated MCP Top 10, and the EU AI Act compliance deadline is August 2, 2026.

Existing security tools are fragmented: mcp-scan (Snyk) does tool poisoning only, mcp-audit (APIsec) does config scanning only, Cisco mcp-scanner requires a commercial subscription for full features. No single open-source tool combines credential scanning, full-schema poisoning detection, authentication compliance testing, SSRF analysis, rug-pull detection, and structured reporting into a unified intelligent agent.

### 1.2 Project Goal

Build **MCPGuard**, an AI-powered MCP security auditor that:
- Connects to any MCP server and performs comprehensive security analysis
- Detects vulnerabilities across all 10 OWASP MCP risk categories
- Streams scan results in real-time via CLI with Rich formatting
- Ships as both a CLI tool (`pip install mcpguard`) AND an MCP server (usable from Claude Desktop, Cursor)
- Produces structured SARIF/JSON reports for CI/CD integration
- Includes a self-evaluation benchmark with precision/recall metrics
- Uses PydanticAI for intelligent semantic analysis of ambiguous findings

### 1.3 Target Users

| User Persona | Need | Usage Pattern |
|-------------|------|---------------|
| **AI Engineer** (primary) | Audit MCP servers before connecting them to agents | Ad-hoc CLI scans during development |
| **Security Engineer** | Assess MCP server fleet for org-wide risks | Batch scanning, SARIF reports, CI/CD gates |
| **MCP Server Author** | Validate own server before publishing | Pre-publish check, integrated in dev workflow |
| **IDE User** (Cursor/Claude Desktop) | On-demand security check from IDE | MCP server mode, natural language queries |

### 1.4 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tool poisoning detection recall | ≥ 0.90 | Evaluation on 50+ labeled test cases |
| Tool poisoning detection precision | ≥ 0.85 | Same benchmark (minimize false positives) |
| Credential detection recall | ≥ 0.95 | Regex pattern coverage on known secret types |
| Full-schema poisoning detection | ≥ 0.80 | CyberArk-style parameter name attacks |
| Rug pull detection accuracy | 1.00 | Hash-based, deterministic |
| Overall F1 score (all categories) | ≥ 0.85 | Aggregate across all vulnerability classes |
| False positive rate | ≤ 0.15 | On clean/legitimate server descriptions |
| Scan latency (10-tool server) | ≤ 15 seconds | Rule-based + LLM semantic analysis |
| Scan latency (rule-based only) | ≤ 2 seconds | No LLM calls |
| CI/CD integration | Pass/fail exit codes + SARIF | GitHub Actions compatible |
| LLM cost per scan | ≤ $0.02 | Gemini Flash free tier for most scans |

---

## 2. Functional Requirements

### 2.1 Core Scanning Features

#### FR-01: MCP Server Connection and Introspection
- **Description:** Connect to any MCP server via stdio or Streamable HTTP transport. Enumerate all tools, resources, resource templates, prompts, and server capabilities. Extract server name, version, and instruction text.
- **Input:** Server connection config (command + args for stdio, URL for HTTP) or path to MCP config file (Claude Desktop, Cursor, VS Code format)
- **Output:** Complete server inventory: tool definitions (name, description, inputSchema), resource list, prompt list, server metadata
- **Priority:** P0 (Must Have)

#### FR-02: Tool Poisoning Detection (Description-Level)
- **Description:** Scan tool descriptions for hidden instructions targeting the LLM rather than describing the tool's functionality. Detect `<IMPORTANT>`, `[CRITICAL]`, `**SYSTEM**`, `NOTE:`, `REQUIRED:` directive tags, file exfiltration directives, cross-tool manipulation references, attacker-controlled URLs, and unusual instruction patterns.
- **Detection method:** Regex pattern matching + LLM semantic analysis for ambiguous cases
- **Priority:** P0 (Must Have)

#### FR-03: Full-Schema Poisoning Detection (CyberArk-Style)
- **Description:** Scan ALL JSON schema fields for hidden instructions — not just descriptions. Check parameter names, type fields, required arrays, default values, enum values, and example fields. Example: a parameter named `content_from_reading_ssh_id_rsa` injects instructions via its key name.
- **Detection method:** Entropy analysis on parameter names, keyword matching across all schema fields, LLM semantic analysis
- **Priority:** P0 (Must Have)
- **Note:** This is MCPGuard's primary differentiator. No existing tool performs full-schema analysis.

#### FR-04: Unicode Steganography Detection
- **Description:** Detect invisible Unicode characters used to hide instructions: zero-width space (U+200B), zero-width non-joiner (U+200C), zero-width joiner (U+200D), left-to-right mark (U+200E), byte-order mark (U+FEFF), and other invisible codepoints.
- **Detection method:** Character-class scanning across all text fields
- **Priority:** P0 (Must Have)

#### FR-05: Credential and Secret Detection
- **Description:** Scan tool descriptions, parameter schemas, default values, example fields, and server instructions for exposed credentials. Detect 25+ secret types: AWS keys, GitHub tokens, Slack tokens, Stripe keys, private key headers, JWTs, generic API keys, bearer tokens, database connection strings.
- **Detection method:** Regex pattern matching from established rulesets (TruffleHog, Gitleaks, secrets-patterns-db)
- **Priority:** P0 (Must Have)

#### FR-06: SSRF Risk Detection
- **Description:** Identify tool input parameters that accept arbitrary URLs without documented validation constraints. Flag parameters named `url`, `uri`, `endpoint`, `callback`, `webhook`, `fetch`, `proxy`, `redirect`, `src`, `target`, `download` that accept unrestricted string input.
- **Detection method:** Schema analysis — parameter name matching + type/format constraint checking
- **Priority:** P1 (Should Have)

#### FR-07: Command Injection Pattern Detection
- **Description:** Flag tools whose descriptions reference shell execution or whose parameter schemas suggest command injection risk. Detect references to `os.system()`, `subprocess`, `exec()`, `eval()`, `shell`, `bash` in descriptions. Flag parameters named `cmd`, `exec`, `command`, `execute`, `code`, `payload`, `run`. Detect shell metacharacters in default values.
- **Detection method:** Regex + description keyword analysis
- **Priority:** P1 (Should Have)

#### FR-08: Rug Pull Detection via Tool Pinning
- **Description:** On first scan, compute SHA-256 hash of each tool's complete definition (name + description + full inputSchema JSON). Store hashes in `~/.mcpguard/baselines.json`. On subsequent scans, compare current hashes against baseline. Any mismatch triggers a rug pull alert with a diff of exactly what changed.
- **Detection method:** Deterministic hash comparison
- **Priority:** P0 (Must Have)

#### FR-09: Authentication and Authorization Compliance
- **Description:** For HTTP-transport MCP servers, check OAuth 2.1 compliance per MCP spec. Probe `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`. Verify PKCE enforcement (S256, not plain). Check for proper 401 responses with `WWW-Authenticate` header. Classify auth status: oauth, api_key, none, unknown.
- **Detection method:** HTTP endpoint probing + response analysis
- **Priority:** P1 (Should Have)

#### FR-10: Transport Security Analysis
- **Description:** For HTTP-transport servers, verify HTTPS enforcement, Origin header validation, rate limiting headers, and session ID quality. For stdio servers, verify the server doesn't bind to 0.0.0.0 (should be localhost only).
- **Priority:** P2 (Nice to Have)

#### FR-11: Cross-Server Shadowing Detection
- **Description:** When scanning multiple servers from a config file, analyze tool descriptions across servers for cross-references that could enable shadowing attacks — where one server's descriptions inject instructions targeting tools on another server.
- **Detection method:** Cross-reference analysis across tool descriptions from all connected servers
- **Priority:** P1 (Should Have)

### 2.2 LLM-Powered Semantic Analysis

#### FR-12: Intelligent Ambiguity Resolution
- **Description:** For findings that pass rule-based checks but have anomalous characteristics (unusual entropy, borderline patterns), invoke PydanticAI agent with Gemini Flash to perform semantic analysis. The agent determines whether the content is a legitimate tool description or a disguised instruction.
- **LLM:** Gemini 2.5 Flash (free tier: 1,000 RPD) or Groq Llama 3.3 70B (free tier: 14,400 RPD)
- **Cost strategy:** Rule-based checks first (zero cost). LLM only for ambiguous cases (~10-20% of findings).
- **Priority:** P0 (Must Have)

#### FR-13: Structured Report Generation
- **Description:** PydanticAI agent synthesizes all findings into a `ServerAuditReport` Pydantic model with validated fields: overall risk score (0-10), findings list with CVSS-aligned severity, OWASP MCP mapping, remediation recommendations, and tool inventory.
- **Output validation:** Pydantic model validation with automatic retry on schema failure
- **Priority:** P0 (Must Have)

### 2.3 Output and Integration

#### FR-14: Rich Terminal Output (Default)
- **Description:** Color-coded, severity-tagged table output using Rich library. Real-time streaming of findings as each check completes. Summary panel with overall risk score, finding counts by severity, and pass/fail verdict.
- **Priority:** P0 (Must Have)

#### FR-15: JSON Output
- **Description:** Machine-readable JSON output with full finding details, evidence, remediation, and OWASP mappings. Activated via `--format json`.
- **Priority:** P0 (Must Have)

#### FR-16: SARIF 2.1.0 Output
- **Description:** OASIS-standard Static Analysis Results Interchange Format. Compatible with GitHub Code Scanning (`github/codeql-action/upload-sarif@v3`). Each detection rule maps to a SARIF `rules[]` entry with CWE and OWASP tags.
- **Priority:** P1 (Should Have)

#### FR-17: CI/CD Exit Codes
- **Description:** Exit code 0 = no findings above threshold. Exit code 1 = findings at/above severity threshold. Exit code 2 = scanner error. Configurable threshold via `--severity-threshold`.
- **Priority:** P0 (Must Have)

### 2.4 MCP Server Mode

#### FR-18: MCPGuard as MCP Server
- **Description:** MCPGuard itself ships as a FastMCP server with tools: `scan_server`, `scan_config`, `check_tool`, `get_latest_report`. Installable via Claude Desktop/Cursor MCP config. Users can ask "Is this MCP server safe?" in natural language.
- **Transport:** stdio (for Claude Desktop) and Streamable HTTP (for remote use)
- **Priority:** P0 (Must Have)

#### FR-19: MCP Resource Endpoints
- **Description:** Expose scan results as MCP resources: `mcpguard://latest-report`, `mcpguard://baseline/{server_name}`, `mcpguard://rules` (list all detection rules).
- **Priority:** P2 (Nice to Have)

### 2.5 Evaluation Framework

#### FR-20: Self-Evaluation Benchmark
- **Description:** Ship a `pydantic-evals` Dataset with 50+ labeled test cases (half benign, half malicious across all vulnerability categories). Run MCPGuard against the benchmark and report precision, recall, F1 per category. Results are part of the README.
- **Priority:** P0 (Must Have)

#### FR-21: Intentionally Vulnerable Test Servers
- **Description:** Include FastMCP-based test fixtures: a clean server (zero findings expected), and servers with each vulnerability type (tool poisoning, credential leak, SSRF risk, command injection, rug pull, no auth). Used in pytest suite and CI/CD.
- **Priority:** P0 (Must Have)

#### FR-22: Evaluation Reporting
- **Description:** Rich terminal table showing per-category precision/recall/F1. JSON export of evaluation results. Integration with Pydantic Logfire for visual dashboards.
- **Priority:** P1 (Should Have)

### 2.6 CLI Interface

#### FR-23: CLI Commands
- **Description:** Typer-based CLI with subcommands:
  - `mcpguard scan <config-path>` — Scan servers from MCP config file
  - `mcpguard scan --url <server-url>` — Scan a single HTTP server
  - `mcpguard scan --cmd "<command>"` — Scan a single stdio server
  - `mcpguard baseline <config-path>` — Create/update tool hash baselines
  - `mcpguard eval` — Run self-evaluation benchmark
  - `mcpguard serve` — Start MCPGuard as MCP server
  - `mcpguard rules` — List all detection rules with IDs
- **Priority:** P0 (Must Have)

#### FR-24: Config File Auto-Discovery
- **Description:** Auto-detect MCP config files in standard locations: `~/.config/claude/claude_desktop_config.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `mcp.json` in current directory.
- **Priority:** P1 (Should Have)

### 2.7 Observability

#### FR-25: Pydantic Logfire Integration
- **Description:** All scan operations instrumented via OpenTelemetry. Traces capture: server connection, tool enumeration, each detector run (with timing), LLM calls (with token usage and cost), report generation. Viewable in Pydantic Logfire dashboard (free tier: 10M spans/month).
- **Priority:** P1 (Should Have)

---

## 3. Non-Functional Requirements

### 3.1 Performance

| Requirement | Target | Rationale |
|------------|--------|-----------|
| NFR-01: Rule-based scan (10 tools) | ≤ 2 seconds | No LLM, pure regex/heuristic |
| NFR-02: Full scan with LLM (10 tools) | ≤ 15 seconds | Includes semantic analysis |
| NFR-03: Config file parsing | ≤ 500ms | Local file I/O only |
| NFR-04: Streaming first finding | ≤ 1 second | User sees progress immediately |
| NFR-05: SARIF generation | ≤ 500ms | Template-based |

### 3.2 Reliability

| Requirement | Target |
|------------|--------|
| NFR-06: Graceful handling of unreachable servers | Report connection failure, continue scanning other servers |
| NFR-07: LLM fallback | If Gemini unavailable, fall back to rule-based only with "limited analysis" warning |
| NFR-08: Timeout handling | 30-second timeout per server connection; configurable via `--timeout` |

### 3.3 Security (MCPGuard's Own Security)

| Requirement | Description |
|------------|-------------|
| NFR-09: No credential storage | MCPGuard never stores target server credentials; reads from config files only |
| NFR-10: Baseline file protection | Tool hash baselines stored with 0600 permissions in `~/.mcpguard/` |
| NFR-11: No data exfiltration | Scan results stay local unless user explicitly exports; LLM calls send only tool schemas, not user data |
| NFR-12: Input sanitization | MCPGuard sanitizes all server responses before processing to prevent injection into its own LLM agent |

### 3.4 Cost Constraints

| Requirement | Target |
|------------|--------|
| NFR-13: Total project budget | ≤ $20 |
| NFR-14: Expected actual spend | ~$3 (most scans use free tier) |
| NFR-15: Per-scan cost (with LLM) | ≤ $0.02 |
| NFR-16: Per-scan cost (rule-based only) | $0.00 |

### 3.5 Compatibility

| Requirement | Description |
|------------|-------------|
| NFR-17: Python version | ≥ 3.10 |
| NFR-18: OS support | Linux, macOS, Windows (stdio transport) |
| NFR-19: MCP spec version | 2025-06-18 (latest stable) |
| NFR-20: Config file formats | Claude Desktop, Cursor, VS Code, generic mcp.json |

### 3.6 Packaging and Distribution

| Requirement | Description |
|------------|-------------|
| NFR-21: PyPI package | `pip install mcpguard` |
| NFR-22: uvx support | `uvx mcpguard scan .` (zero-install execution) |
| NFR-23: MCP registry listing | Published to official MCP registry + Smithery + Glama |
| NFR-24: Package size | ≤ 10MB (no bundled models; LLM calls are API-based) |

---

## 4. Data Requirements

### 4.1 Detection Rule Database

| Rule Category | Source | Count | Format |
|--------------|--------|-------|--------|
| Tool poisoning patterns | Custom + MCPTox research | ~30 regex patterns | Python regex |
| Secret patterns | TruffleHog/Gitleaks adapted | 25+ patterns | Python regex |
| SSRF parameter names | OWASP SSRF cheat sheet | ~15 keywords | String list |
| Command injection patterns | OWASP Command Injection | ~20 patterns | Regex + keyword list |
| Unicode steganography | Unicode standard | ~10 codepoint ranges | Character class |
| OWASP MCP Top 10 mapping | OWASP 2025 | 10 categories | JSON mapping |

### 4.2 Evaluation Dataset

| Dataset | Size | Content | Format |
|---------|------|---------|--------|
| Benign tool definitions | 25+ | Legitimate MCP tools from popular servers | YAML (pydantic-evals) |
| Malicious tool definitions | 25+ | Tool poisoning, credential leaks, injection patterns | YAML |
| Golden scan results | 50+ | Expected findings per test case | YAML |
| Vulnerable test servers | 7+ | FastMCP servers with intentional flaws | Python fixtures |

### 4.3 Baseline Storage

```
~/.mcpguard/
├── baselines.json          # Tool hash baselines per server
├── config.json             # MCPGuard user preferences
└── scan_history.json       # Optional: historical scan results
```

---

## 5. Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| Agent Framework | PydanticAI v1.70+ | Type-safe structured outputs; native MCP client/server; pydantic-evals; 3rd framework after LangGraph & CrewAI |
| MCP Server Building | FastMCP (via PydanticAI) | Standard MCP server framework; decorator-based API |
| CLI Framework | Typer | Type-hint-based CLI; Pydantic ecosystem alignment |
| Terminal Output | Rich | Tables, progress bars, streaming, severity colors |
| LLM (primary) | Gemini 2.5 Flash (free tier) | 1,000 RPD free; cheapest option for semantic analysis |
| LLM (fallback) | Groq Llama 3.3 70B (free tier) | 14,400 RPD free; fast inference |
| Evaluation | pydantic-evals | PydanticAI-native; Dataset/Case/Evaluator pattern |
| Observability | Pydantic Logfire | OTel-native; 10M spans/month free; native PydanticAI integration |
| Hashing | hashlib (stdlib) | SHA-256 for tool pinning; zero dependencies |
| HTTP Client | httpx | Async HTTP for auth probing; PydanticAI dependency |
| Testing | pytest + pytest-asyncio | Standard Python testing; async MCP server testing |
| CI/CD | GitHub Actions | Free for public repos; SARIF upload support |
| Packaging | Hatchling + PyPI Trusted Publishers | Zero-token publishing via OIDC |

---

## 6. Constraints and Assumptions

### 6.1 Constraints
- C-01: Total budget ≤ $20
- C-02: Single developer, 3-week timeline
- C-03: Must work without paid API subscriptions
- C-04: Cannot execute arbitrary code on target servers (scan only, never exploit)
- C-05: LLM semantic analysis limited to free tier quotas
- C-06: No server-side persistence (CLI tool, not a web app)

### 6.2 Assumptions
- A-01: Gemini 2.5 Flash free tier (1,000 RPD) remains available
- A-02: Groq free tier remains available as fallback
- A-03: Target MCP servers respond to tool/resource listing requests
- A-04: MCP config file locations follow standard conventions
- A-05: PydanticAI MCP client API remains stable (V1 commitment)

### 6.3 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM free tier exhausted during demo | Low | Medium | Fall back to rule-based only; cache LLM responses |
| New vulnerability class emerges | Medium | Low | Modular detector design; add new detector without refactoring |
| False positives annoy users | Medium | High | Strict precision target (≥0.85); severity threshold flag; `--strict` mode |
| Target server blocks introspection | Medium | Low | Report as "unable to enumerate" rather than fail |
| PydanticAI MCP client API changes | Low | Medium | Pin version; V1 stability commitment |

---

## 7. Milestones

| Milestone | Target Date | Deliverables |
|-----------|------------|--------------|
| M1: Detection Engine | Day 7 | All rule-based detectors (poisoning, credentials, SSRF, injection, unicode), CLI skeleton with Rich output, rug pull hash pinning |
| M2: LLM + MCP Integration | Day 14 | PydanticAI semantic analyzer, structured report generation, MCP server mode (FastMCP), connect-and-scan via stdio + HTTP |
| M3: Eval + Ship | Day 21 | pydantic-evals benchmark (50+ cases), vulnerable test fixtures, SARIF output, CI/CD workflow, PyPI publish, MCP registry listing, README with F1 table |
