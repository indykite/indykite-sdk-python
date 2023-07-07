from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2

class ChangePassword:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        if "error" in fields:
            change_password = ChangePassword(error=pb2.Error(code=message.error.code))
        else:
            change_password = "The password has been changed successfully"
        return change_password

    def __init__(self, error=None):
        self.error = error
