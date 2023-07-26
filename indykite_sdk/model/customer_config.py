class CustomerConfig:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        customer_config = CustomerConfig()
        if "default_auth_flow_id" in fields:
            customer_config.default_auth_flow_id = str(message.default_auth_flow_id)

        if "default_email_service_id" in fields:
            customer_config.default_email_service_id = str(message.default_email_service_id)

        return customer_config

    def __init__(self, default_auth_flow_id=None, default_email_service_id=None):
        self.default_auth_flow_id = default_auth_flow_id
        self.default_email_service_id = default_email_service_id
