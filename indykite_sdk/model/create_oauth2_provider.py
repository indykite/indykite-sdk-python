from indykite_sdk.utils import timestamp_to_date


class CreateOAuth2Provider:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        create_oauth2_provider = CreateOAuth2Provider(
            str(message.id),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.bookmark),
            str(message.created_by),
            str(message.updated_by)
        )

        return create_oauth2_provider

    def __init__(self, id, create_time, update_time, etag, bookmark, created_by, updated_by):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time
        self.etag = etag
        self.bookmark = bookmark
        self.created_by = created_by
        self.updated_by = updated_by
