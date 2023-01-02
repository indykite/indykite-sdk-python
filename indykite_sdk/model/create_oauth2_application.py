from indykite_sdk.utils import timestamp_to_date


class CreateOAuth2Application:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        create_oauth2_application = CreateOAuth2Application(
            str(message.id),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.client_id),
            str(message.client_secret),
            str(message.bookmark),
        )

        return create_oauth2_application

    def __init__(self, id, create_time, update_time, etag, client_id, client_secret, bookmark):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time
        self.etag = etag
        self.client_id = client_id
        self.client_secret = client_secret
        self.bookmark = bookmark



