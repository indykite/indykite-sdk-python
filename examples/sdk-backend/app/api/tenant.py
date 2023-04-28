from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from indykite_sdk.config import ConfigClient
from app.config import API_PREFIX
from app.form.tenant import TenantById, TenantCreate
from app.utils.response import get_response, response_data
from app.utils.helper import change_display_to_name

__version__ = "/v1"
__bp__ = "/tenant"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="Tenant", description="Tenant")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post("")
def create_tenant(body: TenantCreate):
    print(body.display_name)

    client_config = ConfigClient()
    tenant = client_config.create_tenant(body.issuer_id,
                                         change_display_to_name(body.display_name),
                                         body.display_name,
                                         body.description, [])
    if tenant:
        return response_data("TenantCreate", get_response(tenant))
    else:
        return response_data("TenantCreate", "Invalid tenant creation")


@api.get("/<id>")
def get_tenant(path: TenantById):
    client_config = ConfigClient()
    tenant = client_config.get_tenant_by_id(path.id)
    if tenant:
        return response_data("TenantById", get_response(tenant))
    else:
        return response_data("TenantById", "Invalid tenant id")
