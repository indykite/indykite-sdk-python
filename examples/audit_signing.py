"""Manage a project's audit-signing configuration via the Config API.

Requires INDYKITE_SERVICE_ACCOUNT_CREDENTIALS[_FILE] and INDYKITE_TEST_PROJECT_ID.
"""

import os

from indykite_sdk import ConfigClient


def main() -> None:
    """Run the example."""
    project_id = os.environ["INDYKITE_TEST_PROJECT_ID"]

    with ConfigClient() as config:
        # The platform holds the signing key - nothing else is needed.
        created = config.create_audit_signing("sdk-example-audit-signing", project_id, description="SDK example")
        print(f"Created audit signing {created.id}")

        signing = config.read_audit_signing(created.id)
        print(f"Provider: {signing.provider}")

        # Switch to a customer-managed key. key_resource and kid are required, and
        # auth_params carries whatever the provider needs to reach the key.
        # Every auth_params value is write-only: reads return the keys with blank values.
        config.update_audit_signing(
            created.id,
            etag=signing.etag,
            provider="CUSTOMER_GCP_KMS",
            key_resource="projects/my-gcp-project/locations/europe-west1/keyRings/audit/cryptoKeys/signing",
            kid="gcp-audit-key-1",
            auth_params={"service_account_json": os.environ.get("GCP_SERVICE_ACCOUNT_JSON", "{}")},
        )
        signing = config.read_audit_signing(created.id)
        print(f"Provider: {signing.provider}, kid: {signing.kid}, auth params: {sorted(signing.auth_params or {})}")

        configs = config.list_audit_signings(project_id, full_fetch=True)
        print(f"Audit signings in project: {[(item.name, item.provider) for item in configs]}")

        # Clean up (delete also requires the current etag).
        config.delete_audit_signing(created.id, etag=signing.etag)
        print("Deleted example audit signing")


if __name__ == "__main__":
    main()
