from indykite_sdk.utils import timestamp_to_date


class CreateApplicationAgent:
    @classmethod
    def deserialize(cls, message, application_id, name):
        if message is None:
            return None

        create_application_agent = CreateApplicationAgent(
            str(message.id),
            str(application_id),
            str(name),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.update_time),
            str(message.etag),
            str(message.bookmark),
            str(message.created_by),
            str(message.updated_by)
        )

        return create_application_agent

    def __init__(self, id, application_id, name, create_time, update_time, etag, bookmark, created_by, updated_by):
        self.id = id
        self.application_id = application_id
        self.name = name
        self.create_time = create_time
        self.update_time = update_time
        self.etag = etag
        self.bookmark = bookmark
        self.created_by = created_by
        self.updated_by = updated_by



