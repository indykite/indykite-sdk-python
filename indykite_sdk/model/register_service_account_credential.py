from indykite_sdk.utils import timestamp_to_date


class RegisterServiceAccountCredential:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        register_service_account_credential = RegisterServiceAccountCredential(
            str(message.id),
            str(message.service_account_id),
            str(message.kid),
            bytes(message.service_account_config),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.expire_time),
            str(message.bookmark),
        )

        return register_service_account_credential

    def __init__(self, id, service_account_id, kid, service_account_config, create_time, expire_time, bookmark):
        self.id = id
        self.service_account_id = service_account_id
        self.kid = kid
        self.service_account_config = service_account_config
        self.create_time = create_time
        self.expire_time = expire_time
        self.bookmark = bookmark



