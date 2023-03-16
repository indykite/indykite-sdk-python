from indykite_sdk.model.batch_operation_result_success import BatchOperationResultSuccess
from indykite_sdk.model.batch_operation_result_error import BatchOperationResultError


class BatchOperationResult:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        batch_operation_result = BatchOperationResult()
        if "index" in fields:
            batch_operation_result.index = message.index
        if "success" in fields:
            batch_operation_result.success = BatchOperationResultSuccess.deserialize(message.success)
        if "error" in fields:
            batch_operation_result.error = BatchOperationResultError.deserialize(message.error)
        return batch_operation_result

    def __init__(self, index=None, success=None, error=None):
        self.index = index
        self.success = success
        self.error = error

