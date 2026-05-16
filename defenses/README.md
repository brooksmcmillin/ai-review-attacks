# defenses/

Six defenses, in increasing order of "how much production engineering does this
cost." All six work better together than any one does alone, but the first two
are the best starting points.

| #   | Defense                              | Cost     | What it stops                         |
| --- | ------------------------------------ | -------- | ------------------------------------- |
| 01  | CODEOWNERS for AI-instruction files  | minutes  | Context file poisoning (01a, 01b)     |
| 02  | Security invariant tests             | hours    | Most policy bypasses (01, 02, 04c)    |
| 03  | Security rules outside LLM context   | days     | Anything that relies on LLM judgment  |
| 04  | Architectural patterns               | weeks    | Multi-layer compromise paths          |
| 05  | Human-in-the-loop checklist          | ongoing  | What AI is blind to (e.g., runtime)   |
| 06  | Runtime hardening (MCP, tool output) | days     | Section 04 attacks at the agent layer |

Each subdirectory has working sample code where applicable. Defenses 02 and 06
have actual passing pytest suites you can run:

```bash
uv run pytest
```
