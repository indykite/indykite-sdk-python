import sys

from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class ConfigClient:
    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="config",
                token_source=token_source,
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .app_space import (
        create_app_space,
        delete_app_space,
        list_app_spaces,
        read_app_space_by_id,
        read_app_space_by_name,
        update_app_space,
    )
    from .application import (
        create_application,
        delete_application,
        list_applications,
        read_application_by_id,
        read_application_by_name,
        update_application,
    )
    from .application_agent import (
        create_application_agent,
        delete_application_agent,
        list_application_agents,
        read_application_agent_by_id,
        read_application_agent_by_name,
        update_application_agent,
        validate_permissions,
    )
    from .application_agent_credential import (
        delete_application_agent_credential,
        read_application_agent_credential,
        register_application_agent_credential_jwk,
        register_application_agent_credential_pem,
    )
    from .config_node import (
        authorization_policy_config,
        consent_config,
        create_authorization_policy_config_node,
        create_consent_config_node,
        create_entity_matching_pipeline_config_node,
        create_event_sink_config_node,
        create_external_data_resolver_config_node,
        create_knowledge_query_config_node,
        create_token_introspect_config_node,
        create_trust_score_profile_config_node,
        delete_config_node,
        entity_matching_pipeline_config,
        entity_matching_pipeline_config_create,
        entity_matching_pipeline_config_update,
        event_sink_config,
        external_data_resolver_config,
        knowledge_query_config,
        list_config_node_versions,
        read_config_node,
        token_introspect_config,
        trust_score_profile_config,
        trust_score_profile_config_create,
        trust_score_profile_config_update,
        update_authorization_policy_config_node,
        update_consent_config_node,
        update_entity_matching_pipeline_config_node,
        update_event_sink_config_node,
        update_external_data_resolver_config_node,
        update_knowledge_query_config_node,
        update_token_introspect_config_node,
        update_trust_score_profile_config_node,
        validate_authorization_policy_status,
        validate_data_points,
        validate_entity_matching_status,
        validate_external_data_resolver_content_type,
        validate_external_data_resolver_method,
        validate_knowledge_query_status,
        validate_token_status,
        validate_trust_score_profile_dimension,
        validate_trust_score_profile_update_frequency,
    )
    from .create_application_with_agent_credentials import create_application_with_agent_credentials
    from .customer import read_customer_by_id, read_customer_by_name
    from .service_account import (
        create_service_account,
        delete_service_account,
        read_service_account,
        read_service_account_by_name,
        update_service_account,
    )
    from .service_account_credential import (
        delete_service_account_credential,
        read_service_account_credential,
        register_service_account_credential_jwk,
        register_service_account_credential_pem,
    )
