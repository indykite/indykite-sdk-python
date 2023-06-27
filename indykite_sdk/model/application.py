from indykite_sdk.utils import timestamp_to_date


class Application:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        application = Application(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.app_space_id)
        )

        if "create_time" in fields:
            application.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            application.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            application.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            application.delete_time = timestamp_to_date(message.delete_time)

        if "description" in fields:
            application.description = str(message.description)

        if "created_by" in fields:
            application.created_by = str(message.created_by)

        if "updated_by" in fields:
            application.updated_by = str(message.updated_by)

        return application

    def __init__(self, id, name, display_name, etag, customer_id, app_space_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None
        self.created_by = None
        self.updated_by = None


