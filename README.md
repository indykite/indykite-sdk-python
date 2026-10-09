# IndyKite Python SDK

[![PyPI](https://img.shields.io/pypi/v/indykite-sdk-python)](https://pypi.org/project/indykite-sdk-python/)
[![Tests](https://github.com/indykite/indykite-sdk-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/indykite/indykite-sdk-python/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/indykite/indykite-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/indykite/indykite-sdk-python)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Python clients for the [IndyKite](https://www.indykite.com) platform REST APIs:
the Identity Knowledge Graph (IKG), KBAC authorization (AuthZEN), ContX IQ
knowledge queries, data capture, entity matching, the tamper-proof audit
trail, and platform configuration.

- SDK API reference: <https://indykite.github.io/indykite-sdk-python/>
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
| **Application Agent** | all data-plane clients (capture, authzen, ciq, data schema, entity matching, audit) | the **raw credential token itself** (opaque string, sent as `X-IK-ClientKey`) | `INDYKITE_APPLICATION_CREDENTIALS` (the token) or `INDYKITE_APPLICATION_CREDENTIALS_FILE` (path) |
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

Each data-plane API is guarded by one **API permission** on the application
agent, granted when the agent is created (Hub or `ConfigClient`):

| Permission | Client | Endpoints |
| --- | --- | --- |
| `Authorization` | `AuthZENClient` | decisions and searches (`/access/v1/evaluation*`, `/search/*`) |
| `ReadAuthZConfigs` | `AuthZENClient.policies` | the project's active policies (`/access/v1/policies`) |
| `Capture` | `CaptureClient` | `/capture/v1/*` |
| `ContXIQ` | `CIQClient` | `/contx-iq/v1/*` |
| `ReadDataSchema` | `DataSchemaClient` | `/data-schema/v1` |
| `EntityMatching` | `EntityMatchingClient` | `/entity-matching/v1/*` |
| `Audit` | `AuditClient` | the tamper-proof audit trail (`/audit/v1/*`) |

A call to an endpoint the agent is not permitted for raises
`AuthenticationError` (401, `insufficient API access level`). A permission
granted later takes a moment to reach the data plane.

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

    # The active policies of the project (agent needs the ReadAuthZConfigs permission)
    for policy in client.policies(subject_type="Person").results:
        print(policy.tags, policy.policy["actions"])
```

#### Token claims in policy conditions

Decisions and knowledge queries accept two optional request tokens. They travel
as headers, never in the body, and the policy condition reads their claims:

| Argument | Header | Claims in the policy |
| --- | --- | --- |
| `user_token` | `Authorization: Bearer` | `$token`, e.g. `$token.sub` (needs a Token Introspect configuration) |
| `delegated_token` | `X-IK-Token` | `$ik_token`, e.g. `$ik_token.act.sub` — the RFC 8693 delegation chain of a token minted by the IndyKite Token Service |

```python
with AuthZENClient() as client:
    result = client.evaluation(
        ("Person", "ada"),
        "CAN_DRIVE",
        ("Car", "kitt"),
        user_token=end_user_access_token,  # $token.sub == "ada"
        delegated_token=ik_delegated_token,  # $ik_token.act.sub names the acting agent
    )
```

`token` and `ik_token` are reserved names in `input_params`: a policy never
asks for them, a value sent under them is replaced by the real claims, and a
token that was not sent binds an empty claim set, so a policy reading it denies
rather than fails.

### Capture graph data

```python
from indykite_sdk import CaptureClient

with CaptureClient() as client:
    client.upsert_nodes(
        [
            {
                "external_id": "ada",
                "type": "Person",
                "is_identity": True,
                "properties": [{"type": "email", "value": "ada@example.com"}],
            },
            {"external_id": "kitt", "type": "Car"},
        ]
    )
    client.upsert_relationships(
        [
            {
                "type": "OWNS",
                "source": {"external_id": "ada", "type": "Person"},
                "target": {"external_id": "kitt", "type": "Car"},
            },
        ]
    )
```

### Read the graph with a knowledge query (ContX IQ)

```python
from indykite_sdk import CIQClient

with CIQClient() as client:
    for record in client.execute_iter("gid:my-knowledge-query-id", input_params={"personId": "ada"}):
        print(record.nodes)

    # Which graph node does an end-user token resolve to?
    user_token = "<end-user-access-token>"  # a token your Token Introspect config can validate
    me = client.whoami(user_token)
    print(me.type, me.id)  # e.g. Person ada

    # Run in the user's context; the CIQ policy reads $token.sub and $ik_token.act.sub
    client.execute("gid:my-knowledge-query-id", user_token=user_token, delegated_token="<ik-token>")
```

### Read the tamper-proof audit trail

Every audit event of a project is appended to a signed **chain**: events are
collected into signed batches (`logs`), a signed **manifest** links each batch
to the previous one (`prev_hash` / `head_hash`), and signed **checkpoints**
periodically fix the chain head. The agent needs the `Audit` permission and
can only read its own project.

```python
from indykite_sdk import AuditClient

with AuditClient() as client:
    keys = client.jwks(project_id)  # public signing keys; keep them with an export
    for batch in client.iter_logs(project_id):  # sequence order, all pages
        for event in batch.data:  # untyped dicts, authored by whoever triggered them
            print(batch.sequence, event.get("type"))
    manifests = list(client.iter_manifests(project_id))  # linkage without payloads
    newest = client.list_checkpoints(project_id, page_size=1).items  # newest first
```

Listings return a `Page` (`items`, `has_more`, `next_cursor`); `iter_*` follows
the cursor for you. The signing key itself is configured with
`ConfigClient.create_audit_signing` (see below).

### Manage platform configuration

```python
from indykite_sdk import ConfigClient

with ConfigClient() as config:
    organization = config.read_current_organization()
    project = config.create_project("my-project", organization.id, region="europe-west1")
    app = config.create_application("my-app", project.id)
    agent = config.create_application_agent(
        "my-agent", app.id, ["Authorization", "Capture", "ContXIQ", "ReadAuthZConfigs", "Audit"]
    )
    credential = config.create_application_agent_credential(agent.id)
    agent_credentials = credential.as_credentials()  # shown once - store it securely
```

Updates and deletes accept an optional etag, sent as `If-Match` so a change
made since you read the resource is not overwritten: read the resource, then
pass its `.etag`:

```python
app = config.read_application(app_id)
config.update_application(app_id, etag=app.etag, display_name="Renamed")
```

Audit signing decides which key signs a project's audit trail (the batches,
manifests and checkpoints `AuditClient` reads). The default is a
platform-managed key; customer-managed providers bring their own key:

```python
signing = config.create_audit_signing("audit-signing", project.id)  # PLATFORM_MANAGED
config.create_audit_signing(
    "audit-signing-kms",
    project.id,
    provider="CUSTOMER_GCP_KMS",
    key_resource="projects/p/locations/l/keyRings/r/cryptoKeys/k/cryptoKeyVersions/1",
    kid="gcp-key-1",
    auth_params={"service_account_json": "..."},  # write-only, read back masked
)
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
