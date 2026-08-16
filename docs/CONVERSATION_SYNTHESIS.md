# WorkVault conversation synthesis

This document records the design conclusions that emerged from reviewing the full terminal/session-management conversation and the real histories used as examples. It is a distilled engineering record, not a raw conversation dump.

## Problem statement

A terminal window is a temporary control room. It is not a durable archive, project model, provenance graph, or reliable handoff mechanism.

The system needs to answer questions such as:

- What was happening in each terminal/agent session?
- Which project and workstream did that activity belong to?
- What files, commits, reports, images, research, or products were produced?
- What changed over time, including corrections and failed assumptions?
- Which facts were observed directly versus inferred by an agent?
- What is unsafe to close?
- Why does an artifact exist, and what earlier work produced it?
- What was interrupted and what should resume next?

The resulting system is **WorkVault**: a local-first observation, provenance, history, and recovery layer for multi-agent creative and engineering work.

## Real fixtures that shaped the design

### Fiverr Seller OS

The Fiverr transcript contains a full engineering lifecycle:

- MCP server/tool annotations
- OpenAI Secure MCP Tunnel setup
- installer and shell-script creation
- repeated test/verification runs
- Git commits
- tunnel launch failures and remediation
- credential exposures and secret-storage redesign
- ChatGPT app connection
- profile bootstrap
- work interruption caused by usage limits

Important lessons:

1. A transcript contains state transitions, incidents, decisions, verification, and unresolved work, not just dialogue.
2. `finding -> patch -> test -> commit` is a first-class provenance chain.
3. Statements of intent are weaker evidence than tool/test/runtime observations.
4. Session termination does not imply workstream completion.
5. Security incidents and durable policies must survive beyond the transcript that produced them.

### ESO / Poseidon / Hermes chronology research

The ESO transcript contains a research lifecycle:

- evolving objective and user-provided gameplay breakpoint
- source discovery and source hierarchy
- primary, secondary, supplementary, excluded, and blocked sources
- model switch during the same session
- generated Markdown and CSV artifacts
- citation validation attempts
- material correction to the Writhing Wall interpretation
- source-audit documents
- a new reusable research skill emerging from the work

Important lessons:

1. Objectives can be refined in-place without creating a new project.
2. `cwd` is not necessarily the canonical project/artifact root.
3. Research provenance requires source status, authority, claim usage, and exclusions.
4. Corrections must be temporal. The system should retain both the earlier belief and the later verified state.
5. Agent/model changes belong in run provenance.
6. Work can produce new reusable capabilities (skills), not only project files.

### CoH / LaunchCat / CoHModdingTool / Codex

The CoH transcript contains a filesystem/application-state lifecycle:

- ambiguous `review` request misclassified as code review
- broad home-directory scan producing high noise
- disk-usage analysis
- application-specific database inspection
- comparison of declared mod state versus filesystem state
- symlink creation/removal and changing canonical-path decisions
- hash-based artifact identity
- packaging a live mod into a named source package
- configuration-layer comparison
- process checks
- current forum research and queued follow-up work

Important lessons:

1. Objective correction is different from objective refinement.
2. Paths have temporal state: directory, missing, symlink, recreated directory, etc.
3. App-declared state and filesystem-observed state can drift.
4. User assertions of canonicality override agent assumptions about folder roles.
5. SHA-256/content identity should be separate from filename identity.
6. Configuration files need semantic layer metadata; not every pair of configs is directly comparable.
7. GUI actions and queued follow-ups are part of session history.

### Marketplace / multi-agent histories

Earlier histories show foreground work plus background research agents whose outputs feed product listings, pricing, SEO, and later artifacts.

Important lessons:

- background/queued/detached execution is a first-class `RUN` mode
- runs may form parent/child trees
- one workstream may span several agents/providers
- research can flow into commercial products and marketplace artifacts

### Existing `/Users/steven/iterm2` ecosystem

The older iTerm2 work already contained proto-WorkVault concepts:

- `Session-History/`
- `Session-History-Archive/`
- conversation exports
- inventory reports
- handoffs
- agent operations
- Claude/Codex/Qwen/Gemini/Cursor/Qodo runtime trees
- sort plans and TODO aggregation

The old GitHub repo's `.gitignore` is effectively a negative map of this private local control plane. It shows that private runtime evidence and public portable code were already being separated conceptually.

## Final core ontology

The conversation initially produced many useful concepts. The design was simplified so those concepts do not become dozens of database entity types.

Only six durable core entities are required:

```text
PROJECT
WORKSTREAM
SESSION
RUN
ARTIFACT
RESOURCE
```

Definitions:

- **PROJECT**: long-lived canonical effort or product.
- **WORKSTREAM**: coherent objective within/across projects and sessions.
- **SESSION**: working context from a terminal, agent, chat, IDE, or related surface.
- **RUN**: one execution inside a session, including foreground, background, queued, detached, or scheduled activity.
- **ARTIFACT**: produced or materially modified output: source code, commit, image, report, dataset, configuration, skill, package, etc.
- **RESOURCE**: observed/referenced dependency that WorkVault does not necessarily own: URLs, applications, repositories, paths, processes, databases, models, agents, endpoints, credentials locations.

Everything else is represented as typed events, relationships, evidence, or materialized views.

## Event model

Examples:

```text
objective.created
objective.refined
objective.corrected

session.started
session.interrupted
session.completed

run.started
run.failed
run.completed

artifact.created
artifact.modified
artifact.verified

claim.created
claim.corrected
claim.rejected

decision.recorded
decision.superseded

incident.detected
incident.remediated

path.created
path.deleted
path.symlinked
path.replaced

drift.detected
drift.resolved

source.discovered
source.retrieved
source.blocked
source.used
source.excluded

model.changed
milestone.reached
followup.queued
followup.resolved
```

