from pydantic import BaseModel


class HTTPHeaders(BaseModel):
    access_token: str | None = None

    def to_http_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}

        if self.access_token is not None:
            token = self.access_token
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"

            # X-Florence-Token will be deprecated in favour of Authorization in the future.
            # Both headers are included for backward compatibility.
            headers["Authorization"] = token
            headers["X-Florence-Token"] = token

        return headers
