import pytest
import re

from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from tests.helpers import data
from uuid import UUID


def test_patch_properties_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert (
        captured.out == "The digital twin id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_patch_properties_wrong_tenant_id(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-010f00000000"
    tenant_id = "696e6479-6b6-4465-8000-010f00000000"

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert captured.out == "The tenant id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    assert response is None


def test_patch_properties_error():
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_patch_properties_error(request: pb2.PatchDigitalTwinRequest):
        raise Exception("something went very wrong")

    client.stub.PatchDigitalTwin = mocked_patch_properties_error
    response = client.patch_properties(
        digital_twin_id,
        tenant_id,
        {
            "add": ["unemail", data.get_new_email()],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": [],
        },
    )

    assert response is None


def test_patch_properties_success():
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_patch_properties(request: pb2.PatchDigitalTwinRequest):
        digital_twin_bytes_uuid = UUID(digital_twin_id, version=4).bytes
        tenant_bytes_uuid = UUID(tenant_id, version=4).bytes
        assert request.id.digital_twin.id == digital_twin_bytes_uuid
        assert request.id.digital_twin.tenant_id == tenant_bytes_uuid
        return pb2.PatchDigitalTwinResponse()

    client.stub.PatchDigitalTwin = mocked_patch_properties
    response = client.patch_properties(
        digital_twin_id,
        tenant_id,
        {
            "add": ["email", data.get_new_email()],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": [],
        },
    )

    assert response is not None


def test_patch_properties_by_token_short_token(capsys):
    token = "short_token"

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties_by_token(token, [])
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_patch_properties_by_token_expired_token(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-010f00000000"
    tenant_id = data.get_tenant()
    token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties_by_token(
        token,
        {
            "add": ["email", data.get_new_email()],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": [],
        },
    )
    captured = capsys.readouterr()

    print(captured.out)
    assert "invalid or expired access_token" in captured.out
    assert response is None


def test_patch_properties_by_token_success(registration):
    token = registration[0]

    client = IdentityClient()
    assert client is not None

    def mocked_patch_properties_by_token(request: pb2.PatchDigitalTwinRequest):
        assert request.id.access_token == token
        return pb2.PatchDigitalTwinResponse()

    client.stub.PatchDigitalTwin = mocked_patch_properties_by_token
    response = client.patch_properties_by_token(
        token,
        {
            "add": ["email", data.get_new_email()],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": [],
        },
    )

    assert response is not None
    assert "The patch operation was success" in response
