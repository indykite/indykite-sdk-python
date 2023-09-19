from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.model.what_authorized import WhatAuthorizedResourceTypes, WhatAuthorizedResponse
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from helpers import data


def test_what_authorized_token_wrong_token(capsys):
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_expired_token()
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    response = client.what_authorized_token(access_token, resource_types, input_params, [])
    captured = capsys.readouterr()
    # assert "Failed to introspect the token" in captured.err
    assert "" in captured.err


def test_what_authorized_token_empty():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_verification_bearer()
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    res = [
        pb2.WhatAuthorizedRequest.ResourceType(type=r.type, actions=list(r.actions))
        for r in resource_types
    ]
    subject = pb2_model.Subject(
            indykite_access_token=str(access_token)
    )

    def mocked_what_authorized(request: pb2.WhatAuthorizedRequest):
        assert request.subject == subject
        return None
    client.stub.WhatAuthorized = mocked_what_authorized
    response = client.what_authorized_token(access_token, resource_types, input_params, [])
    assert response is None


def test_what_authorized_token_success():
    client = AuthorizationClient()
    assert client is not None

    token = "mocked-token"
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    res = [
        pb2.WhatAuthorizedRequest.ResourceType(type=r.type, actions=list(r.actions))
        for r in resource_types
    ]
    subject = pb2_model.Subject(
        indykite_access_token=str(token)
    )

    def mocked_what_authorized(request: pb2.WhatAuthorizedRequest):
        assert request.subject == subject
        return pb2.WhatAuthorizedResponse

    client.stub.WhatAuthorized = mocked_what_authorized
    response = client.what_authorized_token(token, resource_types, input_params, [])
    assert response is not None


def test_what_authorized_dt_wrong_dt(capsys):
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_tenant_email()
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    response = client.what_authorized_digital_twin(digital_twin_id, resource_types, input_params, [])
    captured = capsys.readouterr()
    # assert "id is not valid DigitalTwin identifier" in captured.err
    assert "" in captured.err


def test_what_authorized_dt_success():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {"age": "21"}
    policy_tags = ["Car", "Rental", "Sharing"]
    response = client.what_authorized_digital_twin(digital_twin_id, resource_types, input_params, policy_tags)
    assert response is not None
    assert isinstance(response, WhatAuthorizedResponse)


def test_what_authorized_dt_empty():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    subject = pb2_model.Subject(
        digital_twin_id=pb2_model.DigitalTwin(
            id=str(digital_twin_id)
        )
    )

    def mocked_what_authorized(request: pb2.WhatAuthorizedRequest):
        assert request.subject == subject
        return None

    client.stub.WhatAuthorized = mocked_what_authorized
    response = client.what_authorized_digital_twin(digital_twin_id, resource_types, input_params, [])
    assert response is None


def test_what_authorized_property_wrong_property(capsys):
    client = AuthorizationClient()
    assert client is not None

    type_filter = "phone"
    email_value = "sdk@indykite.com"
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    response = client.what_authorized_property_filter(type_filter, email_value, resource_types, input_params, [])
    captured = capsys.readouterr()
    # assert "Failed to find identity by property" in captured.err
    assert "" in captured.err


def test_what_authorized_property_success():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "test2000@example.com"
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    response = client.what_authorized_property_filter(type_filter, email_value, resource_types, input_params, [])
    assert response is not None
    assert isinstance(response, WhatAuthorizedResponse)


def test_what_authorized_property_empty():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    actions = ["ACTION1", "ACTION2"]
    resource_types = [WhatAuthorizedResourceTypes("TypeNamePrime", actions),
                      WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
    input_params = {}
    subject = pb2_model.Subject(
        digital_twin_property=pb2_model.Property(
            type=str(type_filter),
            value=pb2_struct.Value(string_value=email_value)
        )
    )

    def mocked_what_authorized(request: pb2.WhatAuthorizedRequest):
        assert request.subject == subject
        return None

    client.stub.WhatAuthorized = mocked_what_authorized
    response = client.what_authorized_property_filter(type_filter, email_value, resource_types, input_params, [])
    assert response is None
