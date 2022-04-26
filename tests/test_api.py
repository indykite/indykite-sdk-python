import json
import re
import sys
from uuid import UUID

import pytest

from jarvis_sdk import api
from tests.helpers import data
from tests.helpers import api_requests


@pytest.fixture(name="prepare")
@pytest.mark.usefixtures("set_env")
def prepare(set_env):
    assert set_env


def is_uuid4(uid):
    try:
        UUID(uid, version=4)
    except (TypeError, ValueError):
        return False
    return True


@pytest.mark.usefixtures("login")
def test_introspect_success(prepare, login, capsys):
    # Prepare
    token = login[0]
    sys.argv = ["this_is_skipped", "introspect", token]

    # Act
    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    # Assert
    assert "customerId" in x
    assert is_uuid4(x["customerId"])
    assert "appSpaceId" in x
    assert is_uuid4(x["appSpaceId"])
    assert "applicationId" in x
    assert is_uuid4(x["applicationId"])
    assert "subject" in x
    assert is_uuid4(x["subject"]["id"])
    assert is_uuid4(x["subject"]["tenantId"])
    assert "issueTime" in x
    assert len(x["issueTime"]) != 0
    assert "expireTime" in x
    assert len(x["expireTime"]) != 0
    assert "authenticationTime" in x
    assert len(x["authenticationTime"]) != 0
    assert len(x["providerInfo"]) >= 1
    for a in x["providerInfo"]:
        assert a["type"] == "PROVIDER_TYPE_PASSWORD"
        assert a["issuer"] == "indykite.id"


@pytest.mark.usefixtures("login")
def test_get_dt_success(prepare, login, capsys):
    # Prepare
    token = login[0]
    sys.argv = ["this_is_skipped", "introspect", token]

    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    dt_id = x["subject"]["id"]
    tenant_id = x["subject"]["tenantId"]
    sys.argv = ["this_is_skipped", "get-dt", dt_id, tenant_id, "property_list", "email"]

    # Act
    api.main()
    captured = capsys.readouterr()
    prefix = "['email']\n"
    x = json.loads(captured.out[len(prefix):])

    # Assert
    assert x["digitalTwin"]["digitalTwin"]["id"] == dt_id
    assert x["digitalTwin"]["digitalTwin"]["tenantId"] == tenant_id
    assert len(x["digitalTwin"]["createTime"]) != 0
    for e in x["digitalTwin"]["properties"]:
        assert e["id"] != ""
        assert e["definition"]["property"] == "email"
        # assert e["meta"]["primary"] in [True, False]
        assert len(e["objectValue"]["stringValue"]) != 0


@pytest.mark.usefixtures("login")
def test_get_dt_by_token_success(prepare, login, capsys):
    # Prepare
    token = login[0]
    sys.argv = ["this_is_skipped", "get-dt-by-token", token, "property_list", "email"]

    # Act
    api.main()
    captured = capsys.readouterr()
    prefix = "['email']\n"
    x = json.loads(captured.out[len(prefix):])

    # Assert
    assert is_uuid4(x["digitalTwin"]["digitalTwin"]["id"])
    assert is_uuid4(x["digitalTwin"]["digitalTwin"]["tenantId"])
    assert len(x["digitalTwin"]["createTime"]) != 0
    for e in x["digitalTwin"]["properties"]:
        assert e["id"] != 0
        assert e["definition"]["property"] == "email"
        # assert e["meta"]["primary"] in [True, False]
        assert len(e["objectValue"]["stringValue"]) != 0


@pytest.mark.usefixtures("registration")
def test_del_dt_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "introspect", token]

    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    dt_id = x["subject"]["id"]
    tenant_id = x["subject"]["tenantId"]
    sys.argv = ["this_is_skipped", "del-dt", dt_id, tenant_id]

    # Act
    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    # Assert
    assert x["digitalTwin"]["id"] == dt_id
    assert x["digitalTwin"]["tenantId"] == tenant_id


@pytest.mark.usefixtures("registration")
def test_del_dt_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "del-dt-by-token", token]

    # Act
    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    # Assert
    assert is_uuid4(x["digitalTwin"]["id"])
    assert is_uuid4(x["digitalTwin"]["tenantId"])


@pytest.mark.usefixtures("registration")
def test_patch_properties_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "introspect", token]

    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    dt_id = x["subject"]["id"]
    tenant_id = x["subject"]["tenantId"]
    sys.argv = ["this_is_skipped", "patch-properties", dt_id, tenant_id, "--add", "email", "second@email.com"]

    # Act
    api.main()
    captured = capsys.readouterr()

    # Assert
    assert "success" in captured.out
    assert captured.out.count("success") == 1


@pytest.mark.usefixtures("registration")
def test_patch_properties_by_token_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "patch-properties-by-token", token, "--add", "email", "second@email.com"]

    # Act
    api.main()
    captured = capsys.readouterr()
    prefix = "The patch operation was success: result "
    trimmed = captured.out[len(prefix):]

    # Assert
    assert "success" in trimmed
    assert trimmed.count("success") == 1
    assert trimmed.count("property_id") == 1


