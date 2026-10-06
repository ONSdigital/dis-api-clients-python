from typing import Protocol, runtime_checkable

from .models.dataset import Dataset
from .models.dataset_landing_page import DatasetLandingPage
from .models.headers import HTTPHeaders


@runtime_checkable
class ZebedeeClientProtocol(Protocol):
    """Protocol for the Zebedee SDK client."""

    def get_dataset(
        self,
        uri: str,
        *,
        headers: HTTPHeaders | None = None,
        collection_id: str = "",
        lang: str = "",
    ) -> Dataset: ...

    def get_dataset_landing_page(
        self,
        uri: str,
        *,
        headers: HTTPHeaders | None = None,
        collection_id: str = "",
        lang: str = "",
    ) -> DatasetLandingPage: ...
