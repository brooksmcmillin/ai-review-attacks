# 01: Context File Poisoning

`AGENTS.md` and `CLAUDE.md` files are dual-use: documentation for humans,
behavioral instructions for LLMs. A PR that edits them can:

- Add a section that **reframes** dangerous patterns as intentional ("legacy
  patterns, do not flag"). See `01a-selective-blindness/`.
- Hide instructions in **HTML comments** that disappear in rendered Markdown but stay
  in the raw file the model reads. See `01b-hidden-instructions/`.

Both work because the model is told, correctly, that project conventions are
authoritative. There is no separate channel for trusted vs untrusted project
conventions.

## Run it

```bash
uv run python attacks/01-context-files/run.py
```

The harness reviews the same vulnerable code twice: once with a clean
`AGENTS.md`, once with the poisoned one. It prints the two verdicts.
