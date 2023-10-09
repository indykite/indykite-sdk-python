# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/auditsink/v1beta1/authorization.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.indykite/auditsink/v1beta1/authorization.proto\x12\x1aindykite.auditsink.v1beta1\x1a%indykite/objects/v1beta1/struct.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe9\x02\n\x14\x41uthorizationSubject\x12Y\n\x0c\x64igital_twin\x18\x01 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinH\x00R\x0b\x64igitalTwin\x12o\n\x15\x64igital_twin_property\x18\x02 \x01(\x0b\x32\x39.indykite.auditsink.v1beta1.AuthorizationSubject.PropertyH\x00R\x13\x64igitalTwinProperty\x12#\n\x0c\x61\x63\x63\x65ss_token\x18\x03 \x01(\tH\x00R\x0b\x61\x63\x63\x65ssToken\x1aU\n\x08Property\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05valueB\t\n\x07subject\"*\n\x18\x41uthorizationDigitalTwin\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"9\n\x13\x41uthorizationPolicy\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"3\n\x17\x41uthorizationDenyReason\x12\x18\n\x07message\x18\x01 \x01(\tR\x07message\"\x92\x0e\n\x0cIsAuthorized\x12J\n\x07request\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.IsAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12M\n\x08response\x18\x03 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.IsAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a\xe0\x03\n\x07Request\x12J\n\x07subject\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.AuthorizationSubjectR\x07subject\x12W\n\tresources\x18\x02 \x03(\x0b\x32\x39.indykite.auditsink.v1beta1.IsAuthorized.Request.ResourceR\tresources\x12\x64\n\x0cinput_params\x18\x03 \x03(\x0b\x32\x41.indykite.auditsink.v1beta1.IsAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x04 \x03(\tR\npolicyTags\x1aH\n\x08Resource\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x03 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\xa7\x06\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12^\n\tdecisions\x18\x02 \x03(\x0b\x32@.indykite.auditsink.v1beta1.IsAuthorized.Response.DecisionsEntryR\tdecisions\x1a\x1e\n\x06\x41\x63tion\x12\x14\n\x05\x61llow\x18\x01 \x01(\x08R\x05\x61llow\x1a\xe3\x01\n\x08Resource\x12\x61\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32G.indykite.auditsink.v1beta1.IsAuthorized.Response.Resource.ActionsEntryR\x07\x61\x63tions\x1at\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12N\n\x05value\x18\x02 \x01(\x0b\x32\x38.indykite.auditsink.v1beta1.IsAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a\xf5\x01\n\x0cResourceType\x12k\n\tresources\x18\x01 \x03(\x0b\x32M.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceType.ResourcesEntryR\tresources\x1ax\n\x0eResourcesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x05value\x18\x02 \x01(\x0b\x32:.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceR\x05value:\x02\x38\x01\x1a|\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12T\n\x05value\x18\x02 \x01(\x0b\x32>.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\"\xa8\r\n\x0eWhatAuthorized\x12L\n\x07request\x18\x01 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.WhatAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12O\n\x08response\x18\x03 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.WhatAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a\xe5\x03\n\x07Request\x12J\n\x07subject\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.AuthorizationSubjectR\x07subject\x12\x66\n\x0eresource_types\x18\x02 \x03(\x0b\x32?.indykite.auditsink.v1beta1.WhatAuthorized.Request.ResourceTypeR\rresourceTypes\x12\x66\n\x0cinput_params\x18\x03 \x03(\x0b\x32\x43.indykite.auditsink.v1beta1.WhatAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x04 \x03(\tR\npolicyTags\x1a<\n\x0cResourceType\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x02 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\xb2\x05\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12`\n\tdecisions\x18\x02 \x03(\x0b\x32\x42.indykite.auditsink.v1beta1.WhatAuthorized.Response.DecisionsEntryR\tdecisions\x1a+\n\x08Resource\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x1a\x64\n\x06\x41\x63tion\x12Z\n\tresources\x18\x01 \x03(\x0b\x32<.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceR\tresources\x1a\xef\x01\n\x0cResourceType\x12g\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32M.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceType.ActionsEntryR\x07\x61\x63tions\x1av\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x05value\x18\x02 \x01(\x0b\x32:.indykite.auditsink.v1beta1.WhatAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a~\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12V\n\x05value\x18\x02 \x01(\x0b\x32@.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\"\xbf\x0e\n\rWhoAuthorized\x12K\n\x07request\x18\x01 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.WhoAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12N\n\x08response\x18\x03 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.WhoAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a\x96\x03\n\x07Request\x12X\n\tresources\x18\x01 \x03(\x0b\x32:.indykite.auditsink.v1beta1.WhoAuthorized.Request.ResourceR\tresources\x12\x65\n\x0cinput_params\x18\x02 \x03(\x0b\x32\x42.indykite.auditsink.v1beta1.WhoAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x03 \x03(\tR\npolicyTags\x1aH\n\x08Resource\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x03 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\x9b\x07\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12_\n\tdecisions\x18\x02 \x03(\x0b\x32\x41.indykite.auditsink.v1beta1.WhoAuthorized.Response.DecisionsEntryR\tdecisions\x1a*\n\x07Subject\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x1a`\n\x06\x41\x63tion\x12V\n\x08subjects\x18\x01 \x03(\x0b\x32:.indykite.auditsink.v1beta1.WhoAuthorized.Response.SubjectR\x08subjects\x1a\xe5\x01\n\x08Resource\x12\x62\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32H.indykite.auditsink.v1beta1.WhoAuthorized.Response.Resource.ActionsEntryR\x07\x61\x63tions\x1au\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12O\n\x05value\x18\x02 \x01(\x0b\x32\x39.indykite.auditsink.v1beta1.WhoAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a\xf7\x01\n\x0cResourceType\x12l\n\tresources\x18\x01 \x03(\x0b\x32N.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceType.ResourcesEntryR\tresources\x1ay\n\x0eResourcesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12Q\n\x05value\x18\x02 \x01(\x0b\x32;.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceR\x05value:\x02\x38\x01\x1a}\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12U\n\x05value\x18\x02 \x01(\x0b\x32?.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\x42\xbe\x01\n\x1e\x63om.indykite.auditsink.v1beta1B\x12\x41uthorizationProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1aIndykite.Auditsink.V1beta1\xca\x02\x1aIndykite\\Auditsink\\V1beta1\xe2\x02&Indykite\\Auditsink\\V1beta1\\GPBMetadata\xea\x02\x1cIndykite::Auditsink::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.auditsink.v1beta1.authorization_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.indykite.auditsink.v1beta1B\022AuthorizationProtoP\001\242\002\003IAX\252\002\032Indykite.Auditsink.V1beta1\312\002\032Indykite\\Auditsink\\V1beta1\342\002&Indykite\\Auditsink\\V1beta1\\GPBMetadata\352\002\034Indykite::Auditsink::V1beta1'
  _ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY._options = None
  _ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY._serialized_options = b'8\001'
  _ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY._options = None
  _ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY._serialized_options = b'8\001'
  _ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY._options = None
  _ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY._serialized_options = b'8\001'
  _ISAUTHORIZED_RESPONSE_DECISIONSENTRY._options = None
  _ISAUTHORIZED_RESPONSE_DECISIONSENTRY._serialized_options = b'8\001'
  _WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY._options = None
  _WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY._serialized_options = b'8\001'
  _WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY._options = None
  _WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY._serialized_options = b'8\001'
  _WHATAUTHORIZED_RESPONSE_DECISIONSENTRY._options = None
  _WHATAUTHORIZED_RESPONSE_DECISIONSENTRY._serialized_options = b'8\001'
  _WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY._options = None
  _WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY._serialized_options = b'8\001'
  _WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY._options = None
  _WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY._serialized_options = b'8\001'
  _WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY._options = None
  _WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY._serialized_options = b'8\001'
  _WHOAUTHORIZED_RESPONSE_DECISIONSENTRY._options = None
  _WHOAUTHORIZED_RESPONSE_DECISIONSENTRY._serialized_options = b'8\001'
  _globals['_AUTHORIZATIONSUBJECT']._serialized_start=183
  _globals['_AUTHORIZATIONSUBJECT']._serialized_end=544
  _globals['_AUTHORIZATIONSUBJECT_PROPERTY']._serialized_start=448
  _globals['_AUTHORIZATIONSUBJECT_PROPERTY']._serialized_end=533
  _globals['_AUTHORIZATIONDIGITALTWIN']._serialized_start=546
  _globals['_AUTHORIZATIONDIGITALTWIN']._serialized_end=588
  _globals['_AUTHORIZATIONPOLICY']._serialized_start=590
  _globals['_AUTHORIZATIONPOLICY']._serialized_end=647
  _globals['_AUTHORIZATIONDENYREASON']._serialized_start=649
  _globals['_AUTHORIZATIONDENYREASON']._serialized_end=700
  _globals['_ISAUTHORIZED']._serialized_start=703
  _globals['_ISAUTHORIZED']._serialized_end=2513
  _globals['_ISAUTHORIZED_REQUEST']._serialized_start=1223
  _globals['_ISAUTHORIZED_REQUEST']._serialized_end=1703
  _globals['_ISAUTHORIZED_REQUEST_RESOURCE']._serialized_start=1534
  _globals['_ISAUTHORIZED_REQUEST_RESOURCE']._serialized_end=1606
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=1608
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=1703
  _globals['_ISAUTHORIZED_RESPONSE']._serialized_start=1706
  _globals['_ISAUTHORIZED_RESPONSE']._serialized_end=2513
  _globals['_ISAUTHORIZED_RESPONSE_ACTION']._serialized_start=1879
  _globals['_ISAUTHORIZED_RESPONSE_ACTION']._serialized_end=1909
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=1912
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=2139
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_start=2023
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_end=2139
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=2142
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=2387
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_start=2267
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_end=2387
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=2389
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=2513
  _globals['_WHATAUTHORIZED']._serialized_start=2516
  _globals['_WHATAUTHORIZED']._serialized_end=4220
  _globals['_WHATAUTHORIZED_REQUEST']._serialized_start=3042
  _globals['_WHATAUTHORIZED_REQUEST']._serialized_end=3527
  _globals['_WHATAUTHORIZED_REQUEST_RESOURCETYPE']._serialized_start=3370
  _globals['_WHATAUTHORIZED_REQUEST_RESOURCETYPE']._serialized_end=3430
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=1608
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=1703
  _globals['_WHATAUTHORIZED_RESPONSE']._serialized_start=3530
  _globals['_WHATAUTHORIZED_RESPONSE']._serialized_end=4220
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=3705
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=3748
  _globals['_WHATAUTHORIZED_RESPONSE_ACTION']._serialized_start=3750
  _globals['_WHATAUTHORIZED_RESPONSE_ACTION']._serialized_end=3850
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=3853
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=4092
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._serialized_start=3974
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._serialized_end=4092
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=4094
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=4220
  _globals['_WHOAUTHORIZED']._serialized_start=4223
  _globals['_WHOAUTHORIZED']._serialized_end=6078
  _globals['_WHOAUTHORIZED_REQUEST']._serialized_start=4746
  _globals['_WHOAUTHORIZED_REQUEST']._serialized_end=5152
  _globals['_WHOAUTHORIZED_REQUEST_RESOURCE']._serialized_start=1534
  _globals['_WHOAUTHORIZED_REQUEST_RESOURCE']._serialized_end=1606
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=1608
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=1703
  _globals['_WHOAUTHORIZED_RESPONSE']._serialized_start=5155
  _globals['_WHOAUTHORIZED_RESPONSE']._serialized_end=6078
  _globals['_WHOAUTHORIZED_RESPONSE_SUBJECT']._serialized_start=5329
  _globals['_WHOAUTHORIZED_RESPONSE_SUBJECT']._serialized_end=5371
  _globals['_WHOAUTHORIZED_RESPONSE_ACTION']._serialized_start=5373
  _globals['_WHOAUTHORIZED_RESPONSE_ACTION']._serialized_end=5469
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=5472
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=5701
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_start=5584
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_end=5701
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=5704
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=5951
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_start=5830
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_end=5951
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=5953
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=6078
# @@protoc_insertion_point(module_scope)
