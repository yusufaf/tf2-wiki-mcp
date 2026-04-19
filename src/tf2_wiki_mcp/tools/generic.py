"""Tier 1 generic MediaWiki tools: search, page fetch, summary, sections, recent changes."""

from __future__ import annotations

from typing import Any, Literal

from fastmcp import FastMCP

from ..client import WikiClient


def register(mcp: FastMCP, client: WikiClient) -> None:
    @mcp.tool
    async def search_wiki(query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Full-text search the TF2 Wiki. Returns title + snippet + wordcount for each hit."""
        data = await client.query(
            action="query",
            list="search",
            srsearch=query,
            srlimit=min(max(limit, 1), 50),
        )
        hits = data.get("query", {}).get("search", [])
        return [
            {
                "title": h["title"],
                "snippet": _strip_html(h.get("snippet", "")),
                "wordcount": h.get("wordcount"),
                "size_bytes": h.get("size"),
            }
            for h in hits
        ]

    @mcp.tool
    async def get_page(
        title: str,
        format: Literal["wikitext", "plain", "html"] = "plain",
    ) -> dict[str, Any]:
        """Fetch a single TF2 Wiki page. `format` picks raw wikitext, plaintext extract, or rendered HTML."""
        if format == "wikitext":
            data = await client.query(action="parse", page=title, prop="wikitext")
            parse = data.get("parse", {})
            return {"title": parse.get("title"), "wikitext": parse.get("wikitext")}
        if format == "html":
            data = await client.query(action="parse", page=title, prop="text")
            parse = data.get("parse", {})
            return {"title": parse.get("title"), "html": parse.get("text")}
        data = await client.query(
            action="query",
            prop="extracts",
            titles=title,
            explaintext=1,
            redirects=1,
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            return {"title": title, "text": None}
        page = pages[0]
        return {"title": page.get("title"), "text": page.get("extract")}

    @mcp.tool
    async def get_page_summary(title: str) -> dict[str, Any]:
        """Lead-section plaintext summary of a page. Fast context anchor."""
        data = await client.query(
            action="query",
            prop="extracts",
            titles=title,
            exintro=1,
            explaintext=1,
            redirects=1,
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            return {"title": title, "summary": None}
        page = pages[0]
        return {"title": page.get("title"), "summary": page.get("extract")}

    @mcp.tool
    async def get_page_sections(title: str) -> dict[str, Any]:
        """Section table-of-contents for a page; use before get_page to fetch selectively."""
        data = await client.query(action="parse", page=title, prop="sections")
        parse = data.get("parse", {})
        return {
            "title": parse.get("title"),
            "sections": [
                {
                    "index": s.get("index"),
                    "level": int(s.get("level", 0)) if s.get("level") else None,
                    "line": s.get("line"),
                    "anchor": s.get("anchor"),
                }
                for s in parse.get("sections", [])
            ],
        }

    @mcp.tool
    async def get_recent_changes(
        limit: int = 20, namespace: int = 0
    ) -> list[dict[str, Any]]:
        """Recently edited pages in the given namespace (0 = main/articles)."""
        data = await client.query(
            action="query",
            list="recentchanges",
            rcnamespace=namespace,
            rclimit=min(max(limit, 1), 100),
            rcprop="title|timestamp|user|comment|ids",
        )
        return list(data.get("query", {}).get("recentchanges", []))


def _strip_html(s: str) -> str:
    import re

    return re.sub(r"<[^>]+>", "", s)
