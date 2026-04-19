# tf2-wiki-mcp

An [MCP](https://modelcontextprotocol.io) server that exposes the [Team Fortress Wiki](https://wiki.teamfortress.com/) to LLM clients (Claude Desktop, Claude Code, Cursor) over stdio.

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

## Install

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/yusufaf/tf2-wiki-mcp
cd tf2-wiki-mcp
uv sync
```

## Use with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tf2-wiki": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/tf2-wiki-mcp", "tf2-wiki-mcp"]
    }
  }
}
```

Restart Claude Desktop. The TF2 wiki tools appear in the tool picker.

## Use with Claude Code

```bash
claude mcp add tf2-wiki uv run --directory /absolute/path/to/tf2-wiki-mcp tf2-wiki-mcp
```

## Use with Cursor

Similar `mcpServers` entry in `~/.cursor/mcp.json` — same shape as the Claude Desktop config above.

## Development

```bash
uv sync --dev
uv run pytest              # offline, uses recorded cassettes
uv run pytest --live       # also hits the real wiki
```

## Licensing & Attribution

**Code:** MIT (see `LICENSE`).

**Wiki content:** Not redistributed. This project contains zero scraped wiki data. All page content is fetched live from `wiki.teamfortress.com` at the user's request and returned directly to the user's LLM client — the same posture as a browser extension.

Wiki content is © its respective contributors under Valve's [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/) (Game Site terms). Users of this tool are responsible for compliance with Valve's terms. **Code license ≠ content license**: MIT covers this codebase, not the wiki content it fetches.

Requests to the wiki include a descriptive `User-Agent` (`tf2-wiki-mcp/<version> (https://github.com/yusufaf/tf2-wiki-mcp)`) per MediaWiki etiquette and respect `maxlag`/`Retry-After` responses.

## Contributing

Don't check in scraped wiki text. Infobox *examples* for parser tests are fine (short, fair-use-grade fixtures). Full page dumps are not.
