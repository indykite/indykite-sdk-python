# IndyKite Python SDK

[![PyPI](https://img.shields.io/pypi/v/indykite-sdk-python)](https://pypi.org/project/indykite-sdk-python/)
[![Tests](https://github.com/indykite/indykite-sdk-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/indykite/indykite-sdk-python/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/indykite/indykite-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/indykite/indykite-sdk-python)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Python clients for the [IndyKite](https://www.indykite.com) platform REST APIs:
the Identity Knowledge Graph (IKG), KBAC authorization (AuthZEN), ContX IQ
knowledge queries, data capture, entity matching, and platform configuration.

- OpenAPI reference: <https://openapi.indykite.com>
- Developer guides: <https://developer.indykite.com>

## Requirements

- Python **3.14+**

## Installation

```sh
pip install indykite-sdk-python
```

## Credentials

The SDK uses the two standard IndyKite credential kinds, obtained from the
[IndyKite Hub](https://eu.hub.indykite.com) (or created via the Config API):

| Credential | Used by | What it is | Environment variables |
| --- | --- | --- | --- |
| **Application Agent** | all data-plane clients (capture, authzen, ciq, data schema, entity matching) | the **raw credential token itself** (opaque string, sent as `X-IK-ClientKey`) | `INDYKITE_APPLICATION_CREDENTIALS` (the token) or `INDYKITE_APPLICATION_CREDENTIALS_FILE` (file with the token) |
| **Service Account** | `ConfigClient` | a **JSON artifact** (`serviceAccountId`, pre-issued `token`, private key), sent as `Authorization: Bearer` | `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS` (inline JSON) or `INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE` (path) |

```sh
export INDYKITE_APPLICATION_CREDENTIALS="ik1_..."   # the app agent credential token, as issued
export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE=/path/to/service-account-credentials.json
```

Credentials can also be passed explicitly:

```python
from indykite_sdk import CaptureClient, ConfigClient, Credentials

capture = CaptureClient("ik1_...")  # data-plane clients take the raw token
config = ConfigClient(Credentials.from_file("service-account-credentials.json"))
```

The service-account JSON's pre-issued `token` is used while valid; when it
expires the SDK self-signs a fresh JWT from the credential's private key
(`privateKeyJWK` or PKCS#8). The app-agent token is never a JWT the SDK mints —
it is sent exactly as issued.

### Regions and environments

Production defaults to `https://eu.api.indykite.com`; pass `region="us"` for
the US region, or point `base_url=` / `INDYKITE_BASE_URL` at another
environment (e.g. `https://api.dev.indykite.xyz`).

## Quickstart

### Authorization decisions (AuthZEN)

```python
from indykite_sdk import AuthZENClient

with AuthZENClient() as client:
    result = client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
    print(result.decision)  # True / False

    # Which cars can ada drive?
    cars = client.search_resource(("Person", "ada"), "CAN_DRIVE", "Car")
    print([car.id for car in cars.results])
```

### Capture graph data

```python
from indykite_sdk import CaptureClient

with CaptureClient() as client:
    client.upsert_nodes([
        {
            "external_id": "ada",
            "type": "Person",
            "is_identity": True,
            "properties": [{"type": "email", "value": "ada@example.com"}],
        },
        {"external_id": "kitt", "type": "Car"},
    ])
    client.upsert_relationships([
        {
            "type": "OWNS",
            "source": {"external_id": "ada", "type": "Person"},
            "target": {"external_id": "kitt", "type": "Car"},
        },
    ])
```

### Read the graph with a knowledge query (ContX IQ)

```python
from indykite_sdk import CIQClient

with CIQClient() as client:
    for record in client.execute_iter("gid:my-knowledge-query-id", input_params={"personId": "ada"}):
        print(record.nodes)
```

### Manage platform configuration

```python
from indykite_sdk import ConfigClient

with ConfigClient() as config:
    organization = config.read_current_organization()
    project = config.create_project("my-project", organization.id, region="europe-west1")
    app = config.create_application("my-app", project.id)
    agent = config.create_application_agent("my-agent", app.id, ["Authorization", "Capture", "ContXIQ"])
    credential = config.create_application_agent_credential(agent.id)
    agent_credentials = credential.as_credentials()  # shown once - store it securely
```

Updates and deletes are guarded by etags (`If-Match`): read the resource, then
pass its `.etag`:

```python
app = config.read_application(app_id)
config.update_application(app_id, etag=app.etag, display_name="Renamed")
```

### Async

Every client has an async twin with identical methods:

```python
from indykite_sdk import AsyncAuthZENClient

async with AsyncAuthZENClient() as client:
    result = await client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
```

## Error handling

The SDK always raises typed exceptions — no method returns `None` on failure:

```python
from indykite_sdk import AuthZENClient, AuthenticationError, IndyKiteError

try:
    with AuthZENClient() as client:
        decision = client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
except AuthenticationError as error:
    print(error)  # includes method, URL, status, and an actionable hint
except IndyKiteError as error:
    print(f"SDK call failed: {error}")
```

Exceptions include `BadRequestError` (400), `AuthenticationError` (401),
`PermissionDeniedError` (403), `NotFoundError` (404), `ETagMismatchError`
(412), `RateLimitError` (429), `InternalServerError` (5xx),
`RequestValidationError` (client-side validation), and
`IndyKiteConnectionError` (network).

Idempotent requests (GET/PUT/DELETE) are retried automatically on 429/502/503/504
with exponential backoff; tune or disable via `retries=RetryConfig(...)` / `retries=None`.

## Examples

Runnable scripts for every client live in [`examples/`](examples/).

## Development

```sh
pipenv install --dev
pipenv run pytest                  # unit tests (mocked, no credentials needed)
pipenv run pytest -m integration   # live tests (needs credentials, see tests/integration/conftest.py)
pre-commit run --all-files
```

## Support

- Issues: <https://github.com/indykite/indykite-sdk-python/issues>
- Vulnerability reports: see [responsible_disclosure.md](responsible_disclosure.md)

Licensed under the [Apache License 2.0](LICENSE).
