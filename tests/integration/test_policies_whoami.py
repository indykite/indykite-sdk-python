"""Live tests for the policy listing (AuthZEN) and whoami (ContX IQ) endpoints.

Both tests build their own fixtures in the test project with the service
account, read them back through the application agent, and clean up after
themselves. Nothing is left behind, so they can run repeatedly.
"""

from __future__ import annotations

import json
import time

from indykite_sdk import AuthenticationError, AuthZENClient, CaptureClient, CIQClient, ConfigClient
from indykite_sdk.authzen import PolicyDefinition
from tests.integration.conftest import poll_until

POLICY_ACTION = "SDK_IT_CAN_SERVICE"


def _self_signed_end_user_token(issuer: str, audience: str, subject: str) -> tuple[str, str]:
    """Return ``(public_jwk_json, token)`` for a fresh RSA key pair.

    The public half goes into the Token Introspect configuration; the private
    half signs the end-user token and is discarded with this test run.
    """
    from joserfc import jwt  # skipcq: PYL-C0415 - only this test signs tokens
    from joserfc.jwk import RSAKey  # skipcq: PYL-C0415 - only this test signs tokens

    key = RSAKey.generate_key(2048)
    kid = key.thumbprint()
    public_jwk = {**key.as_dict(private=False), "kid": kid, "alg": "RS256", "use": "sig"}
    now = int(time.time())
    claims = {"iss": issuer, "aud": audience, "sub": subject, "iat": now, "exp": now + 600}
    return json.dumps(public_jwk), jwt.encode({"alg": "RS256", "kid": kid}, claims, key)


def test_authzen_policies_lists_project_policies(
    config_client: ConfigClient, authzen_client: AuthZENClient, project_id: str, unique_suffix: str
) -> None:
    """Authzen policies lists project policies."""
    tag = f"sdkit{unique_suffix}"  # tags are alphanumeric, at most 20 characters
    policy_document = {
        "meta": {"policy_version": "2.0-kbac"},
        "subject": {"type": "Person"},
        "actions": [POLICY_ACTION],
        "resource": {"type": "Car"},
        "condition": {"cypher": "MATCH (subject)-[:OWNS]->(resource)"},
    }
    created = config_client.create_authorization_policy(
        f"sdk-it-policy-{unique_suffix}", project_id, json.dumps(policy_document), "ACTIVE", tags=[tag]
    )
    assert created.id
    try:

        def find_mine(results: list[PolicyDefinition]) -> PolicyDefinition | None:
            return next((policy for policy in results if tag in policy.tags), None)

        # Filtered listing: only Person policies, ours among them.
        mine = poll_until(lambda: find_mine(authzen_client.policies(subject_type="Person").results))
        assert mine.subject_type == "Person"
        assert mine.policy["actions"] == [POLICY_ACTION]
        assert mine.policy["resource"] == {"type": "Car"}
        assert mine.tags == [tag]

        # Unfiltered listing contains it as well, and every entry has the documented shape.
        everything = authzen_client.policies().results
        assert find_mine(everything) is not None
        for policy in everything:
            assert isinstance(policy.policy, dict)
            assert isinstance(policy.tags, list)

        # A subject type no policy uses is not an error; it simply matches nothing of ours.
        assert find_mine(authzen_client.policies(subject_type="SdkItNoSuchSubject").results) is None
    finally:
        current = config_client.read_authorization_policy(created.id)
        config_client.delete_authorization_policy(created.id, etag=current.etag)


def test_ciq_whoami_resolves_end_user_token(
    config_client: ConfigClient,
    capture_client: CaptureClient,
    ciq_client: CIQClient,
    project_id: str,
    unique_suffix: str,
) -> None:
    """Ciq whoami resolves end user token."""
    # Issuer and audience are unique per run so no cached "no such configuration"
    # lookup from an earlier run can shadow the configuration created here.
    issuer = f"https://sdk-it-{unique_suffix}.example.com"
    audience = f"sdk-it-{unique_suffix}"
    subject = f"sdk-it-whoami-{unique_suffix}"
    public_jwk, token = _self_signed_end_user_token(issuer, audience, subject)

    introspect = config_client.create_token_introspect(
        {
            "name": f"sdk-it-introspect-{unique_suffix}",
            "project_id": project_id,
            "jwt_matcher": {"issuer": issuer, "audience": audience},
            "offline_validation": {"public_jwks": [public_jwk]},
            "ikg_node_type": "Person",
            "perform_upsert": False,
        }
    )
    assert introspect.id
    try:
        # Introspection matches the token subject to an existing Person node by external_id.
        capture_client.upsert_nodes([{"external_id": subject, "type": "Person", "is_identity": True}])
        try:
            # Until the configuration reaches the credential service the token is rejected as 401.
            me = poll_until(lambda: ciq_client.whoami(token), retry_on=(AuthenticationError,))
            assert me.type == "Person"
            assert me.id == subject
        finally:
            capture_client.delete_nodes([{"external_id": subject, "type": "Person"}])
    finally:
        current = config_client.read_token_introspect(introspect.id)
        config_client.delete_token_introspect(introspect.id, etag=current.etag)
