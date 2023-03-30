from google.protobuf.timestamp_pb2 import Timestamp


def timestamp_to_date(timestamp):
    if timestamp is None:
        return None

    return timestamp.ToDatetime()


def date_to_timestamp(date):
    if date is None:
        return None

    timestamp = Timestamp()
    timestamp.FromDatetime(date)
    return timestamp


def duration_to_seconds(duration):
    if duration is None:
        return None

    return duration.ToSeconds()
