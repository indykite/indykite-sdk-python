from indykite_sdk.model.username_policy import UsernamePolicy


class TenantConfig:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        tenant_config = TenantConfig()

        if "default_auth_flow_id" in fields:
            tenant_config.default_auth_flow_id = str(message.default_auth_flow_id)

        if "default_email_service_id" in fields:
            tenant_config.default_email_service_id = str(message.default_email_service_id)

        if "username_policy" in fields:
            tenant_config.username_policy = UsernamePolicy.deserialize(message.username_policy)
        return tenant_config

    def __init__(self, default_auth_flow_id=None, default_email_service_id=None):
        self.default_auth_flow_id = default_auth_flow_id
        self.default_email_service_id = default_email_service_id
        self.username_policy = None
