"""Thin async wrapper around the TF2 Wiki's MediaWiki api.php."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from . import __version__

API_URL = "https://wiki.teamfortress.com/w/api.php"
USER_AGENT = (
    f"tf2-wiki-mcp/{__version__} (https://github.com/yusufaf/tf2-wiki-mcp)"
)
DEFAULT_MAXLAG = 5
DEFAULT_TIMEOUT = 30.0


class WikiError(RuntimeError):
    """Raised when the MediaWiki API returns an error or is unreachable."""


class WikiClient:
    def __init__(
        self,
        api_url: str = API_URL,
        user_agent: str = USER_AGENT,
        maxlag: int = DEFAULT_MAXLAG,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._api_url = api_url
        self._maxlag = maxlag
        self._client = httpx.AsyncClient(
            headers={"User-Agent": user_agent, "Accept": "application/json"},
            timeout=timeout,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "WikiClient":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def query(self, **params: Any) -> dict[str, Any]:
        """Call api.php with the given params; returns parsed JSON."""
        merged: dict[str, Any] = {
            "format": "json",
            "formatversion": "2",
            "maxlag": self._maxlag,
            **params,
        }
        for attempt in range(2):
            resp = await self._client.get(self._api_url, params=merged)
            if resp.status_code == 429 or resp.headers.get("Retry-After"):
                wait = float(resp.headers.get("Retry-After", "1"))
                await asyncio.sleep(min(wait, 10.0))
                if attempt == 0:
                    continue
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                err = data["error"]
                raise WikiError(f"{err.get('code')}: {err.get('info')}")
            return data
        raise WikiError("MediaWiki API repeatedly asked us to back off")
