# WorkVault

`AvaTar-ArTs/iterm2` is the portable seed repository for **WorkVault**, a local-first terminal, AI-session, repository-provenance, and workspace-recovery system.

The original iTerm2-specific work remains part of the design, but iTerm2 is now treated as a sensor/provider rather than the whole product. WorkVault correlates terminal sessions, agent sessions, processes, repositories, branches, transcripts, tool events, artifacts, research, decisions, incidents, and provenance without making raw private history public by default.

## Design record

The architecture is grounded in real working histories rather than synthetic examples.

- [`docs/CONVERSATION_SYNTHESIS.md`](docs/CONVERSATION_SYNTHESIS.md) — complete design synthesis from the WorkVault/iTerm2 conversation
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — core architecture and runtime model
- [`docs/FIXTURE_CORPUS.md`](docs/FIXTURE_CORPUS.md) — Fiverr, ESO/Poseidon, CoH/LaunchCat, marketplace-agent, and multi-agent iTerm2 golden fixtures
- [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md) — local-first ingestion, redaction, reference-only evidence, public/private boundaries
- [`schemas/canonical-event.schema.json`](schemas/canonical-event.schema.json) — first executable canonical-event contract

## First working command: repository hygiene audit

Install locally:

```bash
python -m pip install -e .
```

Scan the current repository:

```bash
wv github-audit .
```

Machine-readable output:

```bash
wv github-audit . --json
```

Use in CI or automation:

```bash
wv github-audit . --fail-on private
wv github-audit . --fail-on secret
```

Current classifications:

- `SAFE_PUBLIC` — explicitly safe/exportable material
- `REVIEW` — logs, debug output, temp data, backups, or similar material requiring review
- `PRIVATE_REFERENCE` — AI/session/runtime history that should usually remain local/private and be indexed by reference
- `SECRET_ROTATE` — credential files or secret-like content requiring immediate review and likely rotation if committed publicly

The scanner reports **where** a secret-like signal was found without echoing the matched secret value.

## Why WorkVault exists

A terminal window is a control room, not an archive.

Across the reviewed histories, a single working session can contain:

```text
research
background agents
code changes
Git commits
failed runs
security incidents
filesystem mutations
model switches
source corrections
GUI actions
queued follow-ups
productization
interrupted work
```

Flattening that into one transcript loses the actual project state.

WorkVault preserves the causal structure.

## Six durable entities

The conversation initially surfaced many useful concepts. The core was deliberately reduced to six durable entities so the database does not become an ontology maze:

```text
PROJECT      long-lived canonical effort/product
WORKSTREAM   coherent objective spanning sessions/runs
SESSION      working context from terminal/agent/chat/IDE
RUN          one foreground/background/queued/detached execution
ARTIFACT     produced or materially modified output
RESOURCE     observed/referenced dependency WorkVault may not own
```

Incidents, decisions, corrections, source status, model changes, drift, milestones, path mutations, and follow-ups are represented primarily as typed events.

## Canonical event model

Representative events:

```text
objective.created
objective.refined
objective.corrected
session.started
session.interrupted
run.started
run.failed
run.completed
artifact.created
artifact.verified
claim.corrected
decision.recorded
incident.detected
incident.remediated
path.symlinked
drift.detected
source.blocked
source.excluded
model.changed
milestone.reached
followup.queued
```

Events preserve history. Reducers/materialized views provide fast current-state queries.

## Temporal + evidence-aware by default

Important facts can carry:

```text
observed_at
valid_from
valid_to
```

and evidence classes such as:

```text
user_assertion
tool_observation
filesystem_observation
git_observation
test_result
external_source
agent_inference
assistant_statement
derived_computation
```

This keeps statements such as “I’m starting the tunnel” separate from stronger observations such as a passing health endpoint or test result.

## Runtime identity

The target runtime identity correlates agent and terminal worlds:

```json
{
  "session_id": "ses_...",
  "provider_session_id": "agent-native-id",
  "provider": "codex",
  "agent": "codex",
  "model": "provider/model",
  "pid": 1234,
  "ppid": 987,
  "tty": "/dev/ttys016",
  "terminal_provider": "iterm2",
  "terminal_session_id": "native-terminal-id",
  "cwd": "/path/to/working-dir",
  "repo": "/path/to/repo",
  "branch": "main"
}
```

Fields may be discovered incrementally from different sensors.

