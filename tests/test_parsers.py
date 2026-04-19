from __future__ import annotations

from pathlib import Path

from tf2_wiki_mcp.parsers.infobox import parse_template
from tf2_wiki_mcp.parsers.weapon import extract_weapon_stats

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_template_extracts_named_params():
    wikitext = (FIXTURES / "scattergun_infobox.txt").read_text(encoding="utf-8")
    params = parse_template(wikitext, "Item infobox")
    assert params is not None
    assert params["slot"] == "primary"
    assert params["used-by"] == "Scout"
    assert params["clip-size"] == "6"


def test_parse_template_case_insensitive():
    wikitext = "{{item_infobox|slot=primary}}"
    assert parse_template(wikitext, "Item infobox") == {"slot": "primary"}


def test_parse_template_returns_none_when_missing():
    assert parse_template("no template here", "Item infobox") is None


def test_extract_weapon_stats_coerces_numbers_and_groups_attributes():
    wikitext = (FIXTURES / "scattergun_infobox.txt").read_text(encoding="utf-8")
    stats = extract_weapon_stats(wikitext)
    assert stats is not None
    assert stats["damage-max"] == 105
    assert stats["rof"] == 0.625
    assert stats["clip-size"] == 6
    assert "attributes" in stats
    assert any(a.startswith("+ ") for a in stats["attributes"])
    assert any(a.startswith("- ") for a in stats["attributes"])


def test_extract_weapon_stats_returns_none_without_infobox():
    assert extract_weapon_stats("just prose, no template") is None
