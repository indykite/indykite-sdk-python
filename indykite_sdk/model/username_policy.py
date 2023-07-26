from indykite_sdk.utils import duration_to_seconds


class UsernamePolicy:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        username_policy = UsernamePolicy()
        if "allowed_username_formats" in fields:
            username_policy.allowed_username_formats = [
                str(t)
                for t in message.allowed_username_formats
            ]
        if "valid_email" in fields:
            username_policy.valid_email = bool(message.valid_email)
        if "verify_email" in fields:
            username_policy.verify_email = bool(message.verify_email)
        if "verify_email_grace_period" in fields:
            username_policy.verify_email_grace_period = duration_to_seconds(message.verify_email_grace_period)

        if "allowed_email_domains" in fields:
            username_policy.allowed_email_domains = [
                str(t)
                for t in message.allowed_email_domains
            ]
        if "exclusive_email_domains" in fields:
            username_policy.exclusive_email_domains = [
                str(t)
                for t in message.exclusive_email_domains
            ]
        return username_policy

    def __init__(self,
                 allowed_username_formats=[],
                 valid_email=False,
                 verify_email=False,
                 verify_email_grace_period=None,
                 allowed_email_domains=[],
                 exclusive_email_domains=[]
                 ):
        self.allowed_username_formats = allowed_username_formats
        self.valid_email = valid_email
        self.verify_email = verify_email
        self.verify_email_grace_period = verify_email_grace_period
        self.allowed_email_domains = allowed_email_domains
        self.exclusive_email_domains = exclusive_email_domains
