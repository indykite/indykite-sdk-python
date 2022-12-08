from jarvis_sdk.utils import timestamp_to_date


class CreateConfigNode:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        create_config_node = CreateConfigNode(
            str(message.id),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.bookmark),
        )

        return create_config_node

    def __init__(self, id, create_time, update_time, etag, bookmark):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time
        self.etag = etag
        self.bookmark = bookmark



