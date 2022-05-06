from jarvis_sdk.indykite.identity.v1beta1.model_pb2 import PostalAddress as PostalAddressPb
from jarvis_sdk.model.postal_address import PostalAddress
from google.protobuf.json_format import MessageToDict, MessageToJson, Parse, ParseDict

from jarvis_sdk.indykite.identity.v1beta1.identity_management_api_pb2 import CreateInvitationRequest

def object_to_value(object):
  if (object.HasField('null_value')):
    return object.null_value
  elif (object.HasField('bool_value')):
    return object.bool_value
  elif (object.HasField('integer_value')):
    return object.integer_value
  elif (object.HasField('unsigned_integer_value')):
    return object.unsigned_integer_value
  elif (object.HasField('double_value')):
    return object.double_value
  elif (object.HasField('value_time')):
    return object.value_time
  elif (object.HasField('duration_value')):
    return object.duration_value
  elif (object.HasField('identifier_value')):
    return object.identifier_value
  elif (object.HasField('string_value')):
    return object.string_value
  elif (object.HasField('bytes_value')):
    return object.bytes_value
  elif (object.HasField('geo_point_value')):
    return object.geo_point_value
  elif (object.HasField('any_value')):
    if (object.any_value.Is(PostalAddressPb.DESCRIPTOR)):
      return PostalAddress.deserialize(object.any_value)
    return object.any_value
  elif (object.HasField('array_value')):
    return list(map(object_to_value, object.array_value.values))
  elif (object.HasField('map_value')):
    fields = object.map_value.fields
    keys = fields.keys()
    mapped = {}
    for key in keys:
      mapped[key] = object_to_value(fields[key])
    return mapped
  
  return None
