class BatchOperationResultError:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        messages = []
        for e in message.message:
            messages.append(BatchOperationResultError(e))
        return messages

    def __init__(self, message):
        self.message = message
