# Zebedee SDK

A Python client for retrieving datasets and dataset landing pages from [Zebedee](https://github.com/ONSdigital/zebedee).

For installation instructions, see [Install an API Client](../../README.md#install-an-api-client) in the main README.

## Quick Start

Create a client and retrieve a dataset:

```python
from dis_api_clients.zebedee import HTTPHeaders, create_client

client = create_client(base_url="http://localhost:8082")
headers = HTTPHeaders(access_token="<service-auth-token>")

dataset = client.get_dataset(
    uri="/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset",
    headers=headers,
)

print(dataset.description.title)
```

## Create a Client

```python
import requests

from dis_api_clients.zebedee import create_client

session = requests.Session()
client = create_client(
    base_url="http://localhost:8082",
    timeout=5.0,
    session=session,
)
```

Both session and timeout are optional. If not provided, the client creates a new `requests.Session` and uses a
10 second timeout by default.

## Authentication and Headers

Pass an instance of `HTTPHeaders` to the client methods when a request requires authentication or additional
headers. The supported headers include:

| `HTTPHeaders` field | HTTP header                            |
|---------------------|----------------------------------------|
| `access_token`      | `Authorization` and `X-Florence-Token` |

## Available Methods

| Method                                                             | HTTP endpoint |
|--------------------------------------------------------------------|---------------|
| [`client.get_dataset()`](#get-a-dataset)                           | `GET /data`   |
| [`client.get_dataset_landing_page()`](#get-a-dataset-landing-page) | `GET /data`   |

### Get a dataset

Fetches dataset details for the given URI and fills in sizes for downloads and supplementary files stored in Zebedee.

```python
dataset = client.get_dataset(
    uri="/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset",
    headers=headers,
)
```

### Get a dataset landing page

Fetches landing page content for the given URI and resolves titles for related datasets, documents, and methodology items.

```python
landing_page = client.get_dataset_landing_page(
    uri="/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset",
    headers=headers,
)
```

## Error Handling

HTTP errors and request failures raise an `APIError`. HTTP errors include the response status code in
`status_code` while network errors have `status_code` set to `None`.

```python
from dis_api_clients import APIError
from dis_api_clients.zebedee import create_client

client = create_client(base_url="http://localhost:8082")

try:
    dataset = client.get_dataset(uri="/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset")
except APIError as error:
    print(f"Zebedee request failed: {error}; status={error.status_code}")
```
