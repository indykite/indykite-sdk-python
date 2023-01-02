from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.tenant import Tenant
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_tenant import CreateTenant
from indykite_sdk.model.update_tenant import UpdateTenant


def get_tenant_by_id(self, tenant_id):
    try:
        response = self.stub.ReadTenant(
            pb2.ReadTenantRequest(
                id=str(tenant_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Tenant.deserialize(response.tenant)


def get_tenant_by_name(self, app_space_id, tenant_name):

    try:
        response = self.stub.ReadTenant(
            pb2.ReadTenantRequest(
                name=UniqueNameIdentifier(location = app_space_id, name = tenant_name)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Tenant.deserialize(response.tenant)


def create_tenant(self, issuer_id, name, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.CreateTenant(
            pb2.CreateTenantRequest(
                issuer_id=issuer_id,name=name, display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return CreateTenant.deserialize(response)


def update_tenant(self, tenant_id, etag, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.UpdateTenant(
            pb2.UpdateTenantRequest(
                id=tenant_id,etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return UpdateTenant.deserialize(response)


def list_tenants(self, app_space_id, match=[], bookmarks=[]):

    try:
        streams = self.stub.ListTenants(
            pb2.ListTenantsRequest(
                app_space_id=app_space_id,match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        print(exception)
        return None

    return responses


def delete_tenant(self, tenant_id, etag, bookmarks):

    try:
        response = self.stub.DeleteTenant(
            pb2.DeleteTenantRequest(
                id=tenant_id, etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response
