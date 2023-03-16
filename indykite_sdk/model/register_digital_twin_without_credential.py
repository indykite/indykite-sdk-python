from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.model.batch_operation_result import BatchOperationResult


class RegisterDigitalTwinWithoutCredential:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        fields = [desc.name for desc, val in message.ListFields()]
        register_digital_twin_without_credential = RegisterDigitalTwinWithoutCredential(
            digital_twin=DigitalTwinCore(
                message.digital_twin.id,
                message.digital_twin.tenant_id,
                message.digital_twin.kind,
                message.digital_twin.state),
        )
        if "results" in fields:
            results = []
            for e in message.results:
                results.append(BatchOperationResult.deserialize(e))
            register_digital_twin_without_credential.results = results
        if "bookmark" in fields:
            register_digital_twin_without_credential.bookmark = str(message.bookmark)
        return register_digital_twin_without_credential

    def __init__(self, digital_twin, results=None, bookmark=None):
        self.digital_twin = digital_twin
        self.results = results
        self.bookmark = bookmark
