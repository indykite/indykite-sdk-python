import json


class ConsentConfiguration:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        data_points = None
        if "data_points" in fields:
            data_points = [
                str(t)
                for t in message_config.data_points
            ]
        consent_config = ConsentConfiguration(
            purpose=str(message_config.purpose),
            data_points=data_points,
            application_id=str(message_config.application_id)
        )

        return consent_config

    def __init__(self, purpose, data_points, application_id):

        self.purpose = purpose
        self.data_points = data_points
        self.application_id = application_id



