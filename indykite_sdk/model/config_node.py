from indykite_sdk.model.external_data_resolver_config import ExternalDataResolverConfig
from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.authorization_policy_config import AuthorizationPolicyConfig
from indykite_sdk.model.consent_configuration import ConsentConfiguration
from indykite_sdk.model.token_introspect_config import TokenIntrospectConfig
from indykite_sdk.model.entity_matching_pipeline_config import EntityMatchingPipelineConfig


class ConfigNode:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        config_node = ConfigNode(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.app_space_id)
        )

        if "create_time" in fields:
            config_node.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            config_node.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            config_node.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            config_node.delete_time = timestamp_to_date(message.delete_time)

        if "description" in fields:
            config_node.description = str(message.description.value)

        if "authorization_policy_config" in fields:
            config_node.authorization_policy_config = AuthorizationPolicyConfig.deserialize(
                message.authorization_policy_config)

        if "consent_config" in fields:
            config_node.consent_config = ConsentConfiguration.deserialize(
                message.consent_config)

        if "token_introspect_config" in fields:
            config_node.token_introspect_config = TokenIntrospectConfig.deserialize(
                message.token_introspect_config)

        if "external_data_resolver_config" in fields:
            config_node.external_data_resolver_config = ExternalDataResolverConfig.deserialize(
                message.external_data_resolver_config)

        if "entity_matching_pipeline_config" in fields:
            config_node.entity_matching_pipeline_config = EntityMatchingPipelineConfig.deserialize(
                message.entity_matching_pipeline_config)

        if "created_by" in fields:
            config_node.created_by = str(message.created_by)

        if "updated_by" in fields:
            config_node.updated_by = str(message.updated_by)

        if "version" in fields:
            config_node.version = message.version
        return config_node

    def __init__(self, id, name, display_name, etag, customer_id, app_space_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None
        self.authorization_policy_config = None
        self.token_introspect_config = None
        self.external_data_resolver_config = None
        self.entity_matching_pipeline_config = None
        self.consent_config = None
        self.created_by = None
        self.updated_by = None
        self.version = None
