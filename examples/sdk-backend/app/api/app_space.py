from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from indykite_sdk.config import ConfigClient
from app.config import API_PREFIX
from app.form.app_space import AppSpaceById, AppSpaceCreate
from app.utils.response import get_response, response_data
from app.utils.helper import change_display_to_name

__version__ = "/v1"
__bp__ = "/app_space"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="AppSpace", description="AppSpace")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post("")
def create_app_space(body: AppSpaceCreate):
    client_config = ConfigClient()
    app_space = client_config.create_app_space(body.customer_id,
                                               change_display_to_name(body.display_name),
                                               body.display_name,
                                               body.description,
                                               [])
    if app_space:
        return response_data("AppSpaceCreate", get_response(app_space))
    else:
        return response_data("AppSpaceCreate", "Invalid app_space creation")


@api.get("/<id>")
def get_app_space(path: AppSpaceById):
    client_config = ConfigClient()
    app_space = client_config.get_app_space_by_id(path.id)
    if app_space:
        return response_data("AppSpaceById", get_response(app_space))
    else:
        return response_data("AppSpaceById", "Invalid app_space id")
