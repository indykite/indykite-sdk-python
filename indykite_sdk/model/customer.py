from indykite_sdk.utils import timestamp_to_date


class Customer:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        customer = Customer(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag)
        )

        if "create_time" in fields:
            customer.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            customer.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            customer.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            customer.delete_time = timestamp_to_date(message.delete_time)

        if "description" in fields:
            customer.description = str(message.description)

        if "created_by" in fields:
            customer.created_by = str(message.created_by)

        if "updated_by" in fields:
            customer.updated_by = str(message.updated_by)

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
        self.created_by = None
        self.updated_by = None
