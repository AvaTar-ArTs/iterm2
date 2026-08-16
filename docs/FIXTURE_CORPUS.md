# WorkVault golden fixture corpus

WorkVault should be evaluated against real, messy histories before it is trusted against a live terminal workspace.

The fixtures below came from actual working-session patterns reviewed during the WorkVault design conversation. Public fixtures must be sanitized. Raw/private evidence should remain local or private and be referenced by hash/path when needed.

## Fixture 1: Fiverr Seller OS tunnel lifecycle

Primary dimensions:

- implementation
- security
- deployment
- Git provenance
- test evidence
- interruption/resume

Expected reconstruction:

- project: Fiverr Seller OS
- workstream: Secure MCP Tunnel integration and Seller OS bootstrap
- tool annotation change
- tunnel-client installation
- first launch failure caused by treating `cd` as the executable
- wrapper-script remediation
- multiple verification/test runs
- credential exposure/remediation events
- migration of secret storage to `~/.env.d`
- ChatGPT app connection
- usage-limit interruption with unfinished work

Gold questions:

1. What caused the first tunnel launch failure?
2. Which artifact fixed it?
3. Which commit recorded the fix?
4. Where should tunnel credentials live after remediation?
5. Why was that policy introduced?
6. Were the MCP tests passing?
7. How many MCP tools were exposed?
8. Which state-changing tools were marked destructive?
9. What source produced the sanitized Seller OS explanation audit?
10. Was the raw ChatGPT export imported into Seller OS state?
11. What was the last verified state before the usage-limit interruption?
12. What remained to be done?

## Fixture 2: ESO Poseidon/Hermes chronology research

Primary dimensions:

- evolving user objective
- source provenance
- model changes
- research authority
- corrections
- machine-readable derivatives
- emergent skill creation

Expected reconstruction:

- temporary CWD: `~/eso-play`
- canonical artifact root: `/Users/steven/ESO`
- gameplay breakpoint: immediately before Infinite Archive
- primary route artifact and CSV derivative
- source hierarchy for UESP, ESO-Hub, guide sites, forums
- blocked sources retained as source leads but excluded from factual claims
- model epoch change to GPT-5.6-terra
- Writhing Wall correction
- citation-verification attempts and final passing state
- creation of a reusable `research-source-intake` capability
- unfinished `~/.agent-skills` creation request

Gold questions:

1. What was the user's actual gameplay breakpoint?
2. Which directory was temporary and which was canonical?
3. Which agent/runtime performed the research?
4. Which models were used during the session?
5. Which source hierarchy governed chronology claims?
6. Which sources were blocked by HTTP 403?
7. Were blocked sources used for factual claims?
8. What Markdown/CSV artifacts were produced?
9. What material correction changed the route later?
10. Which artifacts were patched because of that correction?
11. Did citation validation ultimately pass?
12. What new reusable skill emerged from the work?
13. What request remained unfinished at the end?

## Fixture 3: CoH / LaunchCat filesystem reconciliation

Primary dimensions:

- objective correction
- filesystem archaeology
- application state
- path topology
- drift
- content identity
- GUI actions
- queued follow-up

Expected reconstruction:

- initial `review` intent misclassified as code review
- corrected objective: analyze `/Users/steven/Library` for large disk consumers
- LaunchCat as a major Application Support consumer
- CoHModdingTool database as application-owned declared state
- tracked mod count versus actual filesystem count
- `/Applications/coh` symlink to LaunchCat's game root
- changing `assets/mods` topology across time
- user's rejection of linking live mods directly to the maker repo
- `FreedomTitleMusic.pigg` / `mod-197.pigg` content identity
- named package creation under `mods-mine`
- `coh-taku` documentation update
- config-layer distinction among game options, renderer settings, ReShade loader, and preset
- no remaining Wine/CoH background process at the checked point
- Homecoming forum research and queued `choake` profile/post follow-up

Gold questions:

1. Why did the initial code-review attempt fail?
2. What was the corrected user objective?
3. What were the largest Library consumers?
4. Which path does CoHModdingTool consider the game root?
5. Where does `/Applications/coh` actually point?
6. How many mods were tracked by the app database versus present on disk?
7. Was `assets/mods` a symlink at any point?
8. Did the user accept that as the final topology?
9. What is the canonical live mod folder after correction?
10. Which files are content-identical to `FreedomTitleMusic.pigg`?
11. What tool/database ID corresponds to that mod?
12. Which repos/artifacts were updated to package and document it?
13. Which config files operate at different semantic layers?
14. Were any Wine/CoH processes still running when checked?
15. What forum follow-up was queued but unfinished?

## Fixture 4: Marketplace background-agent productization

Primary dimensions:

- foreground plus background work
- parent/child runs
- research-to-product dependency
- commercialization provenance

Expected reconstruction:

- one productization workstream
- multiple background research runs such as competitive positioning, SEO/discoverability, and strategy
- existing generated marketplace variants
- later research feeding optimization of those artifacts

Gold questions:

1. Which background runs belonged to the same marketplace workstream?
2. Which artifacts existed before the research finished?
3. Which research outputs were intended to modify those artifacts?
4. Which product/repository/gig outputs were derived from earlier research?

## Fixture 5: Multi-agent iTerm2 ecosystem

Primary dimensions:

- many providers/runtimes
- local control plane
- histories and handoffs
- private/public boundary

Expected reconstruction:

- Claude, Codex, Cursor, Gemini, Qwen, Qodo and related operational roles
- session/history/archive stores
- agent operations and handoff material
- runtime directories that should be referenced rather than copied into Git
- distinction between public `AvaTar-ArTs/iterm2` and private `/Users/steven/iterm2`

Gold questions:

1. Which agent runtimes participate in the local control plane?
2. Which paths are runtime state versus portable source?
3. Which existing inventory/handoff artifacts are proto-WorkVault components?
4. What should be referenced rather than committed?

## Scoring dimensions

Each importer/extractor should be evaluated separately for:

```text
entity extraction
run/event extraction
temporal ordering
relationship extraction
path/location roles
artifact identity
current-state reconstruction
evidence classification
sensitive-data handling
handoff completeness
gold-question answer accuracy
```

Do not let a fluent final answer hide poor extraction. Retrieval/reconstruction completeness and final-answer accuracy should be scored independently.

## Public fixture policy

Raw source histories may contain secrets, private prompts, user/account identifiers, hidden model metadata, absolute paths, and tool responses.

Public fixture creation should therefore use:

```text
private/raw evidence
    -> scanner/redactor
    -> normalized event fixture
    -> expected state/relationships
    -> gold questions
```

Recommended public fixture structure:

```text
fixtures/
  fiverr-tunnel/
    events.jsonl
    expected-state.json
    expected-relations.json
    gold-questions.yaml
  eso-poseidon/
  coh-launchcat/
  marketplace-agents/
  multi-agent-iterm2/
```
