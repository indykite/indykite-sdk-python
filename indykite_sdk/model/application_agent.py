from indykite_sdk.utils import timestamp_to_date


class ApplicationAgent:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        application_agent = ApplicationAgent(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.app_space_id),
            str(message.application_id)
        )

        if message.HasField('create_time'):
            application_agent.create_time = timestamp_to_date(message.create_time)

        if message.HasField('update_time'):
            application_agent.update_time = timestamp_to_date(message.update_time)

        if message.HasField('destroy_time'):
            application_agent.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            application_agent.delete_time = timestamp_to_date(message.delete_time)

        if message.HasField('description'):
            application_agent.description = str(message.description)

        return application_agent

    def __init__(self, id, name, display_name, etag, customer_id, app_space_id, application_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.application_id = application_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None


