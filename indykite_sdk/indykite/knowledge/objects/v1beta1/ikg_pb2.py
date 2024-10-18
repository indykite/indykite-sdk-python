# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/knowledge/objects/v1beta1/ikg.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2
from indykite_sdk.indykite.objects.v1beta2 import value_pb2 as indykite_dot_objects_dot_v1beta2_dot_value__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,indykite/knowledge/objects/v1beta1/ikg.proto\x12\"indykite.knowledge.objects.v1beta1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%indykite/objects/v1beta1/struct.proto\x1a$indykite/objects/v1beta2/value.proto\x1a\x17validate/validate.proto\"\xb2\x03\n\x04Node\x12#\n\x02id\x18\x01 \x01(\tB\x13\xfa\x42\x10r\x0e\x10\x16\x18\x80\x02:\x04gid:\xd0\x01\x01R\x02id\x12+\n\x0b\x65xternal_id\x18\x02 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\x80\x02R\nexternalId\x12-\n\x04type\x18\x03 \x01(\tB\x19\xfa\x42\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04type\x12\x36\n\x04tags\x18\x04 \x03(\tB\"\xfa\x42\x1f\x92\x01\x1c\x10\n\x18\x01\"\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04tags\x12;\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12V\n\nproperties\x18\x07 \x03(\x0b\x32,.indykite.knowledge.objects.v1beta1.PropertyB\x08\xfa\x42\x05\x92\x01\x02\x10\x32R\nproperties\x12\x1f\n\x0bis_identity\x18\x08 \x01(\x08R\nisIdentity\"\x9e\x03\n\x0cRelationship\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12\x16\n\x06source\x18\x03 \x01(\tR\x06source\x12\x16\n\x06target\x18\x04 \x01(\tR\x06target\x12;\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12`\n\nproperties\x18\x07 \x03(\x0b\x32@.indykite.knowledge.objects.v1beta1.Relationship.PropertiesEntryR\nproperties\x1a^\n\x0fPropertiesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta2.ValueR\x05value:\x02\x38\x01\"d\n\rExternalValue\x12%\n\x02id\x18\x01 \x01(\tB\x13\xfa\x42\x10r\x0e\x10\x16\x18\x80\x02:\x04gid:\xd0\x01\x01H\x00R\x02id\x12 \n\x04name\x18\x02 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\x80\x02H\x00R\x04nameB\n\n\x08resolver\"\x9d\x02\n\x08Property\x12\x36\n\x04type\x18\x01 \x01(\tB\"\xfa\x42\x1fr\x1d(\x80\x02\x32\x18^[a-zA-Z_][a-zA-Z0-9_]+$R\x04type\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta2.ValueR\x05value\x12X\n\x0e\x65xternal_value\x18\x04 \x01(\x0b\x32\x31.indykite.knowledge.objects.v1beta1.ExternalValueR\rexternalValue\x12H\n\x08metadata\x18\x03 \x01(\x0b\x32,.indykite.knowledge.objects.v1beta1.MetadataR\x08metadata\"\xfc\x02\n\x08Metadata\x12\x36\n\x0f\x61ssurance_level\x18\x01 \x01(\x05\x42\r\xfa\x42\n\x1a\x08\x30\x01\x30\x02\x30\x03@\x01R\x0e\x61ssuranceLevel\x12G\n\x11verification_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x10verificationTime\x12 \n\x06source\x18\x03 \x01(\tB\x08\xfa\x42\x05r\x03\x18\x80\x01R\x06source\x12i\n\x0f\x63ustom_metadata\x18\x04 \x03(\x0b\x32@.indykite.knowledge.objects.v1beta1.Metadata.CustomMetadataEntryR\x0e\x63ustomMetadata\x1a\x62\n\x13\x43ustomMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta2.ValueR\x05value:\x02\x38\x01\"\x96\x04\n\x04User\x12?\n\x07user_id\x18\x01 \x01(\tB$\xfa\x42!r\x1f\x10\x16\x18\xfe\x01\x32\x18^[A-Za-z0-9-_:]{22,254}$H\x00R\x06userId\x12Y\n\x08property\x18\x03 \x01(\x0b\x32\x31.indykite.knowledge.objects.v1beta1.User.PropertyB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x08property\x12`\n\x0b\x65xternal_id\x18\x05 \x01(\x0b\x32\x33.indykite.knowledge.objects.v1beta1.User.ExternalIDB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\nexternalId\x12\x35\n\x11third_party_token\x18\x06 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01H\x00R\x0fthirdPartyToken\x1a`\n\nExternalID\x12(\n\x04type\x18\x01 \x01(\tB\x14\xfa\x42\x11r\x0f\x18@2\x0b^[a-zA-Z]*$R\x04type\x12(\n\x0b\x65xternal_id\x18\x02 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01R\nexternalId\x1aj\n\x08Property\x12\x1d\n\x04type\x18\x01 \x01(\tB\t\xfa\x42\x06r\x04\x10\x02\x18\x14R\x04type\x12?\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x05valueB\x0b\n\x04user\x12\x03\xf8\x42\x01\x42\xdd\x01\n&com.indykite.knowledge.objects.v1beta1B\x08IkgProtoP\x01\xa2\x02\x03IKO\xaa\x02\"Indykite.Knowledge.Objects.V1beta1\xca\x02\"Indykite\\Knowledge\\Objects\\V1beta1\xe2\x02.Indykite\\Knowledge\\Objects\\V1beta1\\GPBMetadata\xea\x02%Indykite::Knowledge::Objects::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.knowledge.objects.v1beta1.ikg_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n&com.indykite.knowledge.objects.v1beta1B\010IkgProtoP\001\242\002\003IKO\252\002\"Indykite.Knowledge.Objects.V1beta1\312\002\"Indykite\\Knowledge\\Objects\\V1beta1\342\002.Indykite\\Knowledge\\Objects\\V1beta1\\GPBMetadata\352\002%Indykite::Knowledge::Objects::V1beta1'
  _globals['_NODE'].fields_by_name['id']._loaded_options = None
  _globals['_NODE'].fields_by_name['id']._serialized_options = b'\372B\020r\016\020\026\030\200\002:\004gid:\320\001\001'
  _globals['_NODE'].fields_by_name['external_id']._loaded_options = None
  _globals['_NODE'].fields_by_name['external_id']._serialized_options = b'\372B\007r\005\020\001\030\200\002'
  _globals['_NODE'].fields_by_name['type']._loaded_options = None
  _globals['_NODE'].fields_by_name['type']._serialized_options = b'\372B\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_NODE'].fields_by_name['tags']._loaded_options = None
  _globals['_NODE'].fields_by_name['tags']._serialized_options = b'\372B\037\222\001\034\020\n\030\001\"\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_NODE'].fields_by_name['properties']._loaded_options = None
  _globals['_NODE'].fields_by_name['properties']._serialized_options = b'\372B\005\222\001\002\0202'
  _globals['_RELATIONSHIP_PROPERTIESENTRY']._loaded_options = None
  _globals['_RELATIONSHIP_PROPERTIESENTRY']._serialized_options = b'8\001'
  _globals['_EXTERNALVALUE'].fields_by_name['id']._loaded_options = None
  _globals['_EXTERNALVALUE'].fields_by_name['id']._serialized_options = b'\372B\020r\016\020\026\030\200\002:\004gid:\320\001\001'
  _globals['_EXTERNALVALUE'].fields_by_name['name']._loaded_options = None
  _globals['_EXTERNALVALUE'].fields_by_name['name']._serialized_options = b'\372B\007r\005\020\001\030\200\002'
  _globals['_PROPERTY'].fields_by_name['type']._loaded_options = None
  _globals['_PROPERTY'].fields_by_name['type']._serialized_options = b'\372B\037r\035(\200\0022\030^[a-zA-Z_][a-zA-Z0-9_]+$'
  _globals['_METADATA_CUSTOMMETADATAENTRY']._loaded_options = None
  _globals['_METADATA_CUSTOMMETADATAENTRY']._serialized_options = b'8\001'
  _globals['_METADATA'].fields_by_name['assurance_level']._loaded_options = None
  _globals['_METADATA'].fields_by_name['assurance_level']._serialized_options = b'\372B\n\032\0100\0010\0020\003@\001'
  _globals['_METADATA'].fields_by_name['source']._loaded_options = None
  _globals['_METADATA'].fields_by_name['source']._serialized_options = b'\372B\005r\003\030\200\001'
  _globals['_USER_EXTERNALID'].fields_by_name['type']._loaded_options = None
  _globals['_USER_EXTERNALID'].fields_by_name['type']._serialized_options = b'\372B\021r\017\030@2\013^[a-zA-Z]*$'
  _globals['_USER_EXTERNALID'].fields_by_name['external_id']._loaded_options = None
  _globals['_USER_EXTERNALID'].fields_by_name['external_id']._serialized_options = b'\372B\004r\002\020\001'
  _globals['_USER_PROPERTY'].fields_by_name['type']._loaded_options = None
  _globals['_USER_PROPERTY'].fields_by_name['type']._serialized_options = b'\372B\006r\004\020\002\030\024'
  _globals['_USER_PROPERTY'].fields_by_name['value']._loaded_options = None
  _globals['_USER_PROPERTY'].fields_by_name['value']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_USER'].oneofs_by_name['user']._loaded_options = None
  _globals['_USER'].oneofs_by_name['user']._serialized_options = b'\370B\001'
  _globals['_USER'].fields_by_name['user_id']._loaded_options = None
  _globals['_USER'].fields_by_name['user_id']._serialized_options = b'\372B!r\037\020\026\030\376\0012\030^[A-Za-z0-9-_:]{22,254}$'
  _globals['_USER'].fields_by_name['property']._loaded_options = None
  _globals['_USER'].fields_by_name['property']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_USER'].fields_by_name['external_id']._loaded_options = None
  _globals['_USER'].fields_by_name['external_id']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_USER'].fields_by_name['third_party_token']._loaded_options = None
  _globals['_USER'].fields_by_name['third_party_token']._serialized_options = b'\372B\004r\002\020\001'
  _globals['_NODE']._serialized_start=220
  _globals['_NODE']._serialized_end=654
  _globals['_RELATIONSHIP']._serialized_start=657
  _globals['_RELATIONSHIP']._serialized_end=1071
  _globals['_RELATIONSHIP_PROPERTIESENTRY']._serialized_start=977
  _globals['_RELATIONSHIP_PROPERTIESENTRY']._serialized_end=1071
  _globals['_EXTERNALVALUE']._serialized_start=1073
  _globals['_EXTERNALVALUE']._serialized_end=1173
  _globals['_PROPERTY']._serialized_start=1176
  _globals['_PROPERTY']._serialized_end=1461
  _globals['_METADATA']._serialized_start=1464
  _globals['_METADATA']._serialized_end=1844
  _globals['_METADATA_CUSTOMMETADATAENTRY']._serialized_start=1746
  _globals['_METADATA_CUSTOMMETADATAENTRY']._serialized_end=1844
  _globals['_USER']._serialized_start=1847
  _globals['_USER']._serialized_end=2381
  _globals['_USER_EXTERNALID']._serialized_start=2164
  _globals['_USER_EXTERNALID']._serialized_end=2260
  _globals['_USER_PROPERTY']._serialized_start=2262
  _globals['_USER_PROPERTY']._serialized_end=2368
# @@protoc_insertion_point(module_scope)
