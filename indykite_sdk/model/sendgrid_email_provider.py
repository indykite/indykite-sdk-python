from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers


class SendgridEmailProvider:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        sendgrid_email_provider = SendgridEmailProvider(
            str(message.api_key),
            bool(message.sandbox_mode),
            wrappers.StringValue(message.ip_pool_name),
            wrappers.StringValue(message.host)
        )
        return sendgrid_email_provider

    def __init__(self, api_key, sandbox_mode, ip_pool_name, host):
        self.api_key = api_key,
        self.sandbox_mode = sandbox_mode,
        self.ip_pool_name = ip_pool_name,
        self.host = host

