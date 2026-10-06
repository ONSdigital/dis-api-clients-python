from dis_api_clients.zebedee.client import ZebedeeClient, create_client
from dis_api_clients.zebedee.models.headers import HTTPHeaders
from dis_api_clients.zebedee.protocols import ZebedeeClientProtocol
from tests.fakes import FakeResponse, FakeSession

from .test_headers import TEST_VALUE


def test_get_dataset_resolves_file_sizes() -> None:
    uri = "/datasets/example"
    headers = HTTPHeaders(access_token=TEST_VALUE)
    request_headers = headers.to_http_headers()
    session = FakeSession(
        responses=[
            FakeResponse(
                200,
                {
                    "type": "dataset",
                    "downloads": [
                        {"file": "test.txt"},
                        {"file": "external.csv", "uri": "https://example.test/file", "Size": "2"},
                    ],
                    "supplementaryFiles": [
                        {"title": "test_title", "file": "extra.txt"},
                    ],
                },
            ),
            FakeResponse(200, {"fileSize": 1}),
            FakeResponse(200, {"fileSize": 3}),
        ]
    )

    client = ZebedeeClient("http://localhost:8082", session=session)

    dataset = client.get_dataset(uri, headers=headers, collection_id="example_collection", lang="en")

    assert dataset.downloads[0].size == "1"
    assert dataset.downloads[1].size == "2"
    assert dataset.supplementary_files[0].size == "3"

    assert len(session.calls) == 3
    data_call, download_call, supplementary_call = session.calls

    assert data_call == {
        "method": "GET",
        "url": "http://localhost:8082/data/example_collection",
        "params": {"uri": uri, "lang": "en"},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert download_call == {
        "method": "GET",
        "url": "http://localhost:8082/filesize/example_collection",
        "params": {"uri": f"{uri}/test.txt", "lang": "en"},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert supplementary_call == {
        "method": "GET",
        "url": "http://localhost:8082/filesize/example_collection",
        "params": {"uri": f"{uri}/extra.txt", "lang": "en"},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert not session.responses


def test_get_dataset_landing_page_resolves_related_titles() -> None:
    uri = "/datasets/example"
    headers = HTTPHeaders(access_token=TEST_VALUE)
    request_headers = headers.to_http_headers()
    session = FakeSession(
        responses=[
            FakeResponse(
                200,
                {
                    "type": "dataset_landing_page",
                    "description": {"title": "Labour disputes by sector: LABD02"},
                    "relatedDatasets": [{"uri": "pageTitle1"}],
                    "relatedDocuments": [{"uri": "pageTitle2"}],
                    "relatedMethodology": [{"uri": "pageTitle3"}],
                    "relatedMethodologyArticle": [{"uri": "pageTitle4"}],
                    "datasets": [{"uri": "not-resolved"}],
                    "links": [{"uri": "also-not-resolved"}],
                },
            ),
            FakeResponse(200, {"title": "related-dataset"}),
            FakeResponse(200, {"title": "page-title"}),
            FakeResponse(200, {"title": "methodology-title"}),
            FakeResponse(200, {"title": "article-title"}),
        ]
    )
    client = ZebedeeClient("http://localhost:8082", session=session)

    dataset_landing_page = client.get_dataset_landing_page(uri, headers=headers, lang="en")

    assert dataset_landing_page.description.title == "Labour disputes by sector: LABD02"
    assert dataset_landing_page.related_datasets[0].title == "related-dataset"
    assert dataset_landing_page.related_documents[0].title == "page-title"
    assert dataset_landing_page.related_methodology[0].title == "methodology-title"
    assert dataset_landing_page.related_methodology_article[0].title == "article-title"
    assert dataset_landing_page.datasets[0].title == ""
    assert dataset_landing_page.related_links[0].title == ""

    assert len(session.calls) == 5
    dataset_landing_page_call, dataset_call, document_call, methodology_call, article_call = session.calls

    assert dataset_landing_page_call == {
        "method": "GET",
        "url": "http://localhost:8082/data",
        "params": {"uri": uri, "lang": "en"},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert dataset_call == {
        "method": "GET",
        "url": "http://localhost:8082/data",
        "params": {"uri": "pageTitle1", "lang": "en", "title": ""},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert document_call == {
        "method": "GET",
        "url": "http://localhost:8082/data",
        "params": {"uri": "pageTitle2", "lang": "en", "title": ""},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert methodology_call == {
        "method": "GET",
        "url": "http://localhost:8082/data",
        "params": {"uri": "pageTitle3", "lang": "en", "title": ""},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert article_call == {
        "method": "GET",
        "url": "http://localhost:8082/data",
        "params": {"uri": "pageTitle4", "lang": "en", "title": ""},
        "json": None,
        "headers": request_headers,
        "timeout": 10.0,
    }
    assert not session.responses


def test_create_client_returns_protocol_conforming_client() -> None:
    client = create_client("http://localhost:8082")

    assert isinstance(client, ZebedeeClientProtocol)
    assert isinstance(client, ZebedeeClient)
