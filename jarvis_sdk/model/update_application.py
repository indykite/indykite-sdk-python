from jarvis_sdk.utils import timestamp_to_date


class UpdateApplication:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        update_application = UpdateApplication(
            str(message.id),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.bookmark),
        )

        return update_application

    def __init__(self, id, update_time, etag, bookmark):
        self.id = id
        self.update_time = update_time
        self.etag = etag
        self.bookmark = bookmark


