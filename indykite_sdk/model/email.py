from indykite_sdk.indykite.config.v1beta1.model_pb2 import Email


class Email:
    @classmethod
    def deserialize(cls, message):
        return Email(message.address, message.name)

    def __init__(self, address, name):
        self.address = address
        self.name = name

    def __str__(self):
        return (f"Address: {self.address} \n "
                f"Name: {self.name} \n"
                )
