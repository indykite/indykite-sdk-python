from indykite_sdk.model.customer_config import CustomerConfig
from indykite_sdk.utils import timestamp_to_date


class ReadCustomerConfig:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        read_customer_config = ReadCustomerConfig(
            str(message.id),
            str(message.etag)
        )

        if "config" in fields:
            read_customer_config.config = CustomerConfig.deserialize(message.config)

        if "create_time" in fields:
            read_customer_config.create_time = timestamp_to_date(message.create_time)

        if "created_by" in fields:
            read_customer_config.created_by = str(message.created_by)

        if "update_time" in fields:
            read_customer_config.update_time = timestamp_to_date(message.update_time)

        if "updated_by" in fields:
            read_customer_config.updated_by = str(message.updated_by)

        return read_customer_config

    def __init__(self, id, etag, config=None):
        self.id = id
        self.etag = etag
        self.config = config
        self.create_time = None
        self.created_by = None
        self.update_time = None
        self.updated_by = None
