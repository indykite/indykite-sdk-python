from indykite_sdk.utils import timestamp_to_date


class CreateServiceAccount:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        create_service_account = CreateServiceAccount(
            str(message.id),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.bookmark)
        )
        if "created_by" in fields:
            create_service_account.created_by = str(message.created_by)

        if "updated_by" in fields:
            create_service_account.updated_by = str(message.updated_by)

        return create_service_account

    def __init__(self, id, create_time, update_time, etag, bookmark):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time
        self.etag = etag
        self.bookmark = bookmark
        self.created_by = None
        self.updated_by = None
