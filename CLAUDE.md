# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A FastMCP stdio server (~500 lines of Python) exposing the [Team Fortress Wiki](https://wiki.teamfortress.com/) to LLM clients, so a model stops guessing at weapon stats and patch notes. Published to PyPI and run via `uvx tf2-wiki-mcp`.

Unofficial fan tooling — not affiliated with Valve or the wiki's contributors. Keep that disclaimer in the README.

## Commands

```bash
uv sync                  # install, including dev group
uv run pytest            # offline tests (parsers + server construction)
uv run pytest --live     # also hits the real wiki
uv run tf2-wiki-mcp      # run the stdio server directly
```

Anything marked `@pytest.mark.live` is skipped unless `--live` is passed. The offline suite must stay network-free.

## Layout

```
src/tf2_wiki_mcp/
  server.py            # build_server() -> FastMCP; INSTRUCTIONS; resource + prompts
  client.py            # WikiClient — async httpx wrapper over MediaWiki api.php
  tools/generic.py     # search_wiki, get_page, get_page_summary, get_page_sections, get_recent_changes
  tools/tf2.py         # get_weapon_stats, list_class_loadout, get_cosmetic, list_event_items, get_patch_notes
  parsers/infobox.py   # wikitext template -> dict of params
  parsers/weapon.py    # infobox params -> structured weapon stats
```

`build_server()` instantiates one shared `WikiClient` and passes it into each module's `register(mcp, client)`. Tools take the client by injection rather than reaching for a global, which is what lets tests build a server without opening a connection.

## Architecture

**Two tool tiers, deliberately.** `tools/generic.py` is a thin MediaWiki passthrough — it works for any page and never assumes TF2 structure. `tools/tf2.py` is domain-specific and returns *parsed* data. When the wiki changes its templates, generic tools keep working and only the TF2 tier breaks. Put anything schema-dependent in the TF2 tier; keep the generic tier dumb.

**`WikiClient.query()` is the only way to reach the API.** It merges in `format=json`, `formatversion=2`, and `maxlag`, then retries once on 429 / `Retry-After` with a capped sleep. MediaWiki's `maxlag` is a politeness protocol — under replication lag the API asks clients to back off, and ignoring it gets you blocked. A `WikiError` is raised for API-level errors (which arrive with HTTP 200 and an `error` key, so `raise_for_status()` alone is not enough).

**Parsing is two-stage: wikitext → params → stats.** `parsers/infobox.py` uses `mwparserfromhell` to pull a template's parameters into a flat dict. `parsers/weapon.py` then interprets those params. This split matters because wiki editors rename and reorder infobox params constantly — a break is almost always in the interpretation stage, not the extraction stage, and the two are separately testable. `tests/test_parsers.py` runs on captured wikitext fixtures, so parser changes are verifiable without touching the network.

**Content is fetched live, never cached.** Wiki content changes (patch notes especially), and staleness is worse than latency here.

**The server ships prompts and a resource, not just tools.** `analyze_loadout` and `compare_weapons` are prompt templates that instruct the model to call the tools; `tf2wiki://main` is a resource. These are part of the public surface — changing their signatures breaks client configs.

## Conventions

- `from __future__ import annotations` everywhere; modern builtin generics.
- The `INSTRUCTIONS` string in `server.py` is prompt surface — it steers the model's tool-selection order (`search_wiki` first to discover titles, then summary or full page). Update it when tool semantics change.
- The `USER_AGENT` embeds the version and repo URL. MediaWiki requires a descriptive UA; don't genericize it.
- `version` lives in `pyproject.toml` and is re-exported as `__version__`. `release-please-config.json` is present — don't hand-bump.
- README carries per-client install blocks (VS Code, Cursor, Claude Desktop) with base64/URL-encoded configs. If the package name or args change, those badges all need regenerating.
