import pytest

from jarvis_sdk.cmd import IdentityClient
from tests.helpers import data


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


def test_patch_properties_by_token_short_token(capsys):
    token = "short_token"

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties_by_token(token, [])
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_patch_properties_by_token(capsys):
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
