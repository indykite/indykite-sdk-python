from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from indykite_sdk.config import ConfigClient
from app.config import API_PREFIX
from app.form.app_with_agent_credentials import ApplicationWithAgentCredentialsCreate
from app.utils.response import get_response, get_credentials_response, response_data
import json

__version__ = "/v1"
__bp__ = "/app_with_agent_credentials"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name=" ApplicationWithAgentCredentials", description=" ApplicationWithAgentCredentials")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post("")
def create_app_with_agent_credentials(body: ApplicationWithAgentCredentialsCreate):
    client_config = ConfigClient()
    app_with_agent_credentials = client_config.create_application_with_agent_credentials(
        body.app_space_id,
        body.tenant_id,
        body.application_name,
        body.application_agent_name,
        body.application_agent_credentials_name,
        "jwk",
        None,
        None)
    if app_with_agent_credentials:
        cred = {'ApplicationWithAgentCredentials': []}
        for k, v in app_with_agent_credentials.items():
            app = {k: []}
            if k == "response_application_agent_credentials":
                app_dict = get_credentials_response(v)
            else:
                app_dict = json.loads(get_response(v))
            app[k].append(app_dict)
            cred['ApplicationWithAgentCredentials'].append(app)
        return response_data("ApplicationWithAgentCredentialsCreate",cred)
    else:
        return response_data("ApplicationWithAgentCredentialsCreate", "Invalid app_with_agent_credentials creation")



