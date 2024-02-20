from indykite_sdk.indykite.ingest.v1beta3 import model_pb2
from google.protobuf.json_format import MessageToDict


class StreamRecordsResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        stream_records = StreamRecordsResponse(
            str(message.record_id),
            int(message.record_index)
        )
        if "record_error" in fields:
            stream_records.record_error = message.record_error

        if "status_error" in fields:
            stream_records.status_error = message.status_error

        if "info" in fields:
            info = Info.deserialize(message.info)
            changes = list(map(Change.deserialize, info.changes))
            stream_records.info = changes

        return stream_records

    def __init__(self, record_id, record_index):
        self.record_id = record_id
        self.record_index = record_index
        self.record_error = None
        self.status_error = None
        self.info = None


class IngestRecordResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        ingest_records = IngestRecordResponse(
            str(message.record_id)
        )

        if "info" in fields:
            info = Info.deserialize(message.info)
            changes = []
            if info.changes:
                changes = list(map(Change.deserialize, info.changes))
            ingest_records.info = changes

        return ingest_records

    def __init__(self, record_id):
        self.record_id = record_id
        self.info = None


class Change:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        dict_message = MessageToDict(message)
        if dict_message:
            if "id" in fields:
                return Change(dict_message['id'], dict_message['dataType'])
            return Change(None, dict_message['dataType'])
        return None

    def __init__(self, id=None, data_type=None):
        self.id = id
        self.data_type = data_type


class Info:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        info = model_pb2.Info(
            changes=message.changes
        )
        return info

    def __init__(self, changes=[]):
        self.changes = changes
