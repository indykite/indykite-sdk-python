from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier


class UniqueNameIdentifier:
    @classmethod
    def deserialize(cls, message):
        return UniqueNameIdentifier(message.location, message.name)

    def __init__(self, location, name):
        self.location = location
        self.name = name

    def __str__(self):
        return (
            "Location: " + self.location + "\n"
            "Name: " + self.name
        )
