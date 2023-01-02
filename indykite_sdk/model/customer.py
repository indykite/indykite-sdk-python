from indykite_sdk.utils import timestamp_to_date


class Customer:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        customer = Customer(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag)
        )

        if message.HasField('create_time'):
            customer.create_time = timestamp_to_date(message.create_time)

        if message.HasField('update_time'):
            customer.update_time = timestamp_to_date(message.update_time)

        if message.HasField('destroy_time'):
            customer.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            customer.delete_time = timestamp_to_date(message.delete_time)

        if message.HasField('description'):
            customer.description = str(message.description)

        return customer

    def __init__(self, id, name, display_name, etag):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.etag = etag
        self.create_time = None
        self.update_time = None
        self.destroy_time = None
        self.delete_time = None
        self.description = None


