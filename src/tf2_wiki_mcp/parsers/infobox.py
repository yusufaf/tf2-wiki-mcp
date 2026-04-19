"""Generic {{Item infobox}} / template parameter extraction using mwparserfromhell."""

from __future__ import annotations

import mwparserfromhell


def parse_template(wikitext: str, template_name: str) -> dict[str, str] | None:
    """Return the first matching template's named params as a dict of trimmed strings.

    Template name match is case-insensitive and underscore/space-insensitive.
    Returns None if no matching template is found.
    """
    code = mwparserfromhell.parse(wikitext)
    target = _normalize(template_name)
    for tmpl in code.filter_templates():
        if _normalize(str(tmpl.name)) == target:
            return {
                str(p.name).strip(): str(p.value).strip()
                for p in tmpl.params
                if not str(p.name).strip().isdigit() or str(p.value).strip()
            }
    return None


def _normalize(s: str) -> str:
    return s.strip().lower().replace("_", " ")
