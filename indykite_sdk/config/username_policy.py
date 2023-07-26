from indykite_sdk.indykite.config.v1beta1.model_pb2 import UsernamePolicy


def username_policy(self,
                    allowed_username_formats=[],
                    valid_email=False,
                    verify_email=False,
                    verify_email_grace_period=None,
                    allowed_email_domains=[],
                    exclusive_email_domains=[]
                    ):
    """
    create UsernamePolicy
    :param self:
    :param allowed_username_formats: [] various formats as user identifier for humans
    :param valid_email:  bool
    :param verify_email:  bool
    :param verify_email_grace_period:  google.protobuf.Duration
    :param allowed_email_domains:  [] Allowed email domains to register
    :param exclusive_email_domains:  [] Unique email domain in AppSpace
    :return: UsernamePolicy object
    """
    policy = UsernamePolicy(
        allowed_username_formats=allowed_username_formats,
        valid_email=bool(valid_email),
        verify_email=bool(verify_email),
        verify_email_grace_period=verify_email_grace_period,
        allowed_email_domains=allowed_email_domains,
        exclusive_email_domains=exclusive_email_domains
        )
    return policy
