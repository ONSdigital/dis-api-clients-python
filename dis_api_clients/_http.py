from collections.abc import Mapping
from typing import Any

import requests

from .exceptions import APIError


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        session: requests.Session | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url must not be empty")

        if session is not None and not isinstance(session, requests.Session):
            raise TypeError("session must be an instance of requests.Session")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session if session is not None else requests.Session()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        try:
            response = self.session.request(
                method=method,
                url=f"{self.base_url}{path}",
                params=params,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise APIError(f"Request failed: {exc}") from exc

        if not response.ok:
            raise APIError(
                f"Request failed with status code {response.status_code}: {response.text or 'No response body'}",
                status_code=response.status_code,
            )

        return response
