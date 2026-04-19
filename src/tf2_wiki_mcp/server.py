"""FastMCP server entrypoint for tf2-wiki-mcp."""

from __future__ import annotations

from fastmcp import FastMCP

from .client import WikiClient
from .tools import generic, tf2

INSTRUCTIONS = """\
Tools backed by the Team Fortress 2 Wiki (wiki.teamfortress.com).

Start with `search_wiki` to discover page titles, then `get_page_summary` for
quick context or `get_page` for full content. For weapons, prefer
`get_weapon_stats` which returns structured damage/attribute data. For class
overviews use `list_class_loadout`. Content is fetched live from the wiki.
"""


def build_server() -> FastMCP:
    mcp = FastMCP("tf2-wiki-mcp", instructions=INSTRUCTIONS)
    client = WikiClient()

    generic.register(mcp, client)
    tf2.register(mcp, client)

    @mcp.resource("tf2wiki://main")
    async def main_page() -> str:
        """Lead-section summary of the TF2 Wiki main page."""
        data = await client.query(
            action="query",
            prop="extracts",
            titles="Main Page",
            exintro=1,
            explaintext=1,
        )
        pages = data.get("query", {}).get("pages", [])
        return pages[0].get("extract", "") if pages else ""

    @mcp.prompt
    def analyze_loadout(
        class_name: str, primary: str, secondary: str, melee: str
    ) -> str:
        """Ask the model to evaluate a TF2 loadout using the wiki tools."""
        return (
            f"Evaluate this {class_name} loadout: primary={primary}, "
            f"secondary={secondary}, melee={melee}. Use `get_weapon_stats` "
            f"for each weapon. Discuss strengths, weaknesses, synergies, and "
            f"situations where it excels or struggles."
        )

    @mcp.prompt
    def compare_weapons(weapon_a: str, weapon_b: str) -> str:
        """Side-by-side comparison of two weapons using the wiki tools."""
        return (
            f"Compare {weapon_a} vs {weapon_b}. Call `get_weapon_stats` for "
            f"both, then present a side-by-side table of damage, rate of fire, "
            f"clip size, reload time, and listed attributes. Close with a "
            f"recommendation by playstyle."
        )

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
