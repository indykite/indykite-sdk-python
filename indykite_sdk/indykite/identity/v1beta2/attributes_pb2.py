# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/identity/v1beta2/attributes.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*indykite/identity/v1beta2/attributes.proto\x12\x19indykite.identity.v1beta2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%indykite/objects/v1beta1/struct.proto\x1a\x17validate/validate.proto\"\xf4\x01\n\x06Schema\x12H\n\x07\x63ontext\x18\x04 \x03(\x0b\x32..indykite.identity.v1beta2.Schema.ContextEntryR\x07\x63ontext\x12\x16\n\x06schema\x18\x01 \x01(\tR\x06schema\x12%\n\x0eschema_version\x18\x02 \x01(\tR\rschemaVersion\x12%\n\x0e\x61ttribute_name\x18\x03 \x01(\tR\rattributeName\x1a:\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\x9f\x01\n\x12PropertyDefinition\x12%\n\x07\x63ontext\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\x88\x01\x01\xd0\x01\x01R\x07\x63ontext\x12\x39\n\x04type\x18\x02 \x01(\tB%\xfa\x42\"r (\x80\x02\x32\x18^[a-zA-Z_][a-zA-Z0-9_]+$\xd0\x01\x01R\x04type\x12\'\n\x08property\x18\x03 \x01(\tB\x0b\xfa\x42\x08r\x06\x18\x80\x02\xd0\x01\x01R\x08property\"i\n\x12PropertyConstraint\x12\x18\n\x07issuers\x18\x01 \x03(\tR\x07issuers\x12\x16\n\x06subset\x18\x02 \x03(\tR\x06subset\x12!\n\x0conly_primary\x18\x03 \x01(\x08R\x0bonlyPrimary\"\xb6\x01\n\x0cPropertyMask\x12W\n\ndefinition\x18\x01 \x01(\x0b\x32-.indykite.identity.v1beta2.PropertyDefinitionB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\ndefinition\x12M\n\nconstraint\x18\x02 \x01(\x0b\x32-.indykite.identity.v1beta2.PropertyConstraintR\nconstraint\"\xb8\x01\n\x0ePropertyFilter\x12\x1d\n\x04type\x18\x01 \x01(\tB\t\xfa\x42\x06r\x04\x10\x02\x18\x14R\x04type\x12?\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x05value\x12\x46\n\ttenant_id\x18\x03 \x01(\tB)\xfa\x42&r$\x10\x1b\x18\x64\x32\x1b^gid:[A-Za-z0-9-_]{27,100}$\xd0\x01\x01R\x08tenantId\"\xfd\x01\n\x10PropertyMetadata\x12\x18\n\x07primary\x18\x01 \x01(\x08R\x07primary\x12R\n\x0f\x61ssurance_level\x18\x02 \x01(\x0e\x32).indykite.identity.v1beta2.AssuranceLevelR\x0e\x61ssuranceLevel\x12\x16\n\x06issuer\x18\x03 \x01(\tR\x06issuer\x12G\n\x11verification_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x10verificationTime\x12\x1a\n\x08verifier\x18\x05 \x01(\tR\x08verifier\"\xc0\x02\n\x08Property\x12*\n\x02id\x18\x01 \x01(\tB\x1a\xfa\x42\x17r\x15\x32\x10^[0-9a-f]{1,16}$\xd0\x01\x01R\x02id\x12M\n\ndefinition\x18\x02 \x01(\x0b\x32-.indykite.identity.v1beta2.PropertyDefinitionR\ndefinition\x12?\n\x04meta\x18\x03 \x01(\x0b\x32+.indykite.identity.v1beta2.PropertyMetadataR\x04meta\x12\x44\n\x0cobject_value\x18\x04 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueH\x00R\x0bobjectValue\x12)\n\x0freference_value\x18\x05 \x01(\tH\x00R\x0ereferenceValueB\x07\n\x05value\"\x81\x02\n\x16PropertyBatchOperation\x12\x41\n\x03\x61\x64\x64\x18\x01 \x01(\x0b\x32#.indykite.identity.v1beta2.PropertyB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x03\x61\x64\x64\x12I\n\x07replace\x18\x02 \x01(\x0b\x32#.indykite.identity.v1beta2.PropertyB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x07replace\x12G\n\x06remove\x18\x03 \x01(\x0b\x32#.indykite.identity.v1beta2.PropertyB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x06removeB\x10\n\toperation\x12\x03\xf8\x42\x01\"\xdd\x01\n\x14\x42\x61tchOperationResult\x12\x14\n\x05index\x18\x04 \x01(\x04R\x05index\x12R\n\x07success\x18\x05 \x01(\x0b\x32\x36.indykite.identity.v1beta2.BatchOperationResultSuccessH\x00R\x07success\x12L\n\x05\x65rror\x18\x06 \x01(\x0b\x32\x34.indykite.identity.v1beta2.BatchOperationResultErrorH\x00R\x05\x65rrorB\r\n\x06result\x12\x03\xf8\x42\x01\"W\n\x1b\x42\x61tchOperationResultSuccess\x12\x38\n\x0bproperty_id\x18\x01 \x01(\tB\x17\xfa\x42\x14r\x12\x32\x10^[0-9a-f]{1,16}$R\npropertyId\"5\n\x19\x42\x61tchOperationResultError\x12\x18\n\x07message\x18\x01 \x03(\tR\x07message*\x81\x01\n\x0e\x41ssuranceLevel\x12\x1b\n\x17\x41SSURANCE_LEVEL_INVALID\x10\x00\x12\x17\n\x13\x41SSURANCE_LEVEL_LOW\x10\x01\x12\x1f\n\x1b\x41SSURANCE_LEVEL_SUBSTANTIAL\x10\x02\x12\x18\n\x14\x41SSURANCE_LEVEL_HIGH\x10\x03\x42\xb6\x01\n\x1d\x63om.indykite.identity.v1beta2B\x0f\x41ttributesProtoP\x01\xa2\x02\x03IIX\xaa\x02\x19Indykite.Identity.V1beta2\xca\x02\x19Indykite\\Identity\\V1beta2\xe2\x02%Indykite\\Identity\\V1beta2\\GPBMetadata\xea\x02\x1bIndykite::Identity::V1beta2b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.identity.v1beta2.attributes_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.indykite.identity.v1beta2B\017AttributesProtoP\001\242\002\003IIX\252\002\031Indykite.Identity.V1beta2\312\002\031Indykite\\Identity\\V1beta2\342\002%Indykite\\Identity\\V1beta2\\GPBMetadata\352\002\033Indykite::Identity::V1beta2'
  _SCHEMA_CONTEXTENTRY._options = None
  _SCHEMA_CONTEXTENTRY._serialized_options = b'8\001'
  _PROPERTYDEFINITION.fields_by_name['context']._options = None
  _PROPERTYDEFINITION.fields_by_name['context']._serialized_options = b'\372B\010r\006\210\001\001\320\001\001'
  _PROPERTYDEFINITION.fields_by_name['type']._options = None
  _PROPERTYDEFINITION.fields_by_name['type']._serialized_options = b'\372B\"r (\200\0022\030^[a-zA-Z_][a-zA-Z0-9_]+$\320\001\001'
  _PROPERTYDEFINITION.fields_by_name['property']._options = None
  _PROPERTYDEFINITION.fields_by_name['property']._serialized_options = b'\372B\010r\006\030\200\002\320\001\001'
  _PROPERTYMASK.fields_by_name['definition']._options = None
  _PROPERTYMASK.fields_by_name['definition']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PROPERTYFILTER.fields_by_name['type']._options = None
  _PROPERTYFILTER.fields_by_name['type']._serialized_options = b'\372B\006r\004\020\002\030\024'
  _PROPERTYFILTER.fields_by_name['value']._options = None
  _PROPERTYFILTER.fields_by_name['value']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PROPERTYFILTER.fields_by_name['tenant_id']._options = None
  _PROPERTYFILTER.fields_by_name['tenant_id']._serialized_options = b'\372B&r$\020\033\030d2\033^gid:[A-Za-z0-9-_]{27,100}$\320\001\001'
  _PROPERTY.fields_by_name['id']._options = None
  _PROPERTY.fields_by_name['id']._serialized_options = b'\372B\027r\0252\020^[0-9a-f]{1,16}$\320\001\001'
  _PROPERTYBATCHOPERATION.oneofs_by_name['operation']._options = None
  _PROPERTYBATCHOPERATION.oneofs_by_name['operation']._serialized_options = b'\370B\001'
  _PROPERTYBATCHOPERATION.fields_by_name['add']._options = None
  _PROPERTYBATCHOPERATION.fields_by_name['add']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PROPERTYBATCHOPERATION.fields_by_name['replace']._options = None
  _PROPERTYBATCHOPERATION.fields_by_name['replace']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PROPERTYBATCHOPERATION.fields_by_name['remove']._options = None
  _PROPERTYBATCHOPERATION.fields_by_name['remove']._serialized_options = b'\372B\005\212\001\002\020\001'
  _BATCHOPERATIONRESULT.oneofs_by_name['result']._options = None
  _BATCHOPERATIONRESULT.oneofs_by_name['result']._serialized_options = b'\370B\001'
  _BATCHOPERATIONRESULTSUCCESS.fields_by_name['property_id']._options = None
  _BATCHOPERATIONRESULTSUCCESS.fields_by_name['property_id']._serialized_options = b'\372B\024r\0222\020^[0-9a-f]{1,16}$'
  _globals['_ASSURANCELEVEL']._serialized_start=2266
  _globals['_ASSURANCELEVEL']._serialized_end=2395
  _globals['_SCHEMA']._serialized_start=171
  _globals['_SCHEMA']._serialized_end=415
  _globals['_SCHEMA_CONTEXTENTRY']._serialized_start=357
  _globals['_SCHEMA_CONTEXTENTRY']._serialized_end=415
  _globals['_PROPERTYDEFINITION']._serialized_start=418
  _globals['_PROPERTYDEFINITION']._serialized_end=577
  _globals['_PROPERTYCONSTRAINT']._serialized_start=579
  _globals['_PROPERTYCONSTRAINT']._serialized_end=684
  _globals['_PROPERTYMASK']._serialized_start=687
  _globals['_PROPERTYMASK']._serialized_end=869
  _globals['_PROPERTYFILTER']._serialized_start=872
  _globals['_PROPERTYFILTER']._serialized_end=1056
  _globals['_PROPERTYMETADATA']._serialized_start=1059
  _globals['_PROPERTYMETADATA']._serialized_end=1312
  _globals['_PROPERTY']._serialized_start=1315
  _globals['_PROPERTY']._serialized_end=1635
  _globals['_PROPERTYBATCHOPERATION']._serialized_start=1638
  _globals['_PROPERTYBATCHOPERATION']._serialized_end=1895
  _globals['_BATCHOPERATIONRESULT']._serialized_start=1898
  _globals['_BATCHOPERATIONRESULT']._serialized_end=2119
  _globals['_BATCHOPERATIONRESULTSUCCESS']._serialized_start=2121
  _globals['_BATCHOPERATIONRESULTSUCCESS']._serialized_end=2208
  _globals['_BATCHOPERATIONRESULTERROR']._serialized_start=2210
  _globals['_BATCHOPERATIONRESULTERROR']._serialized_end=2263
# @@protoc_insertion_point(module_scope)
