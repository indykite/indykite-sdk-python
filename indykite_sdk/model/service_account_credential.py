from indykite_sdk.utils import timestamp_to_date


class ServiceAccountCredential:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        service_account_credential = ServiceAccountCredential(
            str(message.id),
            str(message.kid),
            str(message.display_name),
            str(message.customer_id),
            str(message.service_account_id),
            str(message.app_space_id)
        )

        if message.HasField('create_time'):
            service_account_credential.create_time = timestamp_to_date(message.create_time)

        if message.HasField('destroy_time'):
            service_account_credential.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            service_account_credential.delete_time = timestamp_to_date(message.delete_time)

        return service_account_credential

    def __init__(self, id, kid, display_name, customer_id, service_account_id, app_space_id=None):
        self.id = id
        self.kid = kid
        self.display_name = display_name
        self.customer_id = customer_id
        self.service_account_id = service_account_id
        self.app_space_id = app_space_id
        self.create_time = None
        self.destroy_time = None
        self.delete_time = None


