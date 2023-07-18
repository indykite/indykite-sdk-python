from indykite_sdk.model.digital_twin import DigitalTwinCore


class CreateCustomLoginToken:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        create_custom_login_token = CreateCustomLoginToken(
            str(message.token),
            DigitalTwinCore.deserialize(message.digital_twin)
        )
        return create_custom_login_token

    def __init__(self, token, digital_twin):
        self.token = token
        self.digital_twin = digital_twin
