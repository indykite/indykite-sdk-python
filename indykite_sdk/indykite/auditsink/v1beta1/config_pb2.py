# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/auditsink/v1beta1/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'indykite/auditsink/v1beta1/config.proto\x12\x1aindykite.auditsink.v1beta1\"\xca\x02\n\nReadConfig\x12\x10\n\x02id\x18\x01 \x01(\tH\x00R\x02id\x12K\n\x04name\x18\x02 \x01(\x0b\x32\x35.indykite.auditsink.v1beta1.ReadConfig.NameIdentifierH\x00R\x04name\x12:\n\x04type\x18\x03 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\x1a\x92\x01\n\x0eNameIdentifier\x12\x1f\n\x0blocation_id\x18\x01 \x01(\tR\nlocationId\x12K\n\rlocation_type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x0clocationType\x12\x12\n\x04name\x18\x03 \x01(\tR\x04nameB\x0c\n\nidentifier\"[\n\rDeletedConfig\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12:\n\x04type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\"\x86\x02\n\x19\x43reateAuthorizationPolicy\x12\x16\n\x06policy\x18\x01 \x01(\tR\x06policy\x12T\n\x06status\x18\x02 \x01(\x0e\x32<.indykite.auditsink.v1beta1.CreateAuthorizationPolicy.StatusR\x06status\x12\x12\n\x04tags\x18\x03 \x03(\tR\x04tags\x12!\n\x0c\x64isplay_name\x18\x04 \x01(\tR\x0b\x64isplayName\"D\n\x06Status\x12\x12\n\x0eSTATUS_INVALID\x10\x00\x12\x11\n\rSTATUS_ACTIVE\x10\x01\x12\x13\n\x0fSTATUS_INACTIVE\x10\x02*\xfc\x05\n\nConfigType\x12\x17\n\x13\x43ONFIG_TYPE_INVALID\x10\x00\x12\x18\n\x14\x43ONFIG_TYPE_CUSTOMER\x10\x01\x12\x19\n\x15\x43ONFIG_TYPE_APP_SPACE\x10\x02\x12\x16\n\x12\x43ONFIG_TYPE_ISSUER\x10\x0f\x12\x16\n\x12\x43ONFIG_TYPE_TENANT\x10\x03\x12\x1b\n\x17\x43ONFIG_TYPE_APPLICATION\x10\x04\x12\x19\n\x15\x43ONFIG_TYPE_APP_AGENT\x10\x05\x12$\n CONFIG_TYPE_APP_AGENT_CREDENTIAL\x10\x06\x12\x1f\n\x1b\x43ONFIG_TYPE_SERVICE_ACCOUNT\x10\x12\x12\"\n\x1e\x43ONFIG_TYPE_SERVICE_CREDENTIAL\x10\x13\x12\x19\n\x15\x43ONFIG_TYPE_AUTH_FLOW\x10\x07\x12\x1d\n\x19\x43ONFIG_TYPE_EMAIL_SERVICE\x10\x08\x12\x1b\n\x17\x43ONFIG_TYPE_SMS_SERVICE\x10\t\x12\x1a\n\x16\x43ONFIG_TYPE_AUDIT_SINK\x10\x1b\x12\x1d\n\x19\x43ONFIG_TYPE_OAUTH2_CLIENT\x10\n\x12\"\n\x1e\x43ONFIG_TYPE_OAUTH2_APPLICATION\x10\x0b\x12\x1f\n\x1b\x43ONFIG_TYPE_OAUTH2_PROVIDER\x10\x11\x12!\n\x1d\x43ONFIG_TYPE_PASSWORD_PROVIDER\x10\x0c\x12!\n\x1d\x43ONFIG_TYPE_WEBAUTHN_PROVIDER\x10\r\x12\"\n\x1e\x43ONFIG_TYPE_AUTHENTEQ_PROVIDER\x10\x0e\x12\x1d\n\x19\x43ONFIG_TYPE_SAFR_PROVIDER\x10\x10\x12\x1f\n\x1b\x43ONFIG_TYPE_READID_PROVIDER\x10\x18\x12$\n CONFIG_TYPE_AUTHORIZATION_POLICY\x10\x16\x12&\n\"CONFIG_TYPE_KNOWLEDGE_GRAPH_SCHEMA\x10\x17\x42\xb7\x01\n\x1e\x63om.indykite.auditsink.v1beta1B\x0b\x43onfigProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1aIndykite.Auditsink.V1beta1\xca\x02\x1aIndykite\\Auditsink\\V1beta1\xe2\x02&Indykite\\Auditsink\\V1beta1\\GPBMetadata\xea\x02\x1cIndykite::Auditsink::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.auditsink.v1beta1.config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.indykite.auditsink.v1beta1B\013ConfigProtoP\001\242\002\003IAX\252\002\032Indykite.Auditsink.V1beta1\312\002\032Indykite\\Auditsink\\V1beta1\342\002&Indykite\\Auditsink\\V1beta1\\GPBMetadata\352\002\034Indykite::Auditsink::V1beta1'
  _globals['_CONFIGTYPE']._serialized_start=763
  _globals['_CONFIGTYPE']._serialized_end=1527
  _globals['_READCONFIG']._serialized_start=72
  _globals['_READCONFIG']._serialized_end=402
  _globals['_READCONFIG_NAMEIDENTIFIER']._serialized_start=242
  _globals['_READCONFIG_NAMEIDENTIFIER']._serialized_end=388
  _globals['_DELETEDCONFIG']._serialized_start=404
  _globals['_DELETEDCONFIG']._serialized_end=495
  _globals['_CREATEAUTHORIZATIONPOLICY']._serialized_start=498
  _globals['_CREATEAUTHORIZATIONPOLICY']._serialized_end=760
  _globals['_CREATEAUTHORIZATIONPOLICY_STATUS']._serialized_start=692
  _globals['_CREATEAUTHORIZATIONPOLICY_STATUS']._serialized_end=760
# @@protoc_insertion_point(module_scope)