# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/tda/v1beta1/model.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2 as indykite_dot_knowledge_dot_objects_dot_v1beta1_dot_ikg__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n indykite/tda/v1beta1/model.proto\x12\x14indykite.tda.v1beta1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a,indykite/knowledge/objects/v1beta1/ikg.proto\x1a\x17validate/validate.proto\"9\n\x07\x43onsent\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1e\n\nproperties\x18\x02 \x03(\tR\nproperties\"\xfa\x03\n\x0fTrustedDataNode\x12#\n\x02id\x18\x01 \x01(\tB\x13\xfa\x42\x10r\x0e\x10\x16\x18\x80\x02:\x04gid:\xd0\x01\x01R\x02id\x12+\n\x0b\x65xternal_id\x18\x02 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\x80\x02R\nexternalId\x12-\n\x04type\x18\x03 \x01(\tB\x19\xfa\x42\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04type\x12\x36\n\x04tags\x18\x04 \x03(\tB\"\xfa\x42\x1f\x92\x01\x1c\x10 \x18\x01\"\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04tags\x12;\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12V\n\nproperties\x18\x07 \x03(\x0b\x32,.indykite.knowledge.objects.v1beta1.PropertyB\x08\xfa\x42\x05\x92\x01\x02\x10\x32R\nproperties\x12\x1f\n\x0bis_identity\x18\x08 \x01(\x08R\nisIdentity\x12;\n\x05nodes\x18\t \x03(\x0b\x32%.indykite.tda.v1beta1.TrustedDataNodeR\x05nodesB\x98\x01\n\x18\x63om.indykite.tda.v1beta1B\nModelProtoP\x01\xa2\x02\x03ITX\xaa\x02\x14Indykite.Tda.V1beta1\xca\x02\x14Indykite\\Tda\\V1beta1\xe2\x02 Indykite\\Tda\\V1beta1\\GPBMetadata\xea\x02\x16Indykite::Tda::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.tda.v1beta1.model_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\030com.indykite.tda.v1beta1B\nModelProtoP\001\242\002\003ITX\252\002\024Indykite.Tda.V1beta1\312\002\024Indykite\\Tda\\V1beta1\342\002 Indykite\\Tda\\V1beta1\\GPBMetadata\352\002\026Indykite::Tda::V1beta1'
  _globals['_TRUSTEDDATANODE'].fields_by_name['id']._loaded_options = None
  _globals['_TRUSTEDDATANODE'].fields_by_name['id']._serialized_options = b'\372B\020r\016\020\026\030\200\002:\004gid:\320\001\001'
  _globals['_TRUSTEDDATANODE'].fields_by_name['external_id']._loaded_options = None
  _globals['_TRUSTEDDATANODE'].fields_by_name['external_id']._serialized_options = b'\372B\007r\005\020\001\030\200\002'
  _globals['_TRUSTEDDATANODE'].fields_by_name['type']._loaded_options = None
  _globals['_TRUSTEDDATANODE'].fields_by_name['type']._serialized_options = b'\372B\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_TRUSTEDDATANODE'].fields_by_name['tags']._loaded_options = None
  _globals['_TRUSTEDDATANODE'].fields_by_name['tags']._serialized_options = b'\372B\037\222\001\034\020 \030\001\"\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_TRUSTEDDATANODE'].fields_by_name['properties']._loaded_options = None
  _globals['_TRUSTEDDATANODE'].fields_by_name['properties']._serialized_options = b'\372B\005\222\001\002\0202'
  _globals['_CONSENT']._serialized_start=162
  _globals['_CONSENT']._serialized_end=219
  _globals['_TRUSTEDDATANODE']._serialized_start=222
  _globals['_TRUSTEDDATANODE']._serialized_end=728
# @@protoc_insertion_point(module_scope)
