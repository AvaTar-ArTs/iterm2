# WorkVault security and privacy model

WorkVault deals with unusually sensitive evidence: terminal history, prompts, tool inputs/responses, repository state, absolute paths, agent session databases, shell snapshots, OAuth files, API keys, customer/project data, and private research.

The system therefore follows a local-first, reference-first model.

## Core rule

```text
capture locally
  -> classify
  -> redact/reference
  -> normalize
  -> index
  -> explicitly export
```

Never:

```text
capture everything -> commit everything
```

## Sensitivity classes

### PUBLIC

Intentionally publishable content.

### INTERNAL

Ordinary local project material that should not be assumed public.

### SENSITIVE

Terminal transcripts, private prompts, absolute local topology, personal/customer/project context, agent histories, shell snapshots, private research notes.

### SECRET

Credentials, API keys, tokens, passwords, OAuth secrets, private keys, authentication state.

### DO_NOT_INGEST

Material WorkVault should not copy into its managed content store, even locally, unless a later explicit design justifies it.

Examples:

- SSH private keys
- browser cookie stores
- credential keychains
- raw authentication databases
- hidden/private reasoning data from providers

Metadata such as path, existence, file size, mode, and cryptographic hash may be stored when safe and useful.

## Ownership modes

### MANAGED

WorkVault owns the managed artifact/evidence copy.

### REFERENCED

WorkVault stores metadata and a pointer/hash, while the source remains owned by another application or project.

### EPHEMERAL

Temporary observation/run artifact not intended for long-term retention.

Agent/runtime databases and large session stores should normally be `REFERENCED`.

## Secret detection

`wv github-audit` is the first implemented guardrail.

The scanner should:

- classify suspicious paths;
- scan appropriate text files for credential-like patterns;
- report file/rule/location;
- never print the matched secret value;
- support CI failure thresholds;
- prefer false-positive review over silent credential publication.

Secret detection is not proof that a credential is valid. A public committed credential-like value should be reviewed, and actual secrets should be rotated.

## Event logging redaction

Existing hooks such as `my-supremepowers/hooks/after-tool.sh` are useful prototypes but may receive sensitive tool inputs/responses.

Before WorkVault persists a canonical tool event, apply field-aware redaction/classification.

Recommended event storage pattern:

```json
{
  "tool": "...",
  "input_summary": "redacted/normalized summary",
  "input_hash": "...",
  "response_summary": "...",
  "sensitivity": "SENSITIVE",
  "raw_reference": "optional private reference",
  "exit_code": 0
}
```

Do not make raw tool-response storage the default.

## Conversation/session history

Raw conversation exports are historical evidence, not automatically public artifacts.

Recommended default:

```text
raw export
  ownership: REFERENCED
  sensitivity: SENSITIVE
  git policy: NEVER
```

Public test fixtures should be sanitized normalized events and expected answers, not raw private transcript dumps.

## Public repository hygiene

Patterns requiring review/private handling include:

```text
.codex-history/
.specstory/
Session-History/
Session-History-Archive/
conversation-export*
gemini-conversation-*
.claude/
.qwen/
.gemini/
.cursor/
.poolside/
.env*
credentials
auth files
shell snapshots
raw debug/session logs
```

Existing tracked history should not be deleted blindly. Migration sequence:

1. inventory;
2. secret/privacy scan;
3. preserve useful provenance privately by reference/hash;
4. generate sanitized public derivatives where useful;
5. remove raw tracked material from the current public tree;
6. rotate exposed credentials if actual secrets were committed;
7. evaluate Git history rewriting only when warranted.

## Evidence minimization

For external/private resources, prefer storing:

```text
canonical path or resource identifier
cryptographic hash
size/mtime when useful
sensitivity classification
source type
summary/derived facts
```

over copying the entire payload.

## Terminal capture

Full scrollback may contain passwords, tokens, private URLs, customer data, commands, and proprietary content.

Initial iTerm/terminal observation should capture metadata only:

```text
session/window/tab IDs
TTY
CWD
hostname
profile
foreground process
scrollback availability/size metadata
```

Full transcript capture should be a separate explicit policy with redaction and retention controls.

## Secrets locations

WorkVault may record that a secret is expected at a location such as `~/.env.d/...`, but should not ingest the secret value.

A resource could record:

```json
{
  "type": "secret_location",
  "path": "~/.env.d/example.env",
  "mode": "0600",
  "value_stored": false
}
```

## Write safety

Reading state and writing WorkVault's own database are different from mutating the observed world.

Future mutation commands should use explicit modes:

```text
read-only
prompt
approved-write
```

Anything that sends input to a terminal should be treated as command execution.

Anything that modifies a repo, filesystem, app configuration, profile, session, or external service should emit an auditable event with actor, reason, target, and result.

## User intent precedence

For personal intent, explicit user instructions override automated inference.

For example, if WorkVault infers a symlink should be canonical but the user says the live path must remain a real directory, the user's statement becomes the canonical semantic constraint until superseded.

## Public/private split for this repository

`AvaTar-ArTs/iterm2` should contain portable architecture, code, schemas, tests, and sanitized fixtures.

The living private control-plane state under `/Users/steven/iterm2` should remain local-first and be indexed/referenced by WorkVault rather than copied wholesale into GitHub.
