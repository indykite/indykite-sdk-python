import json

from google.protobuf.json_format import MessageToDict

from indykite_sdk.model.external_data_resolver_config_content_type import ContentType

class ExternalDataResolverConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        external_data_resolver_config = ExternalDataResolverConfig(
            url=str(message_config.url),
            method=message_config.method,
        )
        if "headers" in fields:
            headers = {}
            message_dict = MessageToDict(message_config, preserving_proto_field_name=True)
            for k, v in message_dict["headers"].items():
                headers[k] = v
            external_data_resolver_config.headers = headers

        if "request_type" in fields:
            content_types = [c.value for c in ContentType]
            if message_config.request_type and message_config.request_type not in content_types:
                raise TypeError("request_type must be a member of ExternalDataResolverConfig.ContentType")
            external_data_resolver_config.request_type = message_config.request_type

        if "request_payload" in fields:
            external_data_resolver_config.request_payload = json.loads(message_config.request_payload.decode('utf-8'))

        if "response_type" in fields:
            content_types = [c.value for c in ContentType]
            if message_config.response_type and message_config.response_type not in content_types:
                raise TypeError("response_type must be a member of ExternalDataResolverConfig.ContentType")
            external_data_resolver_config.response_type = message_config.response_type

        if "response_selector" in fields:
            external_data_resolver_config.response_selector = message_config.response_selector
        return external_data_resolver_config

    def __init__(self,
                 url,
                 method,
                 headers=None,
                 request_type=None,
                 request_payload=None,
                 response_type=None,
                 response_selector= None):

        self.url = url
        self.method = method
        self.headers = headers
        self.request_type = request_type
        self.request_payload = request_payload
        self.response_type = response_type
        self.response_selector = response_selector
