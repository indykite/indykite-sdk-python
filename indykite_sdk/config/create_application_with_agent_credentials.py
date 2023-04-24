from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from indykite_sdk.model.key_type import KeyType
import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.config import helper
from datetime import datetime


def create_application_with_agent_credentials(self,
                                              app_space_id,
                                              default_tenant_id,
                                              application_name,
                                              application_agent_name,
                                              application_agent_credentials_name,
                                              public_key_type,
                                              public_key=None,
                                              expire_time=None):
    """
    create application, application agent and application credentials for a tenant in an appSpace
    :param self:
    :param app_space_id: string
    :param default_tenant_id: string
    :param application_name: string
    :param application_agent_name: string
    :param application_agent_credentials_name: string
    :param public_key_type: jwk | pem
    :param public_key: bytes | None
    :param expire_time: int (number of seconds from now) | None
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        application_name_id = helper.change_display_to_name(str(application_name))
        response_application = self.create_application(app_space_id,
                                                       application_name_id,
                                                       str(application_name),
                                                       str(application_name),
                                                       [])
        if isinstance(response_application, CreateApplication):
            application_agent_name_id = helper.change_display_to_name(str(application_agent_name))
            response_application_agent = self.create_application_agent(response_application.id,
                                                                       application_agent_name_id,
                                                                       str(application_agent_name),
                                                                       str(application_agent_name),
                                                                       [])
            if isinstance(response_application_agent, CreateApplicationAgent):
                key_types = [k.value for k in KeyType]
                if public_key_type not in key_types:
                    raise TypeError("public_key_type must be a member of KeyType: jwk, pem")

                response_application_agent_credentials = None
                t = datetime.now().timestamp()
                if expire_time:
                    expire_time = int(t) + int(expire_time)
                else:
                    expire_time = int(t) + 3600
                if public_key_type == 'jwk':
                    response_application_agent_credentials = self.register_application_agent_credential_jwk(
                        response_application_agent.id,
                        application_agent_credentials_name,
                        public_key,
                        expire_time,
                        str(default_tenant_id),
                        [])
                elif public_key_type == 'pem':
                    response_application_agent_credentials = self.register_application_agent_credential_pem(
                        response_application_agent.id,
                        application_agent_credentials_name,
                        public_key,
                        expire_time,
                        str(default_tenant_id),
                        [])
                if isinstance(response_application_agent_credentials, RegisterApplicationAgentCredential):
                    response = {"response_application": response_application,
                                "response_application_agent": response_application_agent,
                                "response_application_agent_credentials": response_application_agent_credentials}
                    return response
        return None

    except Exception as exception:
        return logger.logger_error(exception)
