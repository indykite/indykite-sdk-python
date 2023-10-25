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
    from .customer import read_customer_by_id, read_customer_by_name, read_customer_config, update_customer_config, \
        create_customer_config
    from .service_account import read_service_account, read_service_account_by_name, create_service_account, \
        update_service_account, delete_service_account
    from .app_space import read_app_space_by_id, read_app_space_by_name, create_app_space, update_app_space, \
        list_app_spaces, delete_app_space, read_app_space_config, update_app_space_config, create_app_space_config, \
        unique_property_constraints
    from .tenant import read_tenant_by_id, read_tenant_by_name, create_tenant, update_tenant, list_tenants, \
        delete_tenant, create_tenant_config, update_tenant_config, read_tenant_config
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
    from .config_node import create_email_service_config_node, read_config_node, \
        update_email_service_config_node, delete_config_node, create_auth_flow_config_node, \
        update_auth_flow_config_node, \
        create_oauth2_client_config_node, update_oauth2_client_config_node, \
        create_webauthn_provider_config_node, update_webauthn_provider_config_node, \
        create_authorization_policy_config_node, update_authorization_policy_config_node, \
        create_knowledge_graph_schema_config_node, update_knowledge_graph_schema_config_node, \
        knowledge_graph_schema_config, validate_authenticator_attachment, validate_authorization_policy_status, \
        validate_user_verification, validate_conveyance, authorization_policy_config, webauthn_provider_config, \
        auth_flow_config, list_config_node_versions
    from .oauth2_provider import create_oauth2_provider, read_oauth2_provider, update_oauth2_provider, \
        delete_oauth2_provider
    from .oauth2_application import create_oauth2_application, read_oauth2_application, update_oauth2_application, \
        delete_oauth2_application
    from .create_application_with_agent_credentials import create_application_with_agent_credentials
    from .get_schema import get_schema_helpers
    from .username_policy import username_policy
