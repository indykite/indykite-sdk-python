import json


class AuthFlowConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        auth_flow_config = AuthFlowConfig(
            str(message_config.source_format),
            json.loads(message_config.source.decode('utf-8')),
            bool(message_config.default)
        )
        return auth_flow_config

    def __init__(self, source_format, source, default):

        self.source_format = source_format
        self.source = source
        self.default = default



