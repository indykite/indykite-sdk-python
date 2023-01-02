from indykite_sdk.utils import timestamp_to_date


class ServiceAccount:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        service_account = ServiceAccount(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id)
        )

        if message.HasField('create_time'):
            service_account.create_time = timestamp_to_date(message.create_time)

        if message.HasField('update_time'):
            service_account.update_time = timestamp_to_date(message.update_time)

        if message.HasField('destroy_time'):
            service_account.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            service_account.delete_time = timestamp_to_date(message.delete_time)

        return service_account

    def __init__(self, id, name, display_name, etag, customer_id):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.customer_id = customer_id
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None


