import requests

from .._http import HTTPClient
from .models.dataset import Dataset, Download, FileSize, SupplementaryFile
from .models.dataset_landing_page import DatasetLandingPage, PageTitle
from .models.headers import HTTPHeaders
from .models.requests import DataRequestParams
from .protocols import ZebedeeClientProtocol


class ZebedeeClient(HTTPClient):
    """Zebedee SDK client."""

    def get_dataset(
        self,
        uri: str,
        *,
        headers: HTTPHeaders | None = None,
        collection_id: str = "",
        lang: str = "",
    ) -> Dataset:
        """Fetch dataset details and resolve file sizes.

        Retrieves the dataset from ``GET /data`` (or ``/data/{collection_id}``) for
        the requested URI and language. Populates sizes for downloads and
        supplementary files stored in Zebedee.
        """
        data_path = f"/data/{collection_id}" if collection_id else "/data"
        request_headers = headers.to_http_headers() if headers else None

        dataset_response = self._request(
            "GET",
            data_path,
            params=DataRequestParams(uri=uri, lang=lang).to_query_params(),
            headers=request_headers,
        )
        dataset = Dataset.model_validate(dataset_response.json())

        file_size_path = f"/filesize/{collection_id}" if collection_id else "/filesize"
        file_items: list[Download | SupplementaryFile] = [
            *dataset.downloads,
            *dataset.supplementary_files,
        ]

        # TODO: Consider making calls concurrently if performance becomes an issue.
        for item in file_items:
            if item.uri:
                continue

            file_size_response = self._request(
                "GET",
                file_size_path,
                params=DataRequestParams(uri=f"{uri}/{item.file}", lang=lang).to_query_params(),
                headers=request_headers,
            )

            item.size = str(FileSize.model_validate(file_size_response.json()).size)

        return dataset

    def get_dataset_landing_page(
        self,
        uri: str,
        *,
        headers: HTTPHeaders | None = None,
        collection_id: str = "",
        lang: str = "",
    ) -> DatasetLandingPage:
        """Fetch a dataset landing page and resolve related item titles.

        Retrieves the page from ``GET /data`` (or ``/data/{collection_id}``) for the
        requested URI and language. Resolves titles for related datasets, documents,
        and methodology items.
        """
        dataset_landing_page_path = f"/data/{collection_id}" if collection_id else "/data"
        request_headers = headers.to_http_headers() if headers else None

        dataset_landing_page_response = self._request(
            "GET",
            dataset_landing_page_path,
            params=DataRequestParams(uri=uri, lang=lang).to_query_params(),
            headers=request_headers,
        )
        dataset_landing_page = DatasetLandingPage.model_validate(dataset_landing_page_response.json())

        # TODO: Consider making calls concurrently if performance becomes an issue.
        for related_items in (
            dataset_landing_page.related_datasets,
            dataset_landing_page.related_documents,
            dataset_landing_page.related_methodology,
            dataset_landing_page.related_methodology_article,
        ):
            for item in related_items:
                page_title_response = self._request(
                    "GET",
                    dataset_landing_page_path,
                    params=DataRequestParams(uri=item.uri, lang=lang, title=True).to_query_params(),
                    headers=request_headers,
                )
                page_title = PageTitle.model_validate(page_title_response.json())
                item.title = page_title.title

        return dataset_landing_page


def create_client(
    base_url: str,
    timeout: float = 10,
    session: requests.Session | None = None,
) -> ZebedeeClientProtocol:
    return ZebedeeClient(base_url=base_url, timeout=timeout, session=session)
