# tf2-wiki-mcp

An [MCP](https://modelcontextprotocol.io) server that exposes the [Team Fortress Wiki](https://wiki.teamfortress.com/) to LLM clients (Claude Desktop, Claude Code, Cursor, VS Code) over stdio.

[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=tf2-wiki-mcp&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=tf2-wiki-mcp&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D&quality=insiders)
[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D)
[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=tf2-wiki-mcp&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJ0ZjItd2lraS1tY3AiXSwiZW52Ijp7fX0=)

> **Not affiliated with Valve Corporation or the Team Fortress Wiki contributors.** Team Fortress 2 is a trademark of Valve Corporation. This is unofficial fan tooling.

## What it does

Gives an LLM live, accurate access to TF2 wiki content so it stops guessing at weapon stats, patch notes, and cosmetic details.

- **Generic wiki access** — search, fetch pages, get summaries, list recent changes.
- **TF2 domain tools** — structured weapon stats, class loadouts, cosmetic lookup, event item lists, patch notes.

### Tools

| Tool | Purpose |
|---|---|
| `search_wiki(query, limit)` | Full-text search |
| `get_page(title, format)` | Page content as `wikitext`, `plain`, or `html` |
| `get_page_summary(title)` | Lead-section plaintext |
| `get_page_sections(title)` | Section TOC for selective fetching |
| `get_recent_changes(limit, namespace)` | Recently edited pages |
| `get_weapon_stats(weapon_name)` | Parsed weapon infobox → structured stats |
| `list_class_loadout(class_name)` | All weapons in a class's wiki category |
| `get_cosmetic(name)` | Cosmetic item infobox params |
| `list_event_items(event_name)` | Items added in an update/event |
| `get_patch_notes(update_name)` | Patch notes for a specific update |

Plus: resource `tf2wiki://main`, prompts `analyze_loadout` and `compare_weapons`.

## Installation

Requires [`uv`](https://docs.astral.sh/uv/) (which manages the Python toolchain for you). Once installed, `uvx tf2-wiki-mcp` will fetch and run the server on demand — no manual clone needed.

**Standard config** works in most MCP clients:

```json
{
  "mcpServers": {
    "tf2-wiki-mcp": {
      "command": "uvx",
      "args": ["tf2-wiki-mcp"],
      "env": {}
    }
  }
}
```

<details>
<summary>Claude Desktop</summary>

Add the standard config above to `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop. The TF2 wiki tools appear in the tool picker.
</details>

<details>
<summary>Claude Code</summary>

```bash
claude mcp add tf2-wiki-mcp -- uvx tf2-wiki-mcp
```
</details>

<details>
<summary>Codex</summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.tf2-wiki-mcp]
command = "uvx"
args = ["tf2-wiki-mcp"]
```

See the [Codex MCP docs](https://github.com/openai/codex/blob/main/codex-rs/config.md#mcp_servers).
</details>

<details>
<summary>Cursor</summary>

[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=tf2-wiki-mcp&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJ0ZjItd2lraS1tY3AiXSwiZW52Ijp7fX0=)

Or add the standard config to `~/.cursor/mcp.json`.
</details>

<details>
<summary>Gemini CLI</summary>

Add the standard config to your Gemini CLI `settings.json` per the [Gemini CLI MCP guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md#configure-the-mcp-server-in-settingsjson).
</details>

<details>
<summary>VS Code</summary>

[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=tf2-wiki-mcp&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D)

Or via the VS Code CLI:

```bash
code --add-mcp '{"name":"tf2-wiki-mcp","command":"uvx","args":["tf2-wiki-mcp"],"env":{}}'
```

See the [VS Code MCP guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) for details.
</details>

<details>
<summary>VS Code Insiders</summary>

[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=tf2-wiki-mcp&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D&quality=insiders)

Or via the CLI:

```bash
code-insiders --add-mcp '{"name":"tf2-wiki-mcp","command":"uvx","args":["tf2-wiki-mcp"],"env":{}}'
```
</details>

<details>
<summary>Visual Studio</summary>

[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22tf2-wiki-mcp%22%5D%2C%22env%22%3A%7B%7D%7D)

Or manually:

1. Open the GitHub Copilot Chat window.
2. Click the tools icon (🛠️) → **+ Add Server**.
3. Fill in: **Server ID** `tf2-wiki-mcp`, **Type** `stdio`, **Command** `uvx`, **Arguments** `tf2-wiki-mcp`.
4. Save.

See the [Visual Studio MCP docs](https://learn.microsoft.com/visualstudio/ide/mcp-servers).
</details>

<details>
<summary>GitHub Copilot Coding Agent</summary>

```json
{
  "mcpServers": {
    "tf2-wiki-mcp": {
      "command": "uvx",
      "args": ["tf2-wiki-mcp"],
      "env": {},
      "type": "local",
      "tools": ["*"]
    }
  }
}
```

Add this in repository settings under **Copilot → Coding agent**. See the [Copilot Coding Agent MCP docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp).
</details>

## Development

Run from a local clone instead of PyPI:

```bash
git clone https://github.com/yusufaf/tf2-wiki-mcp
cd tf2-wiki-mcp
uv sync --dev
uv run pytest              # offline, uses recorded cassettes
uv run pytest --live       # also hits the real wiki
```

To point an MCP client at the local checkout:

```json
{
  "mcpServers": {
    "tf2-wiki-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/tf2-wiki-mcp", "tf2-wiki-mcp"]
    }
  }
}
```

## Licensing & Attribution

**Code:** MIT (see `LICENSE`).

**Wiki content:** Not redistributed. This project contains zero scraped wiki data. All page content is fetched live from `wiki.teamfortress.com` at the user's request and returned directly to the user's LLM client — the same posture as a browser extension.

Wiki content is © its respective contributors under Valve's [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/) (Game Site terms). Users of this tool are responsible for compliance with Valve's terms. **Code license ≠ content license**: MIT covers this codebase, not the wiki content it fetches.

Requests to the wiki include a descriptive `User-Agent` (`tf2-wiki-mcp/<version> (https://github.com/yusufaf/tf2-wiki-mcp)`) per MediaWiki etiquette and respect `maxlag`/`Retry-After` responses.

## Contributing

Don't check in scraped wiki text. Infobox *examples* for parser tests are fine (short, fair-use-grade fixtures). Full page dumps are not.
