# WorkVault architecture

## Product boundary

WorkVault is not an iTerm2 clone, a transcript dump, or a terminal multiplexer.

It is a local-first system that:

1. observes work across terminals, agents, repositories, applications, and files;
2. preserves evidence without flattening observations and inference together;
3. reconstructs temporal state;
4. links runs to artifacts, commits, research, decisions, incidents, and products;
5. generates resumable views such as handoffs, dashboards, and provenance graphs.

## Conceptual layers

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
                       |
                 terminal UI
```

A useful mental split is:

```text
WorkScope   sees live state
WorkVault   remembers evidence/history
WorkGraph   understands relationships
Workbench   lets the user inspect/act
```

These can remain one repository/product while preserving clear internal boundaries.

## Six durable entities

### Project

Long-lived canonical effort or product.

### Workstream

Coherent objective that can span sessions, agents, and repositories.

### Session

Working context from a provider/surface: terminal, agent CLI, ChatGPT export, IDE session, etc.

### Run

One execution inside a session.

Run modes:

```text
foreground
background
queued
detached
scheduled
```

Runs may have `parent_run_id` for delegated/subagent trees.

### Artifact

Output produced or materially modified by work.

Examples: source files, commits, images, reports, datasets, PIGGs, prompts, skills, manifests, generated HTML, configuration files.

### Resource

Observed/referenced dependency not necessarily owned by WorkVault.

Examples: URL, GitHub repository, filesystem path, application, process, model, agent runtime, SQLite database, MCP endpoint, secret location.

## Runtime identity

A normalized active-session identity should be able to correlate agent and terminal worlds:

```json
{
  "session_id": "ses_...",
  "provider_session_id": "native-agent-id",
  "provider": "codex",
  "agent": "codex",
  "model": "gpt-...",
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

Do not require every field. Evidence may arrive incrementally.

## Observation versus inference

Sensors should emit observations only.

An iTerm2 adapter can know:

```text
window ID
tab ID
session ID
TTY
CWD
profile
hostname
foreground process
```

It should not decide:

```text
project
workstream
business intent
agent role
```

Those are semantic inferences in the core and should carry evidence/confidence.

## Event pipeline

```text
RAW OBSERVATION
      |
      v
NORMALIZE
      |
      v
CLASSIFY SENSITIVITY
      |
      v
STORE EVENT + EVIDENCE
      |
      v
UPDATE TEMPORAL FACTS
      |
      v
UPDATE MATERIALIZED CURRENT STATE
      |
      v
OPTIONAL SEMANTIC EXTRACTION
```

This ordering prevents an early inference from becoming indistinguishable from direct evidence.

## Storage

Recommended v1 storage:

```text
SQLite
  normalized entities
  temporal/current-state tables
  relationships
  FTS5 search

JSONL
  append-friendly canonical event archive

Filesystem references
  raw/private evidence references
  managed artifacts

Git
  source history and commit provenance
```

Embeddings are optional and later. Structured metadata + FTS5 + provenance should work first.

## Materialized current state

Avoid replaying the complete history for common queries.

Suggested current-state views/tables:

```text
projects_current
workstreams_current
sessions_current
runs_current
artifacts_current
resources_current
paths_current
```

History remains immutable; reducers update the current-state projections.

## Conversation import architecture

```text
provider-specific parser
      |
      v
normalized message/tool/file/run events
      |
      v
semantic extraction
      |
      v
projects/workstreams/artifacts/relationships
```

Adapters:

```text
codex
claude
hermes_poseidon
chatgpt
gemini
qwen
cursor
qodo
generic_terminal
```

Parser version should be recorded so semantic extraction can be regenerated later.

## Terminal/provider adapters

```text
terminals/
  iterm2
  vscode
  obsidian
  claude_terminal
  tmux
  generic_pty
```

iTerm2 is the primary early sensor, not a schema dependency.

## Existing components to reuse

### my-supremepowers

Already has hook-driven tool-use event capture. Adapt it into a redacting/normalized WorkVault event bridge.

### my-codex

Already demonstrates thin Codex runtime adapters to a canonical control plane.

### claude-manager

Useful patterns:

- SessionStart hook
- `{sessionId, ppid}` mapping
- active-session detection
- transcript search
- resume/continue/fork/import/export
- project + branch filtering
- workspace restore

### claude-terminal

Useful patterns:

- Control Tower
- session recap
- subagent visualization
- worktree isolation
- terminal/chat cross-reference
- checkpoint/file rewind

### git-ai

Use for line/commit-level AI attribution where available. WorkVault should link to it rather than reimplement attribution.

### obsidian-terminal

Useful for terminal-history/provider abstraction and saved/restored terminal history.

## Planned CLI surface

Early:

```text
wv github-audit
wv ingest
wv inspect
wv history
wv resume
wv doctor
```

Later:

```text
wv sessions
wv runs
wv repos
wv agents
wv artifacts
wv graph
wv checkpoint
wv restore
wv dashboard
wv show
```

## Read/write safety boundary

The initial system is read-only except for WorkVault's own storage/output files.

Any future action that writes into terminals, modifies repositories, changes app state, or restores sessions must be separately gated and auditable.
