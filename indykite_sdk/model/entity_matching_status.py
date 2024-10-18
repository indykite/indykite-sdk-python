from enum import Enum


class Status(Enum):
    STATUS_INVALID = 0
    STATUS_PENDING = 1
    STATUS_IN_PROGRESS = 2
    STATUS_SUCCESS = 3
    STATUS_ERROR = 4
