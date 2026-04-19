"""Smoke: server constructs and registers the expected tool surface."""

from __future__ import annotations

import pytest

from tf2_wiki_mcp.server import build_server

EXPECTED_TOOLS = {
    "search_wiki",
    "get_page",
    "get_page_summary",
    "get_page_sections",
    "get_recent_changes",
    "get_weapon_stats",
    "list_class_loadout",
    "get_cosmetic",
    "list_event_items",
    "get_patch_notes",
}


async def test_server_exposes_all_ten_tools():
    mcp = build_server()
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    missing = EXPECTED_TOOLS - names
    assert not missing, f"missing tools: {missing}"


async def test_server_exposes_prompts_and_resource():
    mcp = build_server()
    prompts = await mcp.list_prompts()
    resources = await mcp.list_resources()
    prompt_names = {p.name for p in prompts}
    resource_uris = {str(r.uri) for r in resources}
    assert {"analyze_loadout", "compare_weapons"} <= prompt_names
    assert "tf2wiki://main" in resource_uris


@pytest.mark.live
async def test_live_search_smoke():
    """Real network hit — only runs with --live."""
    from fastmcp import Client

    mcp = build_server()
    async with Client(mcp) as client:
        result = await client.call_tool("search_wiki", {"query": "Scout", "limit": 3})
        data = result.data
        assert isinstance(data, list)
        assert len(data) > 0
        assert all("title" in hit for hit in data)
