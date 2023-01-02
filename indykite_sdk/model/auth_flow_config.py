from indykite_sdk.indykite.config.v1beta1.model_pb2 import AuthFlowConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers


class AuthFlowConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        auth_flow_config = AuthFlowConfig(
            AuthFlowConfig.Format(message_config.source_format),
            bytes(message_config.source),
            wrappers.BoolValue(message_config.default)
        )
        return auth_flow_config

    def __init__(self, source_format, source, default):

        self.source_format = source_format
        self.source = source
        self.default = default



