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
        create_application_agent, update_application_agent, validate_permissions, \
        list_application_agents, delete_application_agent
    from .application_agent_credential import read_application_agent_credential, \
        register_application_agent_credential_jwk, register_application_agent_credential_pem, \
        delete_application_agent_credential
    from .service_account_credential import read_service_account_credential, register_service_account_credential_jwk, \
        register_service_account_credential_pem, delete_service_account_credential
    from .config_node import (read_config_node, delete_config_node,
                              create_authorization_policy_config_node, update_authorization_policy_config_node,
                              validate_authorization_policy_status,
                              authorization_policy_config, list_config_node_versions,
                              consent_config, create_consent_config_node,
                              update_consent_config_node, validate_data_points,
                              create_token_introspect_config_node, update_token_introspect_config_node,
                              token_introspect_config, validate_token_status,
                              validate_external_data_resolver_method,
                              validate_external_data_resolver_content_type,
                              create_external_data_resolver_config_node,
                              update_external_data_resolver_config_node,
                              external_data_resolver_config,
                              create_entity_matching_pipeline_config_node,
                              update_entity_matching_pipeline_config_node,
                              entity_matching_pipeline_config,
                              entity_matching_pipeline_config_create,
                              entity_matching_pipeline_config_update,
                              validate_entity_matching_status,
                              validate_trust_score_profile_dimension,
                              validate_trust_score_profile_update_frequency,
                              trust_score_profile_config,
                              create_trust_score_profile_config_node,
                              update_trust_score_profile_config_node,
                              trust_score_profile_config_create,
                              trust_score_profile_config_update,
                              create_knowledge_query_config_node,
                              update_knowledge_query_config_node,
                              knowledge_query_config,
                              validate_knowledge_query_status,
                              create_event_sink_config_node,
                              update_event_sink_config_node,
                              event_sink_config,
                              )
    from .create_application_with_agent_credentials import create_application_with_agent_credentials
