# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/authorization/v1beta1/model.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as indykite_dot_identity_dot_v1beta2_dot_model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*indykite/authorization/v1beta1/model.proto\x12\x1eindykite.authorization.v1beta1\x1a\x17validate/validate.proto\x1a%indykite/identity/v1beta2/model.proto\"\x8f\x01\n\x07Subject\x12t\n\x17\x64igital_twin_identifier\x18\x01 \x01(\x0b\x32\x30.indykite.identity.v1beta2.DigitalTwinIdentifierB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x15\x64igitalTwinIdentifierB\x0e\n\x07subject\x12\x03\xf8\x42\x01\"\xb3\x01\n\x06Option\x12.\n\x0cstring_value\x18\x01 \x01(\tB\t\xfa\x42\x06r\x04\x10\x01\x18\x32H\x00R\x0bstringValue\x12\x1f\n\nbool_value\x18\x02 \x01(\x08H\x00R\tboolValue\x12%\n\rinteger_value\x18\x03 \x01(\x03H\x00R\x0cintegerValue\x12#\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00R\x0b\x64oubleValueB\x0c\n\x05value\x12\x03\xf8\x42\x01\x42\xca\x01\n\"com.indykite.authorization.v1beta1B\nModelProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1eIndykite.Authorization.V1beta1\xca\x02\x1eIndykite\\Authorization\\V1beta1\xe2\x02*Indykite\\Authorization\\V1beta1\\GPBMetadata\xea\x02 Indykite::Authorization::V1beta1b\x06proto3')



_SUBJECT = DESCRIPTOR.message_types_by_name['Subject']
_OPTION = DESCRIPTOR.message_types_by_name['Option']
Subject = _reflection.GeneratedProtocolMessageType('Subject', (_message.Message,), {
  'DESCRIPTOR' : _SUBJECT,
  '__module__' : 'indykite.authorization.v1beta1.model_pb2'
  # @@protoc_insertion_point(class_scope:indykite.authorization.v1beta1.Subject)
  })
_sym_db.RegisterMessage(Subject)

Option = _reflection.GeneratedProtocolMessageType('Option', (_message.Message,), {
  'DESCRIPTOR' : _OPTION,
  '__module__' : 'indykite.authorization.v1beta1.model_pb2'
  # @@protoc_insertion_point(class_scope:indykite.authorization.v1beta1.Option)
  })
_sym_db.RegisterMessage(Option)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.indykite.authorization.v1beta1B\nModelProtoP\001\242\002\003IAX\252\002\036Indykite.Authorization.V1beta1\312\002\036Indykite\\Authorization\\V1beta1\342\002*Indykite\\Authorization\\V1beta1\\GPBMetadata\352\002 Indykite::Authorization::V1beta1'
  _SUBJECT.oneofs_by_name['subject']._options = None
  _SUBJECT.oneofs_by_name['subject']._serialized_options = b'\370B\001'
  _SUBJECT.fields_by_name['digital_twin_identifier']._options = None
  _SUBJECT.fields_by_name['digital_twin_identifier']._serialized_options = b'\372B\005\212\001\002\020\001'
  _OPTION.oneofs_by_name['value']._options = None
  _OPTION.oneofs_by_name['value']._serialized_options = b'\370B\001'
  _OPTION.fields_by_name['string_value']._options = None
  _OPTION.fields_by_name['string_value']._serialized_options = b'\372B\006r\004\020\001\0302'
  _SUBJECT._serialized_start=143
  _SUBJECT._serialized_end=286
  _OPTION._serialized_start=289
  _OPTION._serialized_end=468
# @@protoc_insertion_point(module_scope)
