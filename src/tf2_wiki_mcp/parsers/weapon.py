"""Weapon-specific normalization on top of the generic infobox parser."""

from __future__ import annotations

import re
from typing import Any

from .infobox import parse_template

WEAPON_TEMPLATE_NAMES = ("Item infobox", "Weapon infobox")

_NUMERIC_KEYS = {
    "damage",
    "damage-max",
    "damage-min",
    "damage-crit",
    "damage-minicrit",
    "rof",
    "reload",
    "clip-size",
    "ammo-loaded",
    "ammo-carried",
    "healed",
}


def extract_weapon_stats(wikitext: str) -> dict[str, Any] | None:
    """Parse a weapon page's wikitext into a structured dict.

    Returns None if no recognizable item/weapon infobox is present.
    """
    params: dict[str, str] | None = None
    for name in WEAPON_TEMPLATE_NAMES:
        params = parse_template(wikitext, name)
        if params:
            break
    if not params:
        return None

    result: dict[str, Any] = {}
    attributes: list[str] = []
    for key, value in params.items():
        k = key.lower()
        if k in _NUMERIC_KEYS:
            result[k] = _coerce_number(value)
        elif k.startswith("att-") and k.endswith("-positive"):
            attributes.append(f"+ {value}")
        elif k.startswith("att-") and k.endswith("-negative"):
            attributes.append(f"- {value}")
        elif k.startswith("att-") and k.endswith("-neutral"):
            attributes.append(f"~ {value}")
        else:
            result[k] = value
    if attributes:
        result["attributes"] = attributes
    return result


def _coerce_number(value: str) -> Any:
    cleaned = re.sub(r"[,\s]", "", value)
    m = re.match(r"^-?\d+(?:\.\d+)?", cleaned)
    if not m:
        return value
    token = m.group(0)
    try:
        return int(token) if "." not in token else float(token)
    except ValueError:
        return value
