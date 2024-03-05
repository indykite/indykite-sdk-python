'''Converts gRPC object to a value'''
from indykite_sdk.indykite.identity.v1beta2.model_pb2 import PostalAddress as PostalAddressPb
from indykite_sdk.model.postal_address import PostalAddress
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as struct
from indykite_sdk.indykite.objects.v1beta2 import value_pb2 as value


def object_to_value(grpc_object):
    '''Converts gRPC object to a struct value'''

    if grpc_object.HasField('null_value'):
        return grpc_object.null_value

    if grpc_object.HasField('bool_value'):
        return grpc_object.bool_value

    if grpc_object.HasField('integer_value'):
        return grpc_object.integer_value

    if grpc_object.HasField('unsigned_integer_value'):
        return grpc_object.unsigned_integer_value

    if grpc_object.HasField('double_value'):
        return grpc_object.double_value

    if grpc_object.HasField('value_time'):
        return grpc_object.value_time

    if grpc_object.HasField('duration_value'):
        return grpc_object.duration_value

    if grpc_object.HasField('string_value'):
        return grpc_object.string_value

    if grpc_object.HasField('bytes_value'):
        return grpc_object.bytes_value

    if grpc_object.HasField('geo_point_value'):
        return grpc_object.geo_point_value

    if grpc_object.HasField('any_value'):
        if grpc_object.any_value.Is(PostalAddressPb.DESCRIPTOR):
            return PostalAddress.deserialize(grpc_object.any_value)
        return grpc_object.any_value

    if grpc_object.HasField('array_value'):
        return list(map(object_to_value, grpc_object.array_value.values))

    if grpc_object.HasField('map_value'):
        fields = grpc_object.map_value.fields
        keys = fields.keys()
        mapped = {}
        for key in keys:
            mapped[key] = object_to_value(fields[key])
        return mapped

    return None


def grpc_to_value(grpc_object):
    '''Converts gRPC object to a value v2'''

    if grpc_object.HasField('bool_value'):
        return grpc_object.bool_value

    if grpc_object.HasField('integer_value'):
        return grpc_object.integer_value

    if grpc_object.HasField('double_value'):
        return grpc_object.double_value

    if grpc_object.HasField('time_value'):
        return grpc_object.time_value

    if grpc_object.HasField('duration_value'):
        return grpc_object.duration_value

    if grpc_object.HasField('string_value'):
        return grpc_object.string_value

    if grpc_object.HasField('bytes_value'):
        return grpc_object.bytes_value

    if grpc_object.HasField('array_value'):
        return list(map(object_to_value, grpc_object.array_value.values))

    if grpc_object.HasField('map_value'):
        fields = grpc_object.map_value.fields
        keys = fields.keys()
        mapped = {}
        for key in keys:
            mapped[key] = object_to_value(fields[key])
        return mapped

    return None


def arg_to_value(value):
    if not value:
        return struct.Value(null_value=value)

    if isinstance(value, int):
        return struct.Value(integer_value=value)

    if isinstance(value, bool):
        return struct.Value(bool_value=value)

    if isinstance(value, float):
        return struct.Value(double_value=value)

    if isinstance(value, str):
        return struct.Value(string_value=value)

    if isinstance(value, bytes):
        return struct.Value(bytes_value=value)

    if isinstance(value, dict):
        keys = value.keys()
        mapped = {}
        for key in keys:
            mapped[key] = arg_to_value(value[key])
        return struct.MapValue(fields=mapped)

    return None


def param_to_value(v):
    if not v:
        return None

    if isinstance(v, int):
        return value.Value(integer_value=v)

    if isinstance(v, bool):
        return value.Value(bool_value=v)

    if isinstance(v, float):
        return value.Value(double_value=v)

    if isinstance(v, str):
        return value.Value(string_value=v)

    if isinstance(v, bytes):
        return value.Value(bytes_value=v)

    if isinstance(v, dict):
        keys = v.keys()
        mapped = {}
        for key in keys:
            mapped[key] = param_to_value(v[key])
        return struct.MapValue(fields=mapped)

    return None
