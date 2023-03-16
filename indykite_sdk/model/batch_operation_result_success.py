class BatchOperationResultSuccess:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        batch_operation_result_success = BatchOperationResultSuccess(message.property_id)
        return batch_operation_result_success

    def __init__(self, property_id):
        self.property_id = property_id
