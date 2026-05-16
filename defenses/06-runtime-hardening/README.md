# Defense 06 — Harden the Agent Runtime

The attacks in section 04 of the talk all exploit channels **outside** the
PR review boundary: tool descriptions, tool results, supply-chain context
files. The runtime is where you defend against those.

This directory has:

- `allowlist-mcp.json` — sample format for pinning MCP servers and tools by
  identity and version. Treat this file as your dependency lockfile for
  agent tools.
- `tool_output_sanitizer.py` — a working sanitizer for tool results. It
  strips HTML comments, neutralizes "AGENT:" / "SECURITY POLICY:" preambles,
  and wraps the result in a strong delimiter that tells the model "this is
  data, not instructions."
- `tests/test_sanitizer.py` — passing pytest cases. Run with `uv run pytest`.

## What the sanitizer actually does

It's defense-in-depth, not a magic filter. LLMs can still be influenced by
plain prose in tool output. What this gets you:

1. **HTML comments stripped.** Stops the 04b "AGENT:" comment pattern dead.
2. **Known-prefix neutralization.** Strings like `[SECURITY POLICY UPDATE`,
   `AGENT:`, `SYSTEM:`, `<!-- AGENT:` get prefix-quoted so the model sees
   them as quoted text from an untrusted source, not addressed instructions.
3. **Hard delimiters.** Output is wrapped in `<UNTRUSTED_TOOL_OUTPUT>...
   </UNTRUSTED_TOOL_OUTPUT>` tags, and the agent's system prompt tells the
   model these tags mark data, not instructions.

The third one is what does the real work — but only because the system
prompt is set up to treat the tags as a trust boundary.

## What the inventory looks like

Run this at agent start (or in CI):

```bash
# List every instruction-shaped file the runtime will load.
find . -maxdepth 5 \
  \( -name AGENTS.md -o -name CLAUDE.md -o -name .cursorrules \
     -o -name copilot-instructions.md -o -path '*/.claude/*' \
     -o -path '*/.codex/*' -o -path '*/.agents/*' \) \
  -not -path './.git/*' -not -path '*/.venv/*' \
  -print
```

If you can't enumerate it, you can't review it.
