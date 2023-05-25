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

        return stream_records

    def __init__(self, record_id, record_index):
        self.record_id = record_id
        self.record_index = record_index
        self.record_error = None
        self.status_error = None


class IngestRecordResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        stream_records = IngestRecordResponse(
            str(message.record_id)
        )
        if "record_error" in fields:
            stream_records.record_error = message.record_error

        if "status_error" in fields:
            stream_records.status_error = message.status_error

        return stream_records

    def __init__(self, record_id):
        self.record_id = record_id
        self.record_error = None
        self.status_error = None
