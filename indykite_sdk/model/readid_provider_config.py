class ReadIdProviderConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        readid_provider_config = ReadIdProviderConfig(
            message_config.submitter_secret,
            message_config.manager_secret,
            message_config.submitter_password,
            message_config.host_address
        )
        if "property_map" in fields:
            property_map = {}
            for k, v in message_config.property_map.items():
                property_map[k] = Property.deserialize(v)
            readid_provider_config.property_map = property_map

        if "unique_property_name" in fields:
            readid_provider_config.unique_property_name = message_config.unique_property_name

        return readid_provider_config

    def __init__(self, submitter_secret, manager_secret, submitter_password, host_address, property_map={},
                 unique_property_name=None):
        self.submitter_secret = submitter_secret
        self.manager_secret = manager_secret
        self.submitter_password = submitter_password
        self.host_address = host_address
        self.property_map = property_map
        self.unique_property_name = unique_property_name


class Property:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        readid_property = Property(message.expression, message.enabled)
        return readid_property

    def __init__(self, expression, enabled=True):
        self.expression = expression
        self.enabled = enabled

