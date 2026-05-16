# Defense 01 — Protect AI Instruction Files

Most teams already require security-team approval for `.github/workflows/`.
Extend the same protection to **every file the agent runtime loads as
instructions**. The list is longer than people expect:

- Repo root: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`
- Tool-specific dirs: `.claude/`, `.codex/`, `.agents/`, `.cursor/`
- Hooks: `.claude/hooks/`, `.git/hooks/` (usually local, but worth listing)
- Plugin/skill dirs: `.claude/skills/`, `.cursor/rules/`

See `CODEOWNERS` for a template you can drop into `.github/CODEOWNERS`.

## Why this isn't enough on its own

CODEOWNERS forces a human reviewer to see the change. That helps **only if**
the human reviewer knows that "this is a 3-line documentation tweak" might
actually be "a behavioral modification for every agent that touches the repo."
Pair this defense with the security-team training that goes along with it:
treat `AGENTS.md` changes the way you treat changes to a security tool's
config file.