Events preserve history. Current state is generated by reducers/materialized views.

## Temporal model

WorkVault should be bi-temporal where practical:

- `observed_at`: when WorkVault learned a fact
- `valid_from` / `valid_to`: when the fact was true in the outside world

This supports queries such as:

- What is true now?
- What did WorkVault believe at a previous point?
- When did a path stop being a symlink?
- When did a security policy change?
- Which claim was later corrected?

## Evidence model

Observations, assertions, inference, and verification are not interchangeable.

Recommended evidence classes:

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

For machine state, direct observation generally outranks inference. For personal intent, explicit user statements outrank all automated interpretation. For research, primary/source evidence outranks synthesis or inference.

## Relationship model

Relationships are generic and first-class:

```text
produced
derived_from
supports
contradicts
corrects
replaces
supersedes
same_content_as
references
configured_by
managed_by
installed_at
documented_in
verified_by
committed_as
commercialized_as
inspired
continues
```

This is the connective tissue that turns session storage into provenance.

## Conversation ingestion model

Conversation/session import uses three layers:

```text
1. raw/reference evidence
2. normalized provider-neutral events
3. semantic extraction
```

Raw evidence remains immutable when retained. Semantic extraction can be rerun later with a newer parser without rewriting history.

Provider-specific importers should normalize into one canonical schema:

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

## Location roles

A project may span several locations. Never assume one `project.path` is enough.

Typical roles:

```text
canonical_repo
runtime
artifact_root
source_root
session_store
secrets
cache
external_install
```

Examples from the fixtures:

- ESO terminal CWD: `~/eso-play`; canonical artifacts: `/Users/steven/ESO`
- CoH runtime: LaunchCat application support; maker repo: `CoX-mod-Adventure`; player docs: `coh-taku`
- Fiverr canonical repo: `/Users/steven/fiverr`; secrets: `~/.env.d`; tunnel profile: `~/.config/tunnel-client`

## Drift detection

`wv doctor` should compare expected/declared state with observed state.

Examples:

```text
expected 284 installed mods    observed 487 files
expected one tunnel daemon     observed two listeners
expected clean repository      observed dirty tree
expected active agent          observed missing process
expected session integration   observed unavailable metadata
```

Drift is a first-class event, not merely a warning string.

## Security model

Ingestion is not equivalent to copying.

Pipeline:

```text
discover
  -> classify sensitivity
  -> reference / redact / ingest
  -> normalize
  -> index
  -> explicitly export
```

Sensitivity classes:

```text
PUBLIC
INTERNAL
SENSITIVE
SECRET
DO_NOT_INGEST
```

Artifact ownership modes:

```text
MANAGED
REFERENCED
EPHEMERAL
```

WorkVault should default to reference-only for large or sensitive external state such as agent databases, raw terminal history, shell snapshots, and private conversation stores.

## Generated views, not canonical truth

These are projections and may be regenerated:

```text
HANDOFF.md
INDEX.md
catalog.csv
HTML dashboard
status summaries
```

Canonical durable state should be events, relationships, evidence, Git references, and indexed storage.

## Terminal architecture

iTerm2 remains important, but it is a sensor/provider rather than the WorkVault core.

The first iTerm adapter should only emit observations such as:

```text
session.created
session.closed
session.focused
session.cwd_changed
session.foreground_process_changed
```

with identifiers such as window/tab/session/TTY/CWD/profile/hostname/foreground process.

Project, agent, workstream, and repo inference belongs in WorkVault core.

Long-term terminal providers may include:

```text
iTerm2
VS Code terminal
Obsidian terminal
Claude Terminal
tmux
generic PTY
```

## Existing systems to integrate

Do not rebuild everything.

- `my-supremepowers`: hook/event/control-plane logic; already emits tool-use JSONL
- `my-codex`: thin Codex runtime bridge and session/tool hooks
- `claude-manager`: session ID + PID mapping, resume/search/restore patterns
- `claude-terminal`: Control Tower, subagent tree, recap, fork/checkpoint/worktree UX
- `.qwen`: Qwen commands/hooks/agents
- `git-ai`: prompt/code/commit attribution
- `obsidian-terminal`: terminal history/provider patterns

WorkVault's role is normalization, correlation, temporal state, and provenance across these systems.

## Revised implementation order

The conversation changed the build order. Build the brain against existing transcripts before connecting to the giant live iTerm2 workspace.

```text
01  canonical schemas
02  SQLite + JSONL storage
03  event ingestion
04  generic terminal transcript importer
05  Codex importer
06  Hermes/Poseidon importer
07  import real fixture corpus
08  temporal reducers/current-state views
09  provenance relationships
10  gold-query evaluation harness
11  wv inspect
12  wv history
13  wv resume
14  static HTML dashboard
15  read-only iTerm observer
16  TTY -> process -> cwd -> Git correlation
17  agent detectors
18  shell hooks
19  status bar
20  checkpoint generation
21  MCP read layer
22  carefully gated write/actions
23  embeddings/semantic search only if needed
```

`wv github-audit` exists first because public-repository hygiene was an immediate risk discovered during the audit. The next architectural milestone should be `wv ingest`, not autonomous terminal mutation.

## Evaluation principle

Real histories are the golden corpus. Synthetic `project-a` examples are insufficient.

A successful parser is judged by whether it can reconstruct causal and current state accurately enough to answer questions from the fixture corpus without rereading entire transcripts.
