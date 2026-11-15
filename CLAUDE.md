Read AGENTS.md in this repository before doing anything. It contains the install steps, the repository map and the rules that must not be weakened.


## Toolchain log (mandatory)

- When any tool, SDK, toolchain, global package, driver, CLI, MCP server or skill is installed or first used for this project, add a row to `docs/TOOLCHAIN.md` in the same session: name, version, install command, why. Use a cheap subagent (haiku) for the edit.
- If `~/.claude/workspace-registry.txt` exists, also record it in the workspace registry with the `shreyas-workspace-replicate:log-tool` skill, so a new machine can be set up from it. Nothing gets installed untracked.
- When the stack changes (a tool is replaced), mark the old row "replaced by <new>" instead of deleting it.
