class SendGridProviderConfig:
    @classmethod
    def deserialize(cls, message):
        return SendGridProviderConfig(
            str(message.api_key),
            bool(message.sandbox_mode),
            str(message.ip_pool_name.value),
            str(message.host.value))

    def __init__(self, api_key, sandbox_mode, ip_pool_name, host):
        self.api_key = api_key
        self.sandbox_mode = sandbox_mode
        self.ip_pool_name = ip_pool_name
        self.host = host
