from http import HTTPStatus

import pytest
import requests

from dis_api_clients._http import HTTPClient
from dis_api_clients.exceptions import APIError

from ..fakes import FakeResponse, FakeSession


def test_init_rejects_empty_base_url() -> None:
    with pytest.raises(ValueError, match="base_url must not be empty"):
        HTTPClient("")


def test_init_removes_trailing_slash_from_base_url() -> None:
    client = HTTPClient("http://localhost:8080/")

    assert client.base_url == "http://localhost:8080"


def test_init_creates_session_when_not_provided() -> None:
    client = HTTPClient("http://localhost:8080")

    assert isinstance(client.session, requests.Session)


def test_init_uses_supplied_session() -> None:
    session = FakeSession(responses=[FakeResponse(status_code=200)])

    client = HTTPClient("http://localhost:8080", session=session)

    assert client.session is session


def test_init_rejects_non_session_objects() -> None:
    with pytest.raises(TypeError):
        HTTPClient(
            base_url="http://localhost:8080",
            session=object(),
        )


def test_request_forwards_options_and_returns_response() -> None:
    response = FakeResponse(status_code=200, payload={"status": "ok"})
    session = FakeSession(responses=[response])
    client = HTTPClient(
        "http://localhost:8080",
        timeout=10,
        session=session,
    )

    result = client._request(
        "GET",
        "/health",
        params={"exampleParam": "foo"},
        headers={"example-header": "bar"},
    )

    assert result is response
    assert len(session.calls) == 1
    assert session.calls[0] == {
        "method": "GET",
        "url": "http://localhost:8080/health",
        "params": {"exampleParam": "foo"},
        "json": None,
        "headers": {"example-header": "bar"},
        "timeout": 10,
    }


def test_request_wraps_request_exception() -> None:
    session = FakeSession(responses=[requests.ConnectionError("connection failed")])
    client = HTTPClient("http://localhost:8080", session=session)

    with pytest.raises(APIError, match="connection failed"):
        client._request("GET", "/health")


def test_request_raises_api_error_for_http_failures() -> None:
    session = FakeSession(responses=[FakeResponse(status_code=500, payload={"error": "internal server error"})])
    client = HTTPClient("http://localhost:8080", session=session)

    with pytest.raises(APIError, match="internal server error") as exc_info:
        client._request("GET", "/health")

    assert str(exc_info.value) == ("Request failed with status code 500: {'error': 'internal server error'}")
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
