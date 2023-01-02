from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.email_service_config import EmailServiceConfig
from indykite_sdk.model.auth_flow_config import AuthFlowConfig
from indykite_sdk.model.oauth2_client_config import OAuth2ClientConfig
from indykite_sdk.model.ingest_mapping_config import IngestMappingConfig


class ConfigNode:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        config_node = ConfigNode(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.app_space_id),
            str(message.tenant_id)
        )

        if message.HasField('create_time'):
            config_node.create_time = timestamp_to_date(message.create_time)

        if message.HasField('update_time'):
            config_node.update_time = timestamp_to_date(message.update_time)

        if message.HasField('destroy_time'):
            config_node.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            config_node.delete_time = timestamp_to_date(message.delete_time)

        if message.HasField('description'):
            config_node.description = str(message.description)

        if message.HasField('email_service_config'):
            config_node.email_service_config = EmailServiceConfig.deserialize(message.email_service_config)

        if message.HasField('auth_flow_config'):
            config_node.auth_flow_config = AuthFlowConfig.deserialize(message.auth_flow_config)

        if message.HasField('oauth2_client_config'):
            config_node.oauth2_client_config = OAuth2ClientConfig.deserialize(message.oauth2_client_config)

        if message.HasField('ingest_mapping_config'):
            config_node.ingest_mapping_config = IngestMappingConfig.deserialize(message.ingest_mapping_config)

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
        self.ingest_mapping_config = None


