from indykite_sdk.utils import timestamp_to_date


class UpdateCustomerConfig:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        update_customer_config = UpdateCustomerConfig(
            str(message.id),
            timestamp_to_date(message.create_time),
            str(message.created_by),
            timestamp_to_date(message.update_time),
            str(message.updated_by),
            str(message.etag),
            str(message.bookmark)
        )
        return update_customer_config

    def __init__(self, id, create_time, created_by, update_time, updated_by, etag, bookmark):
        self.id = id
        self.create_time = create_time
        self.created_by = created_by
        self.update_time = update_time
        self.updated_by = updated_by
        self.etag = etag
        self.bookmark = bookmark
