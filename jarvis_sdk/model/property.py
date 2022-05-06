from google.protobuf.json_format import MessageToDict
from jarvis_sdk.utils.message_to_value import object_to_value

class Property:
  def deserialize(message):
    dict = MessageToDict(message)
    value = None
    if ('referenceValue' in dict):
      value = dict['referenceValue']
    elif ('objectValue' in dict):
      value = object_to_value(message.object_value)
    return Property(dict['id'], dict['definition']['property'], dict['meta'], value)

  def __init__(self, id, property, meta, value):
    self.id = id
    self.property = property
    self.meta = meta
    self.value = value

  def __str__(self):
    return (
      "Property: " + self.property + "\n"
      "ID: " + self.id + "\n"
      "Value: " + str(self.value) + "\n"
    )
