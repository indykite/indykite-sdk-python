# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/objects/v1beta1/struct.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.type import latlng_pb2 as google_dot_type_dot_latlng__pb2
from jarvis_sdk.indykite.objects.v1beta1 import id_pb2 as indykite_dot_objects_dot_v1beta1_dot_id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%indykite/objects/v1beta1/struct.proto\x12\x18indykite.objects.v1beta1\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x18google/type/latlng.proto\x1a!indykite/objects/v1beta1/id.proto\"\x8e\x06\n\x05Value\x12;\n\nnull_value\x18\x01 \x01(\x0e\x32\x1a.google.protobuf.NullValueH\x00R\tnullValue\x12\x1f\n\nbool_value\x18\x02 \x01(\x08H\x00R\tboolValue\x12%\n\rinteger_value\x18\x03 \x01(\x03H\x00R\x0cintegerValue\x12\x36\n\x16unsigned_integer_value\x18\x0e \x01(\x04H\x00R\x14unsignedIntegerValue\x12#\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00R\x0b\x64oubleValue\x12\x33\n\tany_value\x18\x05 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00R\x08\x61nyValue\x12;\n\nvalue_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R\tvalueTime\x12\x42\n\x0e\x64uration_value\x18\x0c \x01(\x0b\x32\x19.google.protobuf.DurationH\x00R\rdurationValue\x12Q\n\x10identifier_value\x18\r \x01(\x0b\x32$.indykite.objects.v1beta1.IdentifierH\x00R\x0fidentifierValue\x12#\n\x0cstring_value\x18\x07 \x01(\tH\x00R\x0bstringValue\x12!\n\x0b\x62ytes_value\x18\x08 \x01(\x0cH\x00R\nbytesValue\x12=\n\x0fgeo_point_value\x18\t \x01(\x0b\x32\x13.google.type.LatLngH\x00R\rgeoPointValue\x12G\n\x0b\x61rray_value\x18\n \x01(\x0b\x32$.indykite.objects.v1beta1.ArrayValueH\x00R\narrayValue\x12\x41\n\tmap_value\x18\x0b \x01(\x0b\x32\".indykite.objects.v1beta1.MapValueH\x00R\x08mapValueB\x07\n\x05value\"E\n\nArrayValue\x12\x37\n\x06values\x18\x01 \x03(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x06values\"\xae\x01\n\x08MapValue\x12\x46\n\x06\x66ields\x18\x01 \x03(\x0b\x32..indykite.objects.v1beta1.MapValue.FieldsEntryR\x06\x66ields\x1aZ\n\x0b\x46ieldsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x42\xdf\x01\n\x1c\x63om.indykite.objects.v1beta1B\x0bStructProtoP\x01Z0github.com/indykite/jarvis/pkg/proto-gen/objects\xa2\x02\x03IOX\xaa\x02\x18Indykite.Objects.V1beta1\xca\x02\x18Indykite\\Objects\\V1beta1\xe2\x02$Indykite\\Objects\\V1beta1\\GPBMetadata\xea\x02\x1aIndykite::Objects::V1beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.objects.v1beta1.struct_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034com.indykite.objects.v1beta1B\013StructProtoP\001Z0github.com/indykite/jarvis/pkg/proto-gen/objects\242\002\003IOX\252\002\030Indykite.Objects.V1beta1\312\002\030Indykite\\Objects\\V1beta1\342\002$Indykite\\Objects\\V1beta1\\GPBMetadata\352\002\032Indykite::Objects::V1beta1'
  _MAPVALUE_FIELDSENTRY._options = None
  _MAPVALUE_FIELDSENTRY._serialized_options = b'8\001'
  _VALUE._serialized_start=251
  _VALUE._serialized_end=1033
  _ARRAYVALUE._serialized_start=1035
  _ARRAYVALUE._serialized_end=1104
  _MAPVALUE._serialized_start=1107
  _MAPVALUE._serialized_end=1281
  _MAPVALUE_FIELDSENTRY._serialized_start=1191
  _MAPVALUE_FIELDSENTRY._serialized_end=1281
# @@protoc_insertion_point(module_scope)
