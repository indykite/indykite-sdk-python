from indykite_sdk.utils import timestamp_to_date


class ServiceAccount:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        service_account = ServiceAccount(
            str(message.id),
            str(message.name),
            str(message.display_name),
            str(message.etag),
            str(message.customer_id)
        )

        if "app_space_id" in fields:
            service_account.app_space_id = str(message.app_space_id)

        if "description" in fields:
            service_account.description = str(message.description)

        if "create_time" in fields:
            service_account.create_time = timestamp_to_date(message.create_time)

        if "update_time" in fields:
            service_account.update_time = timestamp_to_date(message.update_time)

        if "destroy_time" in fields:
            service_account.destroy_time = timestamp_to_date(message.destroy_time)

        if "delete_time" in fields:
            service_account.delete_time = timestamp_to_date(message.delete_time)

        if "created_by" in fields:
            service_account.created_by = str(message.created_by)

        if "updated_by" in fields:
            service_account.updated_by = str(message.updated_by)

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
        self.app_space_id = None
        self.created_by = None
        self.updated_by = None
        self.description = None


