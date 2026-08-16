# Cross-repository WorkVault ecosystem audit

This document captures the repository-level findings that shaped WorkVault after auditing the broader `AvaTar-ArTs` GitHub estate for terminal, session, agent, hook, history, and provenance systems.

## Highest-value reuse candidates

### `my-supremepowers`

Role: canonical hook/event/control logic.

Important existing pattern:

- `after-tool.sh` already writes JSONL containing timestamp, tool name, tool input, tool response, and exit code.
- synchronization logic can react to significant file/tool events.

WorkVault decision:

- reuse the hook/event concept;
- insert sensitivity classification/redaction before persistence;
- normalize the event into the WorkVault canonical schema;
- do not default to storing raw full tool inputs/responses.

Priority: `★★★★★`

### `my-codex`

Role: thin Codex runtime adapter to a canonical control plane.

Important existing patterns:

- `session-start.sh`
- `before-agent.sh`
- `after-tool.sh`
- capability discovery/atlas behavior
- repo-local adapter delegating to canonical runtime logic rather than duplicating implementation

WorkVault decision:

Use this as the adapter-design template. Provider integrations should remain thin and push normalized observations into WorkVault core.

Priority: `★★★★★`

### `claude-manager`

Role: session discovery, search, resume, restore, and runtime correlation patterns.

Important patterns:

- active session status
- `SessionStart` hook records `{sessionId, ppid}`
- terminal process IDs can be correlated with session IDs
- resume/continue/fork/import/export
- project and Git branch filtering
- full-text transcript search
- workspace restore
- hook/MCP/agent/config visibility
- secret masking for MCP configuration

WorkVault decision:

Generalize the identity chain:

```text
agent session ID
    + PID/PPID
    + TTY
    + terminal provider/session
    + CWD
    + Git repo/branch
    -> WorkVault runtime identity
```

Priority: `★★★★★`

### `claude-terminal`

Role: live multi-session UX and control-tower patterns.

Important patterns:

- multiple terminals per project
- terminal/chat cross-reference
- session recap
- session forking
- checkpoint/file rewind
- subagent visualization
- persistent Todos
- model changes during a conversation
- worktree-aware parallel tasks
- Control Tower for active agents across projects

WorkVault decision:

Separate the eventual interface into two views:

```text
HISTORY        what happened?
CONTROL TOWER  what is happening now?
```

Priority: `★★★★★`

### `git-ai`

Role: line/commit-level AI authorship and prompt/code attribution.

WorkVault decision:

Do not rebuild line-level AI attribution. Link WorkVault runs/sessions/artifacts/commits to Git-AI provenance where present.

Priority: `★★★★☆`

### `.qwen`

Role: Qwen-specific commands, hooks, agents, and integration surface.

WorkVault decision:

Create a dedicated Qwen adapter into the provider-neutral event model.

Priority: `★★★★☆`

### `obsidian-terminal`

Role: terminal provider/history patterns.

Important patterns:

- integrated terminals
- multiple profiles
- save/restore terminal history
- explicit terminal-history file export
- external iTerm2 profile support

WorkVault decision:

Use this to keep the terminal schema provider-neutral. iTerm2 is the first major sensor, not a hard dependency of the core model.

Priority: `★★★☆☆`

## Repos useful primarily as fixture/evidence sources

### `CoX-mod-Adventure`

Contains valuable real-world filesystem/application/session archaeology and is an excellent fixture source. It also exposed committed `.specstory/debug/**` traces.

Action already taken:

- ignore future `.specstory`, `.codex-history`, terminal histories, and conversation exports;
- preserve already tracked history until provenance/privacy audit is complete;
- track cleanup in a dedicated issue rather than bulk-delete.

### `agent-skills`

Contains reusable agent/skill material but also committed `.codex-history/**` files.

Action already taken:

- ignore new Codex/specstory/session-history exports;
- preserve already tracked history until inventory/privacy review;
- migrate useful provenance privately before removal.

## Lower-priority / adjacent repos

### `ai-command-hub`

Currently more useful as a UI/product shell than as WorkVault runtime architecture.

Priority: `★☆☆☆☆`

### `CityVault`

Despite the name, this is a City of Heroes server-control product rather than WorkVault infrastructure.

Priority for WorkVault reuse: `★☆☆☆☆`

### `terminal-workflows`

Little recoverable implementation was found during the audit.

Priority: `★☆☆☆☆`

## Existing public/private boundary

The historical `AvaTar-ArTs/iterm2` `.gitignore` already excluded a large set of local runtime and history state:

```text
.claude/
.codex-history/
.cursor/
.gemini/
.poolside/
.qodo/
.qwen/
Codex/
claude-ecosystem/
cursor-ecosystem/
gemini/
Session-History/
Session-History-Archive/
*.itermarchive
conversation-export*.json
agent handoff/session scratch files
credential-like files
```

That makes the old repository a useful negative map of the private local control plane.

WorkVault should preserve that split:

```text
GitHub repo
    portable brain

/Users/steven/iterm2
    living private nervous system
```

## Repository hygiene capability

`wv github-audit` now exists to find risky repository content before WorkVault begins deeper GitHub ingestion.

Current categories:

```text
SAFE_PUBLIC
REVIEW
PRIVATE_REFERENCE
SECRET_ROTATE
```

The audit is intentionally non-destructive. Existing committed histories are migration candidates, not automatic deletion targets.

## Adapter registry direction

```text
adapters/
  codex/
  claude/
  qwen/
  hermes/
  git_ai/
  terminals/
    iterm2/
    vscode/
    obsidian/
    claude_terminal/
    generic_pty/
```

Each adapter should emit provider-neutral observations/events and avoid embedding project/workstream inference inside the provider-specific layer.

## Main conclusion

WorkVault should not recreate the entire ecosystem.

The useful division is:

```text
existing hooks/providers
    observe and emit

WorkVault
    normalize and retain

WorkGraph
    correlate and explain

Workbench/Control Tower
    expose current/history views
```

The repositories already contain many of the organs. WorkVault is the connective tissue and durable memory system that makes them operate as one coherent whole.
