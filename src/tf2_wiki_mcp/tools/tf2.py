"""Tier 2 TF2 domain-specific tools."""

from __future__ import annotations

from typing import Any, Literal

from fastmcp import FastMCP

from ..client import WikiClient
from ..parsers.weapon import extract_weapon_stats

CLASS_CATEGORY = {
    "scout": "Category:Scout",
    "soldier": "Category:Soldier",
    "pyro": "Category:Pyro",
    "demoman": "Category:Demoman",
    "heavy": "Category:Heavy",
    "engineer": "Category:Engineer",
    "medic": "Category:Medic",
    "sniper": "Category:Sniper",
    "spy": "Category:Spy",
}

ClassName = Literal[
    "scout", "soldier", "pyro", "demoman", "heavy",
    "engineer", "medic", "sniper", "spy",
]


def register(mcp: FastMCP, client: WikiClient) -> None:
    @mcp.tool
    async def get_weapon_stats(weapon_name: str) -> dict[str, Any]:
        """Fetch a weapon page and return structured stats parsed from its infobox.

        Returns damage, rate-of-fire, reload, clip size, attributes (+/- effects), etc.
        """
        data = await client.query(
            action="parse", page=weapon_name, prop="wikitext", redirects=1
        )
        parse = data.get("parse", {})
        wikitext = parse.get("wikitext") or ""
        stats = extract_weapon_stats(wikitext)
        return {
            "title": parse.get("title", weapon_name),
            "stats": stats,
            "found": stats is not None,
        }

    @mcp.tool
    async def list_class_loadout(class_name: ClassName) -> dict[str, Any]:
        """List all weapons for the given class.

        Intersects Category:<Class> with Category:Weapons on the wiki.
        """
        cat = CLASS_CATEGORY[class_name.lower()]
        data = await client.query(
            action="query",
            generator="categorymembers",
            gcmtitle=cat,
            gcmlimit=500,
            gcmtype="page",
            prop="categories",
            clcategories="Category:Weapons",
            cllimit=500,
        )
        pages = data.get("query", {}).get("pages", [])
        weapons = [
            p["title"]
            for p in pages
            if any(
                c.get("title") == "Category:Weapons" for c in p.get("categories", [])
            )
        ]
        return {
            "class": class_name,
            "category": cat,
            "weapons": sorted(weapons),
        }

    @mcp.tool
    async def get_cosmetic(name: str) -> dict[str, Any]:
        """Fetch a cosmetic item page and return its infobox params."""
        from ..parsers.infobox import parse_template

        data = await client.query(
            action="parse", page=name, prop="wikitext", redirects=1
        )
        parse = data.get("parse", {})
        wikitext = parse.get("wikitext") or ""
        params = parse_template(wikitext, "Item infobox")
        return {
            "title": parse.get("title", name),
            "infobox": params,
            "found": params is not None,
        }

    @mcp.tool
    async def list_event_items(event_name: str) -> dict[str, Any]:
        """List items added during a given TF2 event/update (e.g. 'Jungle Inferno Update', 'Smissmas 2023')."""
        category = f"Category:{event_name}"
        data = await client.query(
            action="query",
            list="categorymembers",
            cmtitle=category,
            cmlimit=200,
            cmtype="page",
        )
        members = data.get("query", {}).get("categorymembers", [])
        if not members:
            data = await client.query(
                action="query",
                list="search",
                srsearch=f'"{event_name}" items',
                srlimit=20,
            )
            return {
                "event": event_name,
                "source": "search_fallback",
                "items": [h["title"] for h in data.get("query", {}).get("search", [])],
            }
        return {
            "event": event_name,
            "category": category,
            "source": "category",
            "items": [m["title"] for m in members],
        }

    @mcp.tool
    async def get_patch_notes(update_name: str) -> dict[str, Any]:
        """Fetch patch notes for a named update or patch page (e.g. 'October 5, 2023 Patch')."""
        data = await client.query(
            action="query",
            prop="extracts",
            titles=update_name,
            explaintext=1,
            redirects=1,
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            return {"title": update_name, "notes": None, "found": False}
        page = pages[0]
        return {
            "title": page.get("title"),
            "notes": page.get("extract"),
            "found": "extract" in page,
        }
