from jarvis_sdk.indykite.identity.v1beta1.model_pb2 import ProviderType

class ProviderInfo:
  def deserialize(message):
    return ProviderInfo(message.type, message.issuer)

  def __init__(self, type, issuer):
    self.type = ProviderType.Name(type)
    self.issuer = issuer

  def __str__(self):
    return (
      "Type: " + self.type + "\n"
      "Issuer: " + self.issuer
    )
