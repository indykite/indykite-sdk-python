from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.model.register_digital_twin_without_credential import RegisterDigitalTwinWithoutCredential
from indykite_sdk.indykite.identity.v1beta2.identity_management_api_pb2 import RegisterDigitalTwinWithoutCredentialRequest
from helpers import data
from indykite_sdk.identity import helper
import random


def test_register_dt_no_cred_success(capsys):
    client = IdentityClient()
    assert client is not None

    tenant_id = data.get_tenant()
    number = random.randint(1, 1000000)
    properties = []
    definition1 = attributes.PropertyDefinition(
        property="extid"
    )
    property1 = helper.create_property(definition1, None, str(number))
    properties.append(property1)
    # with return success
    register_response = client.register_digital_twin_without_credential(
        tenant_id,
        1,
        [],
        properties,
        [])
    assert isinstance(register_response, RegisterDigitalTwinWithoutCredential)

    # with return error
    register_response = client.register_digital_twin_without_credential(
        tenant_id,
        1,
        [],
        properties,
        [])
    assert isinstance(register_response, RegisterDigitalTwinWithoutCredential)


def test_register_dt_no_cred_empty(capsys):
    tenant_id = data.get_tenant()
    properties = []
    definition1 = attributes.PropertyDefinition(
        property="extid"
    )
    number = random.randint(1, 1000000)
    property1 = helper.create_property(definition1, None, str(number))
    properties.append(property1)

    client = IdentityClient()
    assert client is not None

    def mocked_register_dt_no_cred(request: RegisterDigitalTwinWithoutCredentialRequest):
        return None

    client.stub.RegisterDigitalTwinWithoutCredential = mocked_register_dt_no_cred
    response = client.register_digital_twin_without_credential(
        tenant_id,
        1,
        [],
        properties,
        [])
    captured = capsys.readouterr()
    assert response is None


def test_register_dt_no_cred_none(capsys):
    client = IdentityClient()
    assert client is not None

    tenant_id = data.get_tenant()
    number = random.randint(1, 1000000)
    properties = []
    definition1 = attributes.PropertyDefinition(
        property="extid"
    )
    property1 = helper.create_property(definition1, None, str(number))
    properties.append(property1)
    # with return success
    register_response = client.register_digital_twin_without_credential(
        tenant_id,
        12,
        [],
        properties,
        [])
    assert register_response is None
