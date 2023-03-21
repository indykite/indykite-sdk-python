from enum import Enum


class AuthenticatorAttachment(Enum):
    AUTHENTICATOR_ATTACHMENT_INVALID = 0
    AUTHENTICATOR_ATTACHMENT_DEFAULT = 1
    AUTHENTICATOR_ATTACHMENT_PLATFORM = 2
    AUTHENTICATOR_ATTACHMENT_CROSS_PLATFORM = 3