"""
Shared authentication and Graph API client for msgraph-explore scripts.

This module is imported by fetch.py and search.py — it is not a standalone script.
"""

from __future__ import annotations

import sys
from functools import cache
from pathlib import Path
from typing import Any

import httpxyz as httpx
import orjson
from dotenv import dotenv_values
from msal import PublicClientApplication

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
NOTES_SCOPES = ("Notes.Read.All", "Sites.Read.All")
DRIVE_SCOPES = ("Files.Read.All", "Sites.Read.All")
SEARCH_SCOPES = ("Sites.Read.All", "Files.Read.All")
CACHE_ROOT = Path.home() / ".cache" / "msgraph-explore"
DEFAULT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


class AuthError(Exception):
    """Authentication or token acquisition failure."""


class GraphApiError(Exception):
    """Microsoft Graph API returned an error response."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        url: str,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.url = url
        super().__init__(
            f"Graph API {status_code} ({error_code}) on {url}: {message}"
        )


def _update_env_refresh_token(env_path: Path, new_token: str) -> None:
    if not env_path.exists():
        return

    lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)
    found = False
    with env_path.open("w", encoding="utf-8") as handle:
        for line in lines:
            if line.startswith("MICROSOFT_REFRESH_TOKEN="):
                handle.write(f"MICROSOFT_REFRESH_TOKEN={new_token}\n")
                found = True
            else:
                handle.write(line)
        if not found:
            if lines and not lines[-1].endswith("\n"):
                handle.write("\n")
            handle.write(f"MICROSOFT_REFRESH_TOKEN={new_token}\n")


@cache
def _get_msal_app(
    client_id: str, authority: str, scope_key: tuple[str, ...]
) -> PublicClientApplication:
    del scope_key
    return PublicClientApplication(client_id, authority=authority)


def get_access_token(
    env_path: Path,
    scopes: tuple[str, ...],
    *,
    allow_interactive: bool = True,
) -> str:
    config = dotenv_values(env_path)
    client_id = config.get("MICROSOFT_CLIENT_ID", "")
    authority = config.get("MICROSOFT_AUTHORITY", "")
    if not client_id or not authority:
        raise AuthError(
            f"Missing MICROSOFT_CLIENT_ID or MICROSOFT_AUTHORITY in {env_path}"
        )

    app = _get_msal_app(client_id, authority, scopes)
    refresh_token = config.get("MICROSOFT_REFRESH_TOKEN")
    refresh_error: str | None = None
    if refresh_token:
        result = app.acquire_token_by_refresh_token(refresh_token, scopes=list(scopes))
        if "access_token" in result:
            if "refresh_token" in result:
                _update_env_refresh_token(env_path, result["refresh_token"])
            return result["access_token"]
        refresh_error = result.get("error_description") or result.get("error", "unknown")

    if not allow_interactive:
        detail = f" (reason: {refresh_error})" if refresh_error else ""
        raise AuthError(
            f"Refresh token auth failed{detail} and interactive auth is disabled. "
            "Run interactively to re-authenticate."
        )

    result = app.acquire_token_interactive(scopes=list(scopes))
    if "access_token" not in result:
        raise AuthError(
            f"Interactive authentication failed: {result.get('error_description')}"
        )
    if "refresh_token" in result:
        _update_env_refresh_token(env_path, result["refresh_token"])
    return result["access_token"]


class GraphClient:
    def __init__(
        self,
        env_path: str | Path | None,
        scopes: tuple[str, ...],
        *,
        allow_interactive: bool | None = None,
    ):
        self.env_path = Path(env_path) if env_path else DEFAULT_ENV_PATH
        self.scopes = scopes
        self.allow_interactive = (
            allow_interactive if allow_interactive is not None else sys.stdin.isatty()
        )
        self._headers: dict[str, str] | None = None

    @property
    def headers(self) -> dict[str, str]:
        if self._headers is None:
            token = get_access_token(
                self.env_path, self.scopes, allow_interactive=self.allow_interactive
            )
            self._headers = {"Authorization": f"Bearer {token}"}
        return self._headers

    def _invalidate_token(self) -> None:
        self._headers = None

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | list[Any] | None = None,
        timeout: int = 30,
        follow_redirects: bool = False,
        extra_headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        url = f"{GRAPH_BASE}{path}" if path.startswith("/") else path
        headers = {**self.headers, **(extra_headers or {})}
        response = httpx.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=timeout,
            follow_redirects=follow_redirects,
        )

        # Retry once on 401 (token expired mid-session)
        if response.status_code == 401 and self._headers is not None:
            self._invalidate_token()
            headers = {**self.headers, **(extra_headers or {})}
            response = httpx.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=timeout,
                follow_redirects=follow_redirects,
            )

        if response.is_error:
            error_code = "unknown"
            message = response.text[:200]
            try:
                body = response.json()
                error_info = body.get("error", {})
                error_code = error_info.get("code", error_code)
                message = error_info.get("message", message)
            except Exception:
                pass
            raise GraphApiError(response.status_code, error_code, message, url)

        return response

    def get_json(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self._request("GET", path, params=params).json()

    def get_all(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        next_url: str | None = f"{GRAPH_BASE}{path}" if path.startswith("/") else path
        next_params = params
        while next_url:
            response = self._request(
                "GET", next_url, params=next_params, extra_headers=extra_headers
            )
            payload = response.json()
            results.extend(payload.get("value", []))
            next_url = payload.get("@odata.nextLink")
            next_params = None
        return results

    def get_text(self, path: str, *, timeout: int = 60) -> str:
        return self._request("GET", path, timeout=timeout).text

    def get_bytes(self, path: str, *, timeout: int = 60) -> bytes:
        return self._request(
            "GET", path, timeout=timeout, follow_redirects=True
        ).content

    def post_json(
        self,
        path: str,
        body: dict[str, Any] | list[Any],
        *,
        timeout: int = 30,
    ) -> dict[str, Any]:
        return self._request(
            "POST", path, json_body=body, timeout=timeout
        ).json()
