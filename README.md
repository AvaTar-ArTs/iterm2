# WorkVault

`AvaTar-ArTs/iterm2` is now the seed repository for **WorkVault**, a local-first terminal, AI-session, repository-provenance, and workspace-recovery system.

The original iTerm2-specific work remains part of the design, but iTerm2 is a sensor/provider rather than the entire product. WorkVault is intended to correlate terminal sessions, agent sessions, processes, repositories, branches, transcripts, tool events, artifacts, and provenance without making raw private history public by default.

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

- `SAFE_PUBLIC` — reserved for explicitly safe/exportable material
- `REVIEW` — logs, debug output, temp data, backups, or similar material requiring review
- `PRIVATE_REFERENCE` — AI/session/runtime history that should usually remain local or private
- `SECRET_ROTATE` — credential files or secret-like content requiring immediate review and likely credential rotation if committed publicly

The scanner reports **where** a secret-like signal was found, but deliberately does not echo the matched secret value.

## Signals currently recognized

Path-level signals include:

```text
.codex-history/
.specstory/
Session-History/
Session-History-Archive/
.claude/
.qwen/
.gemini/
.cursor/
.poolside/
.private-journal/
conversation exports
OAuth/credential files
.env files
logs/debug/temp/backups
```

Content-level rules currently recognize common OpenAI-style keys, GitHub tokens, AWS access-key IDs, private-key blocks, and generic secret assignments.

## Why this exists

A terminal window is a control room, not an archive. WorkVault separates:

```text
SESSION       historical execution environment
WORKSTREAM    coherent chunk of activity inside/between sessions
PROJECT       canonical long-lived project
ARTIFACT      produced file, commit, image, document, dataset, prompt, etc.
RELATIONSHIP  why one thing exists because of another
```

The target runtime identity is designed to correlate:

```json
{
  "session_id": "workvault-id",
  "provider_session_id": "agent-native-id",
  "agent": "codex|claude|qwen|hermes|...",
  "model": "provider/model",
  "pid": 1234,
  "ppid": 987,
  "tty": "/dev/ttys016",
  "terminal_provider": "iterm2",
  "terminal_session_id": "native-terminal-id",
  "cwd": "/path/to/project",
  "repo": "owner/repo",
  "branch": "main"
}
```

## Architecture direction

```text
                    WORKVAULT
                       |
        +--------------+--------------+
        |              |              |
     SENSORS        SEMANTICS       STORAGE
        |              |              |
 iTerm Python     project        SQLite/FTS5
 shell hooks      workstream      JSONL
 process tree     agent           Markdown
 Git              task            transcripts
 tmux             provenance      artifacts
 agent hooks      relationships   Git references
        |              |              |
        +--------------+--------------+
                       |
                   INTERFACES
             CLI / HTML / MCP
             iTerm status bar
             context menus
             provenance graph
```

Planned adapter families:

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
    generic_pty/
```

## Existing ecosystem pieces to integrate, not reinvent

- `my-supremepowers`: canonical hook/event/control logic
- `my-codex`: thin Codex runtime bridge
- `claude-manager`: session discovery/resume/search patterns
- `claude-terminal`: Control Tower, session recap, subagent/worktree UX patterns
- `git-ai`: prompt/code/commit authorship provenance
- `.qwen`: Qwen commands/hooks/agent surface
- `obsidian-terminal`: terminal-history/provider patterns

## Safety model

WorkVault is local-first. Raw terminal scrollback, prompts, tool responses, OAuth files, API keys, session databases, and agent histories are considered private evidence unless explicitly exported.

The guiding rule is:

```text
capture locally -> classify -> redact -> normalize -> index -> explicitly export
```

not:

```text
capture -> commit everything
```

## Immediate build sequence

1. `github-audit` repository hygiene scanner ✅
2. `doctor` read-only iTerm2/window/tab/pane/process/repo inventory
3. canonical event schema + redaction pipeline
4. Codex/Claude/Qwen/Hermes adapters
5. snapshot/checkpoint format
6. SQLite + FTS catalog
7. handoff generation
8. restore/recovery flow
9. iTerm status bar + context-menu controls
10. HTML/MCP/provenance interfaces

No destructive cleanup of previously committed session history is performed automatically. Existing history should be audited, migrated to private/local evidence storage, and only then removed from public repository history when appropriate.
