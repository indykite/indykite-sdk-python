from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.email_service_config import EmailServiceConfig
from indykite_sdk.model.auth_flow_config import AuthFlowConfig
from indykite_sdk.model.oauth2_client_config import OAuth2ClientConfig
from indykite_sdk.model.webauthn_provider_config import WebAuthnProviderConfig
from indykite_sdk.model.authorization_policy_config import AuthorizationPolicyConfig


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
            str(message.app_space_id),
            str(message.tenant_id)
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

        if "email_service_config" in fields:
            config_node.email_service_config = EmailServiceConfig.deserialize(message.email_service_config)

        if "auth_flow_config" in fields:
            config_node.auth_flow_config = AuthFlowConfig.deserialize(message.auth_flow_config)

        if "oauth2_client_config" in fields:
            config_node.oauth2_client_config = OAuth2ClientConfig.deserialize(message.oauth2_client_config)

        if "webauthn_provider_config" in fields:
            config_node.webauthn_provider_config = WebAuthnProviderConfig.deserialize(message.webauthn_provider_config)

        if "authorization_policy_config" in fields:
            config_node.authorization_policy_config = AuthorizationPolicyConfig.deserialize(
                message.authorization_policy_config)

        if "created_by" in fields:
            config_node.created_by = str(message.created_by)

        if "updated_by" in fields:
            config_node.updated_by = str(message.updated_by)

        if "version" in fields:
            config_node.version = message.version
        return config_node

    def __init__(self, id, name, display_name, etag, customer_id, app_space_id, tenant_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.tenant_id = tenant_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None
        self.email_service_config = None
        self.auth_flow_config = None
        self.oauth2_client_config = None
        self.webauthn_provider_config = None
        self.authorization_policy_config = None
        self.knowledge_graph_schema_config = None
        self.created_by = None
        self.updated_by = None
        self.version = None


