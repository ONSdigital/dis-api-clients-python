from dis_api_clients.zebedee.models.requests import DataRequestParams


def test_to_query_params_with_all_values() -> None:
    params = DataRequestParams(uri="/economy/datasets/example", lang="cy", title=True)

    assert params.to_query_params() == {
        "uri": "/economy/datasets/example",
        "lang": "cy",
        "title": "",
    }


def test_to_query_params_omits_optional_values() -> None:
    params = DataRequestParams(uri="/economy/datasets/example")

    assert params.to_query_params() == {"uri": "/economy/datasets/example"}
