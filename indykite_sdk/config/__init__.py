import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class ConfigClient(object):

    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="config",
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .customer import read_customer_by_id, read_customer_by_name
    from .service_account import read_service_account, read_service_account_by_name, create_service_account, \
        update_service_account, delete_service_account
    from .app_space import read_app_space_by_id, read_app_space_by_name, create_app_space, update_app_space, \
        list_app_spaces, delete_app_space
    from .application import read_application_by_id, read_application_by_name, create_application, update_application, \
        list_applications, delete_application
    from .application_agent import read_application_agent_by_id, read_application_agent_by_name, \
        create_application_agent, update_application_agent, \
        list_application_agents, delete_application_agent
    from .application_agent_credential import read_application_agent_credential, \
        register_application_agent_credential_jwk, register_application_agent_credential_pem, \
        delete_application_agent_credential
    from .service_account_credential import read_service_account_credential, register_service_account_credential_jwk, \
        register_service_account_credential_pem, delete_service_account_credential
    from .config_node import (read_config_node, delete_config_node,
                              create_authorization_policy_config_node, update_authorization_policy_config_node,
                              validate_authorization_policy_status, validate_conveyance,
                              authorization_policy_config, list_config_node_versions,
                              consent_config, create_consent_config_node,
                              update_consent_config_node, validate_data_points)
    from .create_application_with_agent_credentials import create_application_with_agent_credentials
    from .username_policy import username_policy
