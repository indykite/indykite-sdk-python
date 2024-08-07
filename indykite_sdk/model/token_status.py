from enum import Enum


class ExternalTokenStatus(Enum):
    EXTERNAL_TOKEN_STATUS_INVALID = 0
    EXTERNAL_TOKEN_STATUS_ENFORCE = 1
    EXTERNAL_TOKEN_STATUS_ALLOW = 2
    EXTERNAL_TOKEN_STATUS_DISALLOW = 3
