from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.tenant import Tenant
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_tenant import CreateTenant
from indykite_sdk.model.update_tenant import UpdateTenant
import sys
import indykite_sdk.utils.logger as logger


def read_tenant_by_id(self, tenant_id, bookmarks=[]):
    """
    get tenant info from its id
    :param self:
    :param tenant_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized Tenant instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadTenant(
            pb2.ReadTenantRequest(
                id=str(tenant_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return Tenant.deserialize(response.tenant)


def read_tenant_by_name(self, app_space_id, tenant_name, bookmarks=[]):
    """
    get tenant information from its name
    :param self:
    :param app_space_id: string gid id
    :param tenant_name: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized Tenant instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadTenant(
            pb2.ReadTenantRequest(
                name=UniqueNameIdentifier(
                    location=app_space_id,
                    name=tenant_name
                ),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return Tenant.deserialize(response.tenant)


def create_tenant(self,
                  issuer_id,
                  name,
                  display_name,
                  description="",
                  bookmarks=[]):
    """
    create tenant
    :param self:
    :param issuer_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateTenant instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateTenant(
            pb2.CreateTenantRequest(
                issuer_id=issuer_id,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateTenant.deserialize(response)


def update_tenant(self,
                  tenant_id,
                  etag,
                  display_name,
                  description="",
                  bookmarks=[]):
    """
    update tenant
    :param self:
    :param tenant_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateTenant instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateTenant(
            pb2.UpdateTenantRequest(
                id=tenant_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return UpdateTenant.deserialize(response)


def list_tenants(self, app_space_id, match=[], bookmarks=[]):
    """
    list tenants which match the match param
    :param self:
    :param app_space_id: string gid id
    :param match: list of strings
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: list of deserialized Tenant instances
    """
    sys.excepthook = logger.handle_excepthook
    try:
        streams = self.stub.ListTenants(
            pb2.ListTenantsRequest(
                app_space_id=app_space_id,
                match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not streams:
        return None

    try:
        res = [Tenant.deserialize(response.tenant) for response in streams]
        return res
    except Exception as exception:
        return logger.logger_error(exception)


def delete_tenant(self, tenant_id, etag, bookmarks):
    """
    delete tenant
    :param self:
    :param tenant_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteTenantResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteTenant(
            pb2.DeleteTenantRequest(
                id=tenant_id,
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response