## Architecture

```text
                   LIVE WORLD
                       |
     +-----------------+-----------------+
     |                 |                 |
   terminals         Git/fs           agents/apps
     |                 |                 |
     +---------- OBSERVATION BUS --------+
                       |
                       v
                 CANONICAL EVENTS
                       |
             +---------+---------+
             |                   |
             v                   v
         WorkVault            WorkGraph
       SQLite/JSONL          relationships
       raw references        temporal facts
             |                   |
             +---------+---------+
                       v
                 MATERIALIZED STATE
                       |
       +---------------+----------------+
       v               v                v
      CLI            HTML             MCP/API
```

Conceptually:

```text
WorkScope   sees
WorkVault   remembers
WorkGraph   understands
Workbench   lets you act
```

## Conversation ingestion

WorkVault should **ingest conversations, not merely store them**.

Three layers:

```text
1. immutable raw/reference evidence
2. provider-neutral normalized events
3. semantic extraction into projects/workstreams/artifacts/relationships
```

Provider-specific parsers can then target a common schema:

```text
codex
claude
hermes / poseidon
chatgpt
gemini
qwen
cursor
qodo
generic terminal
```

## Existing ecosystem pieces to integrate, not reinvent

- `my-supremepowers` — hook/event/control logic and tool-use JSONL prototype
- `my-codex` — thin Codex runtime bridge and session/tool hooks
- `claude-manager` — session ID + PID mapping, search/resume/restore patterns
- `claude-terminal` — Control Tower, recaps, subagent/worktree/checkpoint UX
- `git-ai` — prompt/code/commit authorship provenance
- `.qwen` — Qwen commands/hooks/agent surface
- `obsidian-terminal` — terminal-history/provider abstraction patterns

WorkVault's job is the connective tissue: normalization, correlation, temporal state, evidence, and provenance.

## Security model

The guiding rule is:

```text
capture locally -> classify -> redact/reference -> normalize -> index -> explicitly export
```

not:

```text
capture -> commit everything
```

Sensitivity classes:

```text
PUBLIC
INTERNAL
SENSITIVE
SECRET
DO_NOT_INGEST
```

Ownership modes:

```text
MANAGED
REFERENCED
EPHEMERAL
```

Raw terminal scrollback, prompts, tool responses, OAuth files, API keys, session databases, shell snapshots, and agent histories are private evidence unless explicitly sanitized/exported.

## Golden evaluation corpus

The design is evaluated using real histories:

```text
Fiverr Seller OS
  execution + security + deployment + Git provenance

ESO / Poseidon / Hermes
  research + source provenance + corrections + model evolution

CoH / LaunchCat / Codex
  filesystem + application state + drift + path canonicality

Marketplace/background agents
  parallel runs + dependencies + productization

Multi-agent iTerm2 ecosystem
  cross-runtime orchestration + private/public boundaries
```

See [`docs/FIXTURE_CORPUS.md`](docs/FIXTURE_CORPUS.md) for gold questions and expected reconstruction.

## Revised implementation sequence

The conversation changed the build order. Build and evaluate the brain against existing histories **before** attaching autonomous behavior to the giant live iTerm2 workspace.

```text
01  github-audit repository hygiene                         DONE
02  canonical schemas                                      STARTED
03  SQLite + JSONL storage
04  event ingestion
05  generic terminal transcript importer
06  Codex importer
07  Hermes/Poseidon importer
08  import real fixture corpus
09  temporal reducers/current-state views
10  provenance relationships
11  gold-query evaluation harness
12  wv inspect
13  wv history
14  wv resume
15  static HTML dashboard
16  read-only iTerm observer
17  TTY -> process -> cwd -> Git correlation
18  agent detectors
19  shell hooks
20  status bar
21  checkpoint generation
22  MCP read layer
23  carefully gated write/actions
24  embeddings/semantic search only if justified
```

The next architectural milestone is therefore **`wv ingest`**, followed by fixture evaluation. `wv doctor` remains important, but it should reuse the same canonical schema against live observations after the ingestion core is trustworthy.

## Public versus local control plane

This GitHub repository should contain portable code, architecture, schemas, tests, and sanitized fixtures.

The richer living ecosystem under `/Users/steven/iterm2` remains local-first. WorkVault should reference and index that state rather than turn the public repo into a dump of private terminal/session history.
