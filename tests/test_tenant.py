import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.tenant import Tenant
from indykite_sdk.model.create_tenant import CreateTenant
from indykite_sdk.model.update_tenant import UpdateTenant
from indykite_sdk.model.read_tenant_config import ReadTenantConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import TenantConfig, UsernamePolicy
from helpers import data


def test_read_tenant_by_id_wrong_id(capsys):
    tenant_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_tenant_by_id(tenant_id)
    captured = capsys.readouterr()
    assert("invalid ReadTenantRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err )


def test_read_tenant_id_success(capsys):
    client = ConfigClient()
    assert client is not None

    tenant_id = data.get_tenant_id()
    tenant = client.read_tenant_by_id(tenant_id)
    captured = capsys.readouterr()

    assert tenant is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(tenant, Tenant)


def test_read_tenant_by_id_empty():
    client = ConfigClient()
    assert client is not None

    tenant_id = data.get_tenant_id()

    def mocked_read_tenant_by_id(request: pb2.ReadTenantRequest):
        return None

    client.stub.ReadTenant = mocked_read_tenant_by_id
    tenant = client.read_tenant_by_id(tenant_id)
    assert tenant is None


def test_read_tenant_by_name_wrong_name(capsys):
    tenant_name = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()

    response = client.read_tenant_by_name(app_space_id, tenant_name)
    captured = capsys.readouterr()
    assert ("NOT_FOUND" in captured.err)


def test_read_tenant_by_name_wrong_app_space_id(capsys):
    tenant_name = data.get_tenant_name()

    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"

    response = client.read_tenant_by_name(app_space_id, tenant_name)
    captured = capsys.readouterr()
    assert("NOT_FOUND" in captured.err)


def test_read_tenant_by_name_wrong_app_space_size(capsys):
    tenant_name = data.get_tenant_name()

    client = ConfigClient()
    assert client is not None

    app_space_id = "12546"

    response = client.read_tenant_by_name(app_space_id, tenant_name)
    captured = capsys.readouterr()
    assert("invalid ReadTenantRequest.Name" in captured.err)


def test_read_tenant_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    tenant_name = data.get_tenant_name()
    app_space_id = data.get_app_space_id()

    tenant = client.read_tenant_by_name(app_space_id, tenant_name)
    captured = capsys.readouterr()

    assert tenant is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(tenant, Tenant)


def test_read_tenant_by_name_empty():
    client = ConfigClient()
    assert client is not None

    tenant_name = data.get_tenant_name()
    app_space_id = data.get_app_space_id()

    def mocked_read_tenant_by_name(request: pb2.ReadTenantRequest):
        return None

    client.stub.ReadTenant = mocked_read_tenant_by_name
    tenant = client.read_tenant_by_name(app_space_id, tenant_name)
    assert tenant is None


def test_create_tenant_success(capsys):
    client = ConfigClient()
    assert client is not None

    issuer_id = data.get_issuer_id()
    right_now = str(int(time.time()))

    tenant = client.create_tenant(issuer_id, "automation-"+right_now,
                                  "Automation "+right_now, "description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert tenant is not None
    assert isinstance(tenant, CreateTenant)
    response = client.delete_tenant(tenant.id, tenant.etag, [])
    captured = capsys.readouterr()
    assert response is not None


def test_create_tenant_empty():
    client = ConfigClient()
    assert client is not None

    issuer_id = data.get_issuer_id()
    right_now = str(int(time.time()))

    def mocked_create_tenant(request: pb2.CreateTenantRequest):
        return None

    client.stub.CreateTenant = mocked_create_tenant
    tenant = client.create_tenant(issuer_id, "automation-"+right_now, "Automation "+right_now, "description", [])
    assert tenant is None


def test_create_tenant_already_exists(capsys):
    client = ConfigClient()
    assert client is not None
    issuer_id = data.get_issuer_id()
    tenant = client.create_tenant(issuer_id, "tenant-test-test", "SDK Test Tenant", "description", [])
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_tenant_fail_invalid_issuer_id(capsys):
    client = ConfigClient()
    assert client is not None
    issuer_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"
    tenant = client.create_tenant(issuer_id, "tenant-test-test", "SDK Test Tenant", "description", [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for issuer_id" in captured.err


def test_create_tenant_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None
    issuer_id = data.get_issuer_id()
    tenant = client.create_tenant(issuer_id, ["test"], "test create", "description", [])
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_update_tenant_success(capsys):
    client = ConfigClient()
    assert client is not None

    tenant_name = data.get_tenant_name()
    app_space_id = data.get_app_space_id()
    response = client.read_tenant_by_name(app_space_id, tenant_name)
    assert response is not None

    tenant = client.update_tenant(response.id, response.etag, response.display_name, "description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.err
    assert tenant is not None
    assert isinstance(tenant, UpdateTenant)


def test_update_tenant_empty():
    client = ConfigClient()
    assert client is not None

    tenant_name = data.get_tenant_name()
    app_space_id = data.get_app_space_id()
    response = client.read_tenant_by_name(app_space_id, tenant_name)
    assert response is not None

    def mocked_update_tenant(request: pb2.UpdateTenantRequest):
        return None

    client.stub.UpdateTenant = mocked_update_tenant
    tenant = client.update_tenant(response.id, response.etag, response.display_name, "description", [])
    assert tenant is None


def test_update_tenant_fail_invalid_tenant(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    response = client.read_tenant_by_name(app_space_id, tenant_name)
    assert response is not None
    tenant_id = "gid:AAAAAdM5dfh564j5lIW1Ma1nFAA"

    tenant = client.update_tenant(tenant_id, response.etag, response.display_name,"description update", [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_update_tenant_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None

    tenant_id = data.get_tenant_id()
    tenant_name = data.get_tenant_name()
    app_space_id = data.get_app_space_id()
    response = client.read_tenant_by_name(app_space_id, tenant_name)
    assert response is not None

    tenant = client.update_tenant(tenant_id, [response.etag], response.display_name, "description", [])
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_get_tenant_list_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    match = [tenant_name]
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()

    assert tenant is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_tenant_list_wrong_app_space(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    tenant_name = data.get_tenant_name()
    match = [tenant_name]
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for app_space_id" in captured.err


def test_get_tenant_list_wrong_type(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    match = "test-create"
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value length must be between 2 and 254 runes" in captured.err


def test_get_tenant_list_wrong_bookmark(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    match = [tenant_name]
    tenant = client.list_tenants(app_space_id, match,
                                       ["RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"])
    captured = capsys.readouterr()
    assert "invalid bookmark value" in captured.err


def test_get_tenant_list_empty_match(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    match = []
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_tenant_list_no_answer_match(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    tenant_name = "test-creation"
    match = [tenant_name]
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()

    assert tenant is not None
    assert tenant == []


def test_get_tenant_list_raise_exception(capsys):

    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    match = ""
    tenant = client.list_tenants(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_tenant_list_empty():
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    tenant_name = data.get_tenant_name()
    match = [tenant_name]

    def mocked_get_tenant_list(request: pb2.ListTenantsRequest):
        return None

    client.stub.ListTenants = mocked_get_tenant_list
    tenant = client.list_tenants(app_space_id, match, [])

    assert tenant is None


def test_del_tenant_success(capsys):
    client = ConfigClient()
    assert client is not None

    issuer_id = data.get_issuer_id()
    right_now = str(int(time.time()))
    tenant = client.create_tenant(issuer_id, "automation-" + right_now,
                                  "Automation " + right_now, "description", [])
    assert tenant is not None
    response = client.delete_tenant(tenant.id, tenant.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_tenant_wrong_tenant_id(capsys):
    client = ConfigClient()
    assert client is not None

    tenant_id= data.get_app_space_id()
    response = client.delete_tenant(tenant_id, "oeprbUOYHUIYI75U", [] )
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_del_tenant_empty():
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_tenant(request: pb2.DeleteTenantRequest):
        return None

    client.stub.DeleteTenant = mocked_delete_tenant
    response = client.delete_tenant(id, etag, [])

    assert response is None


def test_read_tenant_config_wrong_id(capsys):
    tenant_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_tenant_config(tenant_id)
    captured = capsys.readouterr()
    assert("invalid ReadTenantConfigRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_tenant_config_mock():
    tenant_id = data.get_tenant_id()

    client = ConfigClient()
    assert client is not None

    def mocked_read_tenant_config(request: pb2.ReadTenantConfigRequest):
        test_id = str(tenant_id)
        assert test_id == tenant_id
        return pb2.ReadTenantConfigResponse()

    client.stub.ReadTenantConfig = mocked_read_tenant_config
    tenant_config = client.read_tenant_config(tenant_id)
    assert tenant_config is not None
    assert isinstance(tenant_config, ReadTenantConfig)


def test_read_tenant_config_wrong_id_mock(capsys):
    tenant_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"

    client = ConfigClient()
    assert client is not None

    def mocked_read_tenant_config(request: pb2.ReadTenantConfigRequest):
        raise Exception("something went wrong")

    client.stub.ReadTenantConfig = mocked_read_tenant_config
    tenant = client.read_tenant_config(tenant_id)
    captured = capsys.readouterr()
    assert("something went wrong" in captured.err)


def test_read_tenant_config_success(capsys):
    client = ConfigClient()
    assert client is not None
    tenant_id = data.get_tenant_id()
    tenant_config = client.read_tenant_config(tenant_id)
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert tenant_config is not None


def test_read_tenant_config_empty():
    client = ConfigClient()
    assert client is not None
    tenant_id = data.get_tenant_id()

    def mocked_read_tenant_config(request: pb2.ReadTenantConfigRequest):
        return None

    client.stub.ReadTenantConfig = mocked_read_tenant_config
    tenant_config = client.read_tenant_config(tenant_id)
    assert tenant_config is None


def test_update_tenant_config_mock():
    tenant_id = data.get_tenant_id()
    etag = "Random"
    tenant_config = TenantConfig(
        default_auth_flow_id=None,
        default_email_service_id=None,
        username_policy=None
        )
    bookmarks = []
    client = ConfigClient()
    assert client is not None

    def mocked_update_tenant_config(request: pb2.UpdateTenantConfigRequest):
        test_id = str(tenant_id)
        assert test_id == tenant_id
        test_etag = str(etag)
        assert test_etag == etag
        test_config = tenant_config
        assert test_config == tenant_config
        test_bookmarks = bookmarks
        assert test_bookmarks == bookmarks
        return pb2.UpdateTenantConfigResponse()

    client.stub.UpdateTenantConfig = mocked_update_tenant_config
    update = client.update_tenant_config(tenant_id, etag, tenant_config, bookmarks)
    assert update is not None


def test_update_tenant_config_wrong_id_mock(capsys):
    tenant_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"
    etag = "Random"
    tenant_config = TenantConfig(
        default_auth_flow_id=None,
        default_email_service_id=None,
        username_policy=None
    )
    bookmarks = []
    client = ConfigClient()
    assert client is not None

    def mocked_update_tenant_config(request: pb2.UpdateTenantConfigRequest):
        raise Exception("something went wrong")

    client.stub.UpdateTenantConfig = mocked_update_tenant_config
    update = client.update_tenant_config(tenant_id, etag, tenant_config, bookmarks)
    captured = capsys.readouterr()
    assert("something went wrong" in captured.err)


def test_update_tenant_config_success(capsys):
    client = ConfigClient()
    assert client is not None
    tenant_id = data.get_tenant_id()
    tenant = client.read_tenant_config(tenant_id)
    tenant_config = client.create_tenant_config(
        default_auth_flow_id=tenant.config.default_auth_flow_id,
        default_email_service_id=None,
        username_policy=None
    )
    update = client.update_tenant_config(tenant.id, tenant.etag, tenant_config,[])
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert update is not None


def test_update_tenant_config_empty():
    client = ConfigClient()
    assert client is not None
    tenant_id = data.get_tenant_id()
    etag = "Random"
    tenant_config = TenantConfig(
        default_auth_flow_id=None,
        default_email_service_id=None,
        username_policy=None
    )
    bookmarks = []

    def mocked_update_tenant_config(request: pb2.UpdateTenantConfigRequest):
        return None

    client.stub.UpdateTenantConfig = mocked_update_tenant_config
    update = client.update_tenant_config(tenant_id, etag, tenant_config, bookmarks)
    assert update is None
