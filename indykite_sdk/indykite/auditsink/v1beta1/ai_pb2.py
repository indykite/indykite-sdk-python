# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/auditsink/v1beta1/ai.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from indykite_sdk.indykite.auditsink.v1beta1 import authorization_pb2 as indykite_dot_auditsink_dot_v1beta1_dot_authorization__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#indykite/auditsink/v1beta1/ai.proto\x12\x1aindykite.auditsink.v1beta1\x1a\x1egoogle/protobuf/duration.proto\x1a.indykite/auditsink/v1beta1/authorization.proto\"\xb8\x05\n\rIsChangePoint\x12h\n\x15resolved_digital_twin\x18\x01 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12K\n\x07request\x18\x02 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.IsChangePoint.RequestR\x07request\x12r\n\x15\x63hange_point_detected\x18\x03 \x01(\x0b\x32>.indykite.auditsink.v1beta1.IsChangePoint.ChangePointDetectionR\x13\x63hangePointDetected\x12N\n\x08response\x18\x04 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.IsChangePoint.ResponseR\x08response\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a=\n\x07Request\x12\x1a\n\x08resource\x18\x01 \x01(\tR\x08resource\x12\x16\n\x06\x61\x63tion\x18\x02 \x01(\tR\x06\x61\x63tion\x1ax\n\x14\x43hangePointDetection\x12\x1b\n\tis_change\x18\x01 \x01(\x08R\x08isChange\x12 \n\x0b\x65xplanation\x18\x02 \x01(\tR\x0b\x65xplanation\x12!\n\x0c\x63hange_score\x18\x03 \x01(\x01R\x0b\x63hangeScore\x1a/\n\x08Response\x12#\n\rdecision_time\x18\x01 \x01(\tR\x0c\x64\x65\x63isionTimeB\xb3\x01\n\x1e\x63om.indykite.auditsink.v1beta1B\x07\x41iProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1aIndykite.Auditsink.V1beta1\xca\x02\x1aIndykite\\Auditsink\\V1beta1\xe2\x02&Indykite\\Auditsink\\V1beta1\\GPBMetadata\xea\x02\x1cIndykite::Auditsink::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.auditsink.v1beta1.ai_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.indykite.auditsink.v1beta1B\007AiProtoP\001\242\002\003IAX\252\002\032Indykite.Auditsink.V1beta1\312\002\032Indykite\\Auditsink\\V1beta1\342\002&Indykite\\Auditsink\\V1beta1\\GPBMetadata\352\002\034Indykite::Auditsink::V1beta1'
  _globals['_ISCHANGEPOINT']._serialized_start=148
  _globals['_ISCHANGEPOINT']._serialized_end=844
  _globals['_ISCHANGEPOINT_REQUEST']._serialized_start=612
  _globals['_ISCHANGEPOINT_REQUEST']._serialized_end=673
  _globals['_ISCHANGEPOINT_CHANGEPOINTDETECTION']._serialized_start=675
  _globals['_ISCHANGEPOINT_CHANGEPOINTDETECTION']._serialized_end=795
  _globals['_ISCHANGEPOINT_RESPONSE']._serialized_start=797
  _globals['_ISCHANGEPOINT_RESPONSE']._serialized_end=844
# @@protoc_insertion_point(module_scope)