@pytest.mark.usefixtures("registration")
def test_patch_properties_remove_success(prepare, registration, capsys):
    # Prepare
    new_email = "automation_second@email.com"

    token = registration[0]
    sys.argv = ["this_is_skipped", "introspect", token]

    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    dt_id = x["subject"]["id"]
    tenant_id = x["subject"]["tenantId"]
    sys.argv = ["this_is_skipped", "patch-properties", dt_id, tenant_id, "--add", "email", new_email]
    api.main()

    sys.argv = ["this_is_skipped", "get-dt", dt_id, tenant_id, "property_list", "email"]
    api.main()
    captured = capsys.readouterr()
    sp = captured.out.split("['email']")
    x = json.loads(sp[1])
    email = x["digitalTwin"]["properties"][0]["objectValue"]["stringValue"]
    prop_id = x["digitalTwin"]["properties"][0]["id"]

    assert sp[0].count("success") == 1
    assert email == new_email

    sys.argv = ["this_is_skipped", "patch-properties", dt_id, tenant_id, "--remove", prop_id]

    # Act
    api.main()
    captured = capsys.readouterr()

    # Assert
    assert captured.out.count("success") == 1
    # Check if the property was really removed
    sys.argv = ["this_is_skipped", "get-dt", dt_id, tenant_id, "property_list", "email"]
    api.main()
    captured = capsys.readouterr()
    assert new_email not in captured.out


@pytest.mark.usefixtures("registration")
def test_patch_properties_remove_by_token_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "patch-properties-by-token", token, "--add", "email", "second@email.com"]

    # Act
    api.main()
    captured = capsys.readouterr()
    prefix = "The patch operation was success: result "
    trimmed = captured.out[len(prefix):]

    # Assert
    assert "success" in trimmed
    assert trimmed.count("success") == 1
    assert trimmed.count("property_id") == 1


@pytest.mark.usefixtures("registration")
def test_change_password_of_user_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "get-dt-by-token", token, "property_list", "email"]

    api.main()
    captured = capsys.readouterr()
    prefix = "['email']\n"
    x = json.loads(captured.out[len(prefix):])

    email = x["digitalTwin"]["properties"][0]["objectValue"]["stringValue"]
    dt_id = x["digitalTwin"]["digitalTwin"]["id"]
    tenant_id = x["digitalTwin"]["digitalTwin"]["tenantId"]

    sys.argv = ["this_is_skipped", "change-password-of-user", dt_id, tenant_id, data.get_new_password()]

    # Act
    api.main()
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "The password has been changed successfully\n"
    token, refresh_token = api_requests.login(email, data.get_new_password())
    assert len(token) > 0
    assert len(refresh_token) > 0


@pytest.mark.usefixtures("registration")
def test_change_password_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "get-dt-by-token", token, "property_list", "email"]

    api.main()
    captured = capsys.readouterr()
    prefix = "['email']\n"
    x = json.loads(captured.out[len(prefix):])

    email = x["digitalTwin"]["properties"][0]["objectValue"]["stringValue"]

    sys.argv = ["this_is_skipped", "change-password", token, data.get_new_password()]

    # Act
    api.main()
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "The password has been changed successfully\n"
    token, refresh_token = api_requests.login(email, data.get_new_password())
    assert len(token) > 0
    assert len(refresh_token) > 0


# internal email provider does not work now
@pytest.mark.usefixtures("registration_until_email_arrives")
def test_verify_success(prepare, registration_until_email_arrives, capsys):
    # Prepare
    token = registration_until_email_arrives
    sys.argv = ["this_is_skipped", "verify", token]

    # Act
    api.main()
    captured = capsys.readouterr()
    x = json.loads(captured.out)

    # Assert
    assert is_uuid4(x["digitalTwin"]["id"])
    assert is_uuid4(x["digitalTwin"]["tenantId"])


@pytest.mark.usefixtures("registration")
def test_start_dt_email_verification_success(prepare, registration, capsys):
    # Prepare
    token = registration[0]
    sys.argv = ["this_is_skipped", "get-dt-by-token", token, "property_list", "email"]

    api.main()
    captured = capsys.readouterr()
    prefix = "['email']\n"
    x = json.loads(captured.out[len(prefix):])

    email = x["digitalTwin"]["properties"][0]["objectValue"]["stringValue"]
    dt_id = x["digitalTwin"]["digitalTwin"]["id"]
    tenant_id = x["digitalTwin"]["digitalTwin"]["tenantId"]

    sys.argv = ["this_is_skipped", "start-dt-email-verification", dt_id, tenant_id, email]

    # Act
    api.main()
    captured = capsys.readouterr()

    # Assert
    assert "Email was sent to: "+email in captured.out
