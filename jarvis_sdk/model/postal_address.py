from jarvis_sdk.indykite.identity.v1beta1.model_pb2 import PostalAddress as PostalAddressPb
from google.protobuf.json_format import MessageToDict

class PostalAddress:
  def deserialize(message):
    if not message.Is(PostalAddressPb.DESCRIPTOR):
      return None

    dict = MessageToDict(message)
    return PostalAddress(
      dict.get('addressType', ''),
      dict.get('addressCountry', ''),
      dict.get('addressCountryCode', ''),
      dict.get('addressLocality', ''),
      dict.get('addressRegion', ''),
      dict.get('postOfficeBoxNumber', ''),
      dict.get('postalCode', ''),
      dict.get('streetAddress', ''),
      dict.get('formatted', '')
    )

  def __init__(self, addressType, addressCountry, addressCountryCode, addressLocality, addressRegion, postOfficeBoxNumber, postalCode, streetAddress, formatted):
    self.addressType = addressType
    self.addressCountry = addressCountry
    self.addressCountryCode = addressCountryCode
    self.addressLocality = addressLocality
    self.addressRegion = addressRegion
    self.postOfficeBoxNumber = postOfficeBoxNumber
    self.postalCode = postalCode
    self.streetAddress = streetAddress
    self.formatted = formatted

  def __str__(self):
    if self.formatted:
      return self.formatted
    else:
      return '<Postal Address object>'
