from collections import deque
from http import HTTPStatus

import requests


class FakeResponse:
    def __init__(
        self,
        status_code: int,
        payload: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self.content = b"{}" if payload is not None else b""
        self.text = str(self._payload)
        self.headers: dict[str, str] = dict(headers) if headers is not None else {}

    @property
    def ok(self) -> bool:
        return HTTPStatus.OK <= self.status_code < HTTPStatus.BAD_REQUEST

    def json(self) -> dict:
        return self._payload


class FakeSession(requests.Session):
    def __init__(
        self,
        responses: list[FakeResponse | requests.RequestException],
    ) -> None:
        super().__init__()
        self.responses = deque(responses)
        self.calls: list[dict] = []

    def request(self, **kwargs):
        self.calls.append(kwargs)

        if not self.responses:
            raise AssertionError("FakeSession has no responses left")

        result = self.responses.popleft()
        if isinstance(result, Exception):
            raise result
        return result
