from pydantic import BaseModel


class DataRequestParams(BaseModel):
    """Query parameters for /data requests."""

    uri: str
    lang: str | None = None
    title: bool = False

    def to_query_params(self) -> dict[str, str]:
        params: dict[str, str] = {"uri": self.uri}

        if self.lang:
            params["lang"] = self.lang

        # Zebedee expects the title parameter to be an empty string if present.
        if self.title:
            params["title"] = ""

        return params
