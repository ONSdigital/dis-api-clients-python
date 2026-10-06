from dis_api_clients.zebedee.models.headers import HTTPHeaders

TEST_VALUE = "test-access-token"


def test_to_http_headers_adds_bearer_prefix_to_access_token():
    headers = HTTPHeaders(access_token=TEST_VALUE)

    assert headers.to_http_headers() == {
        "Authorization": f"Bearer {TEST_VALUE}",
        "X-Florence-Token": f"Bearer {TEST_VALUE}",
    }


def test_to_http_headers_preserves_bearer_prefix_if_present():
    headers = HTTPHeaders(access_token=f"Bearer {TEST_VALUE}")

    assert headers.to_http_headers() == {
        "Authorization": f"Bearer {TEST_VALUE}",
        "X-Florence-Token": f"Bearer {TEST_VALUE}",
    }


def test_to_http_headers_omits_empty_values():
    headers = HTTPHeaders()

    assert headers.to_http_headers() == {}
