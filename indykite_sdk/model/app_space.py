from indykite_sdk.utils import timestamp_to_date


class ApplicationSpace:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        application_space = ApplicationSpace(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id),
            str(message.issuer_id)
        )

        if message.HasField('create_time'):
            application_space.create_time = timestamp_to_date(message.create_time)

        if message.HasField('update_time'):
            application_space.update_time = timestamp_to_date(message.update_time)

        if message.HasField('destroy_time'):
            application_space.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            application_space.delete_time = timestamp_to_date(message.delete_time)

        if message.HasField('description'):
            application_space.description = str(message.description)

        return application_space

    def __init__(self, id, name, display_name, etag, customer_id,issuer_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.issuer_id = issuer_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None


