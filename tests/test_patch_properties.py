from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from helpers import data


def test_patch_properties_wrong_twin_id(capsys):
    digital_twin_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert (
        "list indices must be integers or slices, not str" in captured.err
    )


def test_patch_properties_wrong_tenant_id(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"

    client = IdentityClient()
    assert client is not None

    response = client.patch_properties(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert "list indices must be integers or slices, not str" in captured.err


def test_patch_properties_error(capsys):
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
    captured = capsys.readouterr()
    assert "something went very wrong" in captured.err


def test_patch_properties_success():
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_patch_properties(request: pb2.PatchDigitalTwinRequest):
        digital_twin_bytes_str = str(digital_twin_id)
        tenant_bytes_str = str(tenant_id)
        assert request.id.digital_twin.id == digital_twin_bytes_str
        assert request.id.digital_twin.tenant_id == tenant_bytes_str
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
    assert "Token must be 32 chars or more" in captured.err


def test_patch_properties_by_token_expired_token(capsys):
    digital_twin_id = data.get_digital_twin()
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
    assert "invalid or expired access_token" in captured.err


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
