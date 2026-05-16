# 04: Agent Runtime Compromise

The first three categories target the repo. Category 4 targets the layer the
agent runs on: MCP servers, tool descriptions, tool outputs, and the supply
chain that ships them. These flow into the model the same way `AGENTS.md` does,
but they live **outside** the PR review boundary.

- `04a-mcp-description-injection/`: an MCP server lists a `fetch_docs` tool
  whose `description` field is the prompt injection.
- `04b-tool-output-injection/`: `fetch_docs` returns an attacker-controlled
  HTML page. The body contains instructions addressed to the model.
- `04c-supply-chain/`: a poisoned `.cursorrules` file inside a node_modules
  package, which IDEs and agents may auto-discover.

## Run it

```bash
uv run python attacks/04-runtime-compromise/run.py
```
