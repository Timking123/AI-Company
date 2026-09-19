# Client compatibility

Documentation checked on 2026-09-19. The catalog covers 27 commonly encountered
coding-client entries, including one explicitly marked legacy product. It is a
maintained selection, not a market-share ranking or an exhaustive list of every
agent. Products can span more than one category.

This is a capability mapping, not a list of clients that passed an end-to-end
AI-Company runtime test. No row is runtime-certified by this repository. The kit
contains no client plugins, orchestration extensions, or automatic installers.

## Reading the protocol and running a company are separate capabilities

Any assistant able to read Markdown can use the role briefs and handoffs.
Automatic adoption also needs persistent tasks, observable identities,
manager-to-task communication, isolated writable workspaces, and candidate
verification. Check these in the actual installed host before declaring a team
active. [WORKFLOW.md](../WORKFLOW.md) defines the common contract.

## Terminal and desktop coding clients

| Client and instruction source | Entry point | Collaboration mapping and boundary |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | `AGENTS.md` | Follow [CODEX.md](CODEX.md); verify the installed client's durable-task, messaging, and worktree tools. |
| [Claude Code](https://code.claude.com/docs/en/memory) | This kit's `CLAUDE.md` imports `AGENTS.md` | [Agent teams](https://code.claude.com/docs/en/agent-teams) are experimental and cannot nest. Use independently coordinated lead sessions when needed. |
| [pi coding agent](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) | `AGENTS.md` or `CLAUDE.md`, subject to loading settings | Core omits subagents. Use a declared manual workflow or separately evaluated extensions and multiple instances. |
| [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/) | This kit's `GEMINI.md` imports `AGENTS.md`; context filenames are configurable | [Subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md) cannot spawn subagents. Check experimental worktrees and use independent lead sessions for additional levels. |
| [OpenCode](https://opencode.ai/docs/rules) | `AGENTS.md`; custom agent definitions | [Primary agents and subagents](https://opencode.ai/docs/agents) support delegation. Verify checkout isolation; do not mix older and V2 configuration schemas. |
| [Factory Droid](https://docs.factory.ai/harness/subagents) | `AGENTS.md` and `.factory/droids/` definitions | Parallel/background tasks are documented; subagents cannot delegate further. [CLI worktrees](https://docs.factory.ai/droid-cli/cli-reference) need explicit baseline and ownership checks. |
| [Aider](https://aider.chat/docs/usage/conventions.html) | Explicit `/read`, `--read`, or configured read-only Markdown | [Architect/editor mode](https://aider.chat/docs/usage/modes.html) is a staged pair of requests. Generic persistent parallel teams are not established by that feature; arrange separate sessions or manual handoffs. |
| [Amp](https://ampcode.com/docs/customize/agents-md) | `AGENTS.md` | [Agent-to-agent delegation](https://ampcode.com/docs/orbs/agent-to-agent) is documented across threads/projects. Verify manager routing and each workspace; do not infer unlimited nesting. |
| [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/) | `QWEN.md` and existing `AGENTS.md` | [Subagent modes](https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/) differ: forked agents share the parent directory and cannot delegate further. Explicitly verify worker mode and worktree allocation. |

## IDE and editor-centered clients

| Client and instruction source | Entry point | Collaboration mapping and boundary |
| --- | --- | --- |
| [Cursor](https://cursor.com/docs/rules) | `AGENTS.md` or `.cursor/rules/*.mdc` | [Parallel subagents](https://cursor.com/docs/subagents) do not imply separate filesystems. Request and verify isolated write environments. |
| [Windsurf / Devin Desktop](https://docs.devin.ai/desktop/cascade/agents-md) | `AGENTS.md`; current `.devin/rules/`, with legacy `.windsurf/rules/` compatibility | Windsurf documentation now redirects to Devin Desktop. [Cascade worktree sessions](https://docs.devin.ai/desktop/cascade/worktrees) require selecting isolation when starting the session. |
| [GitHub Copilot](https://docs.github.com/en/copilot/reference/custom-instructions-support) | `.github/copilot-instructions.md`; `AGENTS.md` support depends on the surface | [Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) documents fleet/delegation. IDE and CLI capabilities differ; check concurrency and depth limits. |
| [Cline](https://docs.cline.bot/customization/cline-rules) | `AGENTS.md`, `.clinerules/`, or `.cline/rules/` as supported | [Agent Teams](https://docs.cline.bot/cli/agent-teams) are documented for SDK/CLI/Kanban, not VS Code/JetBrains extensions. Do not advertise extension subagents as equivalent persistent teams. |
| [Kilo Code](https://kilo.ai/docs/customize/agents-md) | `AGENTS.md` | [Delegation](https://kilo.ai/docs/code-with-ai/agents/orchestrator-mode) supports parallel work, but independent context can share the directory. Use verified worktree sessions for independent writes. |
| [Continue](https://docs.continue.dev/customize/deep-dives/rules) | `.continue/rules/*.md` | [Agent mode](https://docs.continue.dev/ide-extensions/agent/quick-start) is documented. This review did not establish native hierarchical teams or automatic worktrees; use explicit session handoffs. |
| [Augment Code / Auggie](https://docs.augmentcode.com/setup-augment/guidelines) | `.augment/rules/`, `AGENTS.md`, or `CLAUDE.md` as supported | [Custom subagents](https://docs.augmentcode.com/cli/subagents) are documented for Auggie CLI. Do not infer the same delegation surface for the IDE; verify file isolation. |
| [Kiro](https://kiro.dev/docs/steering/) | `AGENTS.md` or `.kiro/steering/` | Check IDE, CLI, and cloud differences. Custom agents need steering resources explicitly configured; a role definition alone does not establish a running team. |
| [Google Antigravity](https://antigravity.google/docs/rules-workflows?tab=ide) | `.agents/rules/`; legacy `.agent/rules/` compatibility | [Agent management](https://www.antigravity.google/docs/cli/commands/agents) varies by surface. Verify actual identities, instruction inheritance, messaging, and isolated write scopes. |
| [TRAE / TraeCode](https://docs.trae.ai/ide/rules) | `.trae/rules/`; root `AGENTS.md` or Claude files through enabled import settings | Check which import toggles and rule activation modes are enabled. This review does not certify a persistent nested-team or messaging implementation. |
| [Qoder](https://docs.qoder.com/user-guide/rules) | `AGENTS.md` or `.qoder/rules/` | Project rules can take precedence over `AGENTS.md`. Verify loaded instructions and the selected client's task/delegation facilities before assigning roles. |
| [JetBrains Junie](https://junie.jetbrains.com/docs/guidelines-and-memory.html) | `.junie/AGENTS.md`, root `AGENTS.md`, or configured/legacy guidelines | [IDE selection order](https://junie.jetbrains.com/docs/junie-ide-plugin.html) can shadow the root file. Check the actual entry; do not assume custom roles are persistent concurrent sessions. |
| [Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html) | `.amazonq/rules/*.md` for IDE chat | Load a short project rule that directs the assistant to this protocol. The cited rule feature does not establish autonomous multi-level team management. |
| [ZCode by Z.ai](https://zcode.z.ai/en/docs/subagents) | Workspace `AGENTS.md`, or an explicit reading request | Parallel/background subagents cannot spawn subagents. Use independently coordinated primary lead sessions or a declared manual mapping. |

## Managed platforms and SDKs

| Client and instruction source | Entry point | Collaboration mapping and boundary |
| --- | --- | --- |
| [OpenHands](https://docs.openhands.dev/sdk/guides/skill) | SDK project context supports root `AGENTS.md` | [TaskToolSet](https://docs.openhands.dev/sdk/guides/task-tool-set) delegates/resumes tasks but is synchronous. This does not prove parallel scheduling or equivalent behavior in every OpenHands surface. |
| [Devin cloud](https://docs.devin.ai/onboard-devin/agents-md) | Project `AGENTS.md` | [Managed Devin sessions](https://docs.devin.ai/work-with-devin/advanced-capabilities) can be started, messaged, and monitored in isolated environments. Verify the hierarchy and authorization; this is separate from Devin Desktop. |
| [Replit Agent](https://docs.replit.com/features/project-setup/replit-dot-md) | Root `replit.md` | [Task-board work](https://docs.replit.com/features/agent/task-board) uses separate project copies and queues dependencies/capacity overflow. Confirm candidate identity and integration ownership; do not infer native nested teams. |

## Legacy reference

| Client | Historical entry | Status and boundary |
| --- | --- | --- |
| [Roo Code](https://roocodeinc.github.io/Roo-Code/) | Archived [mode instructions](https://roocodeinc.github.io/Roo-Code/features/custom-modes/) | The official site reports the extension shut down on May 15, 2026. Retained for users evaluating historical setups, not advertised as a current supported runner. |

The rows above describe documented building blocks. None is a claim that
copying this repository automatically reproduces the full hierarchy.

## Load one shared protocol

Use `AGENTS.md` directly where the installed client supports it. This kit also
ships thin `CLAUDE.md` and `GEMINI.md` imports. For another rule system, add a
short, authorized project-scoped instruction to read the kit's actual local
entry point, and verify that the model opens the full workflow. Follow that
client's rule activation settings; a Markdown link alone need not inject a file.

Do not overwrite existing rules, install extensions, enable experimental
features, or change global settings merely to make a compatibility row green.
Keep the full protocol in one place. A copy of a role prompt is not a new
runtime, a file lock, or a guarantee of instruction inheritance.

## Claude Code

The small [CLAUDE.md](../CLAUDE.md) import shares one rule source. The official
memory guide documents version- and setting-dependent direct `AGENTS.md`
loading and the `@AGENTS.md` import route. Verify loaded instructions rather
than assuming that a file elsewhere on disk is inherited. See the
[instruction-loading guide](https://code.claude.com/docs/en/memory).

The current [agent-team guide](https://code.claude.com/docs/en/agent-teams)
documents one team per session and no nested teams: teammates cannot spawn
their own teammates. A flat native team therefore cannot, by itself, implement
CTO -> leads -> workers as nested native teams. Separate top-level lead
sessions can be a mapping to evaluate, using supported cross-session messaging
or declared human relay. Check persistence, routing, and workspace ownership.
Do not silently flatten the manager relationships or enable experimental
features without the relevant authorization.

## ZCode

The official [subagent guide](https://zcode.z.ai/en/docs/subagents) describes
parallel and background work, while prohibiting subagents from spawning
subagents. It also documents default `AGENTS.md` injection from v3.7.1, with
exceptions such as built-in Explore and an explicit opt-out.

Give each role its brief and confirm receipt of project rules. A saved subagent
profile is not proof of a durable, user-visible lead task. For a three-level
company, evaluate separate primary sessions for leads and an explicit message
path. Mark unsupported or unverified steps as manual. These notes refer to
Z.ai's ZCode, not unrelated projects with the same name.

## pi coding agent

The current [upstream coding-agent README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md)
documents startup context files, extensibility, and the deliberate absence of
built-in subagents. It suggests separate instances or extensions for such
workflows. The earlier upstream repository address redirects to this project.

Reading `AGENTS.md` provides instructions, not an orchestration extension.
With multiple sessions, explicitly arrange task visibility, message delivery,
workspace isolation, and manager succession. An installed package must be
evaluated on its own; this repository does not endorse an untested extension.
Respect the host's context-loading and project-trust settings.

## Before marking a client supported in your project

1. Record the client/version, model, loaded rules, and required tool capabilities.
2. Create or reuse one bounded lead/worker assignment within authorization.
3. Read back its real identity and workspace; exchange a scoped status update.
4. Check single-writer ownership, a blocked dependency, and an explicit handoff.
5. Inspect the candidate and its evidence before marking the assignment done.

Record which steps ran and which were manual. If native nesting is unavailable,
make the alternative architecture explicit. Apply the same ownership policy
even when a host permits broader peer-to-peer messaging. Do not publish private
session logs to demonstrate compatibility.
