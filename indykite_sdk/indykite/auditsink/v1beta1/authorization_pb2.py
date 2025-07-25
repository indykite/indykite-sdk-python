# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/auditsink/v1beta1/authorization.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.indykite/auditsink/v1beta1/authorization.proto\x12\x1aindykite.auditsink.v1beta1\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%indykite/objects/v1beta1/struct.proto\"\x8c\x04\n\x14\x41uthorizationSubject\x12Y\n\x0c\x64igital_twin\x18\x01 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinH\x00R\x0b\x64igitalTwin\x12o\n\x15\x64igital_twin_property\x18\x02 \x01(\x0b\x32\x39.indykite.auditsink.v1beta1.AuthorizationSubject.PropertyH\x00R\x13\x64igitalTwinProperty\x12#\n\x0c\x61\x63\x63\x65ss_token\x18\x03 \x01(\tH\x00R\x0b\x61\x63\x63\x65ssToken\x12^\n\x0b\x65xternal_id\x18\x04 \x01(\x0b\x32;.indykite.auditsink.v1beta1.AuthorizationSubject.ExternalIDH\x00R\nexternalId\x1aU\n\x08Property\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value\x1a\x41\n\nExternalID\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x1f\n\x0b\x65xternal_id\x18\x02 \x01(\tR\nexternalIdB\t\n\x07subject\"*\n\x18\x41uthorizationDigitalTwin\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"9\n\x13\x41uthorizationPolicy\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"3\n\x17\x41uthorizationDenyReason\x12\x18\n\x07message\x18\x01 \x01(\tR\x07message\"\xa8\x01\n\x0e\x41uthZENRequest\x12\x12\n\x04\x62ody\x18\x01 \x01(\tR\x04\x62ody\x12P\n\x05token\x18\x02 \x01(\x0b\x32:.indykite.auditsink.v1beta1.AuthZENRequest.ThirdPartyTokenR\x05token\x1a\x30\n\x0fThirdPartyToken\x12\x1d\n\nsubject_id\x18\x01 \x01(\tR\tsubjectId\"\x8b\x01\n\x06\x41\x64vice\x12\x46\n\x06values\x18\x01 \x03(\x0b\x32..indykite.auditsink.v1beta1.Advice.ValuesEntryR\x06values\x1a\x39\n\x0bValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xd1\x03\n\nEvaluation\x12\x44\n\x07request\x18\x01 \x01(\x0b\x32*.indykite.auditsink.v1beta1.AuthZENRequestR\x07request\x12\x1a\n\x08response\x18\x02 \x01(\tR\x08response\x12G\n\x07results\x18\x03 \x03(\x0b\x32-.indykite.auditsink.v1beta1.Evaluation.ResultR\x07results\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a\xae\x01\n\x06Result\x12G\n\x06policy\x18\x01 \x01(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\x06policy\x12\x1d\n\nis_allowed\x18\x02 \x01(\x08R\tisAllowed\x12<\n\x07\x61\x64vices\x18\x03 \x03(\x0b\x32\".indykite.auditsink.v1beta1.AdviceR\x07\x61\x64vices\"\xff\x06\n\x0b\x45valuations\x12\x44\n\x07request\x18\x01 \x01(\x0b\x32*.indykite.auditsink.v1beta1.AuthZENRequestR\x07request\x12\x1a\n\x08response\x18\x02 \x01(\tR\x08response\x12T\n\x0b\x65valuations\x18\x03 \x03(\x0b\x32\x32.indykite.auditsink.v1beta1.Evaluations.EvaluationR\x0b\x65valuations\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1a\xce\x04\n\nEvaluation\x12T\n\x07request\x18\x01 \x01(\x0b\x32:.indykite.auditsink.v1beta1.Evaluations.Evaluation.RequestR\x07request\x12S\n\x07results\x18\x02 \x03(\x0b\x32\x39.indykite.auditsink.v1beta1.Evaluations.Evaluation.ResultR\x07results\x1a\xcb\x01\n\x07Request\x12!\n\x0csubject_type\x18\x01 \x01(\tR\x0bsubjectType\x12.\n\x13subject_external_id\x18\x02 \x01(\tR\x11subjectExternalId\x12#\n\rresource_type\x18\x03 \x01(\tR\x0cresourceType\x12\x30\n\x14resource_external_id\x18\x04 \x01(\tR\x12resourceExternalId\x12\x16\n\x06\x61\x63tion\x18\x05 \x01(\tR\x06\x61\x63tion\x1a\xc6\x01\n\x06Result\x12G\n\x06policy\x18\x01 \x01(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\x06policy\x12\x1d\n\nis_allowed\x18\x02 \x01(\x08R\tisAllowed\x12\x16\n\x06reason\x18\x03 \x01(\tR\x06reason\x12<\n\x07\x61\x64vices\x18\x04 \x03(\x0b\x32\".indykite.auditsink.v1beta1.AdviceR\x07\x61\x64vices\"\x9c\x03\n\rSearchSubject\x12\x44\n\x07request\x18\x01 \x01(\x0b\x32*.indykite.auditsink.v1beta1.AuthZENRequestR\x07request\x12\x1a\n\x08response\x18\x02 \x01(\tR\x08response\x12J\n\x07results\x18\x03 \x03(\x0b\x32\x30.indykite.auditsink.v1beta1.SearchSubject.ResultR\x07results\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1at\n\x06Result\x12G\n\x06policy\x18\x01 \x01(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\x06policy\x12!\n\x0c\x65xternal_ids\x18\x02 \x03(\tR\x0b\x65xternalIds\"\x9e\x03\n\x0eSearchResource\x12\x44\n\x07request\x18\x01 \x01(\x0b\x32*.indykite.auditsink.v1beta1.AuthZENRequestR\x07request\x12\x1a\n\x08response\x18\x02 \x01(\tR\x08response\x12K\n\x07results\x18\x03 \x03(\x0b\x32\x31.indykite.auditsink.v1beta1.SearchResource.ResultR\x07results\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1at\n\x06Result\x12G\n\x06policy\x18\x01 \x01(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\x06policy\x12!\n\x0c\x65xternal_ids\x18\x02 \x03(\tR\x0b\x65xternalIds\"\x91\x03\n\x0cSearchAction\x12\x44\n\x07request\x18\x01 \x01(\x0b\x32*.indykite.auditsink.v1beta1.AuthZENRequestR\x07request\x12\x1a\n\x08response\x18\x02 \x01(\tR\x08response\x12I\n\x07results\x18\x03 \x03(\x0b\x32/.indykite.auditsink.v1beta1.SearchAction.ResultR\x07results\x12#\n\rerror_message\x18\x04 \x01(\tR\x0c\x65rrorMessage\x12\x42\n\x0f\x65valuation_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x1ak\n\x06Result\x12G\n\x06policy\x18\x01 \x01(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\x06policy\x12\x18\n\x07\x61\x63tions\x18\x02 \x03(\tR\x07\x61\x63tions\"\xf8\x10\n\x0cIsAuthorized\x12J\n\x07request\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.IsAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12M\n\x08response\x18\x03 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.IsAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x12#\n\rerror_message\x18\x07 \x01(\tR\x0c\x65rrorMessage\x1a\xf1\x03\n\x07Request\x12J\n\x07subject\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.AuthorizationSubjectR\x07subject\x12W\n\tresources\x18\x02 \x03(\x0b\x32\x39.indykite.auditsink.v1beta1.IsAuthorized.Request.ResourceR\tresources\x12\x64\n\x0cinput_params\x18\x03 \x03(\x0b\x32\x41.indykite.auditsink.v1beta1.IsAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x04 \x03(\tR\npolicyTags\x1aY\n\x08Resource\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x03 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\xd7\x08\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12^\n\tdecisions\x18\x02 \x03(\x0b\x32@.indykite.auditsink.v1beta1.IsAuthorized.Response.DecisionsEntryR\tdecisions\x1a\xd9\x01\n\x06\x41\x64vice\x12\x14\n\x05\x65rror\x18\x01 \x01(\tR\x05\x65rror\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12\\\n\x06values\x18\x03 \x03(\x0b\x32\x44.indykite.auditsink.v1beta1.IsAuthorized.Response.Advice.ValuesEntryR\x06values\x1a\x39\n\x0bValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1ar\n\x06\x41\x63tion\x12\x14\n\x05\x61llow\x18\x01 \x01(\x08R\x05\x61llow\x12R\n\x07\x61\x64vices\x18\x02 \x03(\x0b\x32\x38.indykite.auditsink.v1beta1.IsAuthorized.Response.AdviceR\x07\x61\x64vices\x1a\xe3\x01\n\x08Resource\x12\x61\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32G.indykite.auditsink.v1beta1.IsAuthorized.Response.Resource.ActionsEntryR\x07\x61\x63tions\x1at\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12N\n\x05value\x18\x02 \x01(\x0b\x32\x38.indykite.auditsink.v1beta1.IsAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a\xf5\x01\n\x0cResourceType\x12k\n\tresources\x18\x01 \x03(\x0b\x32M.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceType.ResourcesEntryR\tresources\x1ax\n\x0eResourcesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x05value\x18\x02 \x01(\x0b\x32:.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceR\x05value:\x02\x38\x01\x1a|\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12T\n\x05value\x18\x02 \x01(\x0b\x32>.indykite.auditsink.v1beta1.IsAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\"\xcd\r\n\x0eWhatAuthorized\x12L\n\x07request\x18\x01 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.WhatAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12O\n\x08response\x18\x03 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.WhatAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x12#\n\rerror_message\x18\x07 \x01(\tR\x0c\x65rrorMessage\x1a\xe5\x03\n\x07Request\x12J\n\x07subject\x18\x01 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.AuthorizationSubjectR\x07subject\x12\x66\n\x0eresource_types\x18\x02 \x03(\x0b\x32?.indykite.auditsink.v1beta1.WhatAuthorized.Request.ResourceTypeR\rresourceTypes\x12\x66\n\x0cinput_params\x18\x03 \x03(\x0b\x32\x43.indykite.auditsink.v1beta1.WhatAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x04 \x03(\tR\npolicyTags\x1a<\n\x0cResourceType\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x02 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\xb2\x05\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12`\n\tdecisions\x18\x02 \x03(\x0b\x32\x42.indykite.auditsink.v1beta1.WhatAuthorized.Response.DecisionsEntryR\tdecisions\x1a+\n\x08Resource\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x1a\x64\n\x06\x41\x63tion\x12Z\n\tresources\x18\x01 \x03(\x0b\x32<.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceR\tresources\x1a\xef\x01\n\x0cResourceType\x12g\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32M.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceType.ActionsEntryR\x07\x61\x63tions\x1av\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x05value\x18\x02 \x01(\x0b\x32:.indykite.auditsink.v1beta1.WhatAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a~\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12V\n\x05value\x18\x02 \x01(\x0b\x32@.indykite.auditsink.v1beta1.WhatAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\"\x89\x0f\n\rWhoAuthorized\x12K\n\x07request\x18\x01 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.WhoAuthorized.RequestR\x07request\x12h\n\x15resolved_digital_twin\x18\x02 \x01(\x0b\x32\x34.indykite.auditsink.v1beta1.AuthorizationDigitalTwinR\x13resolvedDigitalTwin\x12N\n\x08response\x18\x03 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.WhoAuthorized.ResponseR\x08response\x12V\n\x0epolicies_found\x18\x04 \x03(\x0b\x32/.indykite.auditsink.v1beta1.AuthorizationPolicyR\rpoliciesFound\x12T\n\x0b\x64\x65ny_reason\x18\x05 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.AuthorizationDenyReasonR\ndenyReason\x12\x42\n\x0f\x65valuation_time\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x65valuationTime\x12#\n\rerror_message\x18\x07 \x01(\tR\x0c\x65rrorMessage\x1a\xa7\x03\n\x07Request\x12X\n\tresources\x18\x01 \x03(\x0b\x32:.indykite.auditsink.v1beta1.WhoAuthorized.Request.ResourceR\tresources\x12\x65\n\x0cinput_params\x18\x02 \x03(\x0b\x32\x42.indykite.auditsink.v1beta1.WhoAuthorized.Request.InputParamsEntryR\x0binputParams\x12\x1f\n\x0bpolicy_tags\x18\x03 \x03(\tR\npolicyTags\x1aY\n\x08Resource\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12\x18\n\x07\x61\x63tions\x18\x03 \x03(\tR\x07\x61\x63tions\x1a_\n\x10InputParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\x1a\xaf\x07\n\x08Response\x12?\n\rdecision_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x64\x65\x63isionTime\x12_\n\tdecisions\x18\x02 \x03(\x0b\x32\x41.indykite.auditsink.v1beta1.WhoAuthorized.Response.DecisionsEntryR\tdecisions\x1a>\n\x07Subject\x12\x1f\n\x0b\x65xternal_id\x18\x01 \x01(\tR\nexternalId\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x1a`\n\x06\x41\x63tion\x12V\n\x08subjects\x18\x01 \x03(\x0b\x32:.indykite.auditsink.v1beta1.WhoAuthorized.Response.SubjectR\x08subjects\x1a\xe5\x01\n\x08Resource\x12\x62\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32H.indykite.auditsink.v1beta1.WhoAuthorized.Response.Resource.ActionsEntryR\x07\x61\x63tions\x1au\n\x0c\x41\x63tionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12O\n\x05value\x18\x02 \x01(\x0b\x32\x39.indykite.auditsink.v1beta1.WhoAuthorized.Response.ActionR\x05value:\x02\x38\x01\x1a\xf7\x01\n\x0cResourceType\x12l\n\tresources\x18\x01 \x03(\x0b\x32N.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceType.ResourcesEntryR\tresources\x1ay\n\x0eResourcesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12Q\n\x05value\x18\x02 \x01(\x0b\x32;.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceR\x05value:\x02\x38\x01\x1a}\n\x0e\x44\x65\x63isionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12U\n\x05value\x18\x02 \x01(\x0b\x32?.indykite.auditsink.v1beta1.WhoAuthorized.Response.ResourceTypeR\x05value:\x02\x38\x01\x42\xbe\x01\n\x1e\x63om.indykite.auditsink.v1beta1B\x12\x41uthorizationProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1aIndykite.Auditsink.V1beta1\xca\x02\x1aIndykite\\Auditsink\\V1beta1\xe2\x02&Indykite\\Auditsink\\V1beta1\\GPBMetadata\xea\x02\x1cIndykite::Auditsink::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.auditsink.v1beta1.authorization_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.indykite.auditsink.v1beta1B\022AuthorizationProtoP\001\242\002\003IAX\252\002\032Indykite.Auditsink.V1beta1\312\002\032Indykite\\Auditsink\\V1beta1\342\002&Indykite\\Auditsink\\V1beta1\\GPBMetadata\352\002\034Indykite::Auditsink::V1beta1'
  _globals['_ADVICE_VALUESENTRY']._loaded_options = None
  _globals['_ADVICE_VALUESENTRY']._serialized_options = b'8\001'
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._loaded_options = None
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_options = b'8\001'
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE_VALUESENTRY']._loaded_options = None
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE_VALUESENTRY']._serialized_options = b'8\001'
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._loaded_options = None
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_options = b'8\001'
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._loaded_options = None
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_options = b'8\001'
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._loaded_options = None
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_options = b'8\001'
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._loaded_options = None
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_options = b'8\001'
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._loaded_options = None
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._serialized_options = b'8\001'
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._loaded_options = None
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_options = b'8\001'
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._loaded_options = None
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_options = b'8\001'
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._loaded_options = None
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_options = b'8\001'
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._loaded_options = None
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_options = b'8\001'
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._loaded_options = None
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_options = b'8\001'
  _globals['_AUTHORIZATIONSUBJECT']._serialized_start=183
  _globals['_AUTHORIZATIONSUBJECT']._serialized_end=707
  _globals['_AUTHORIZATIONSUBJECT_PROPERTY']._serialized_start=544
  _globals['_AUTHORIZATIONSUBJECT_PROPERTY']._serialized_end=629
  _globals['_AUTHORIZATIONSUBJECT_EXTERNALID']._serialized_start=631
  _globals['_AUTHORIZATIONSUBJECT_EXTERNALID']._serialized_end=696
  _globals['_AUTHORIZATIONDIGITALTWIN']._serialized_start=709
  _globals['_AUTHORIZATIONDIGITALTWIN']._serialized_end=751
  _globals['_AUTHORIZATIONPOLICY']._serialized_start=753
  _globals['_AUTHORIZATIONPOLICY']._serialized_end=810
  _globals['_AUTHORIZATIONDENYREASON']._serialized_start=812
  _globals['_AUTHORIZATIONDENYREASON']._serialized_end=863
  _globals['_AUTHZENREQUEST']._serialized_start=866
  _globals['_AUTHZENREQUEST']._serialized_end=1034
  _globals['_AUTHZENREQUEST_THIRDPARTYTOKEN']._serialized_start=986
  _globals['_AUTHZENREQUEST_THIRDPARTYTOKEN']._serialized_end=1034
  _globals['_ADVICE']._serialized_start=1037
  _globals['_ADVICE']._serialized_end=1176
  _globals['_ADVICE_VALUESENTRY']._serialized_start=1119
  _globals['_ADVICE_VALUESENTRY']._serialized_end=1176
  _globals['_EVALUATION']._serialized_start=1179
  _globals['_EVALUATION']._serialized_end=1644
  _globals['_EVALUATION_RESULT']._serialized_start=1470
  _globals['_EVALUATION_RESULT']._serialized_end=1644
  _globals['_EVALUATIONS']._serialized_start=1647
  _globals['_EVALUATIONS']._serialized_end=2542
  _globals['_EVALUATIONS_EVALUATION']._serialized_start=1952
  _globals['_EVALUATIONS_EVALUATION']._serialized_end=2542
  _globals['_EVALUATIONS_EVALUATION_REQUEST']._serialized_start=2138
  _globals['_EVALUATIONS_EVALUATION_REQUEST']._serialized_end=2341
  _globals['_EVALUATIONS_EVALUATION_RESULT']._serialized_start=2344
  _globals['_EVALUATIONS_EVALUATION_RESULT']._serialized_end=2542
  _globals['_SEARCHSUBJECT']._serialized_start=2545
  _globals['_SEARCHSUBJECT']._serialized_end=2957
  _globals['_SEARCHSUBJECT_RESULT']._serialized_start=2841
  _globals['_SEARCHSUBJECT_RESULT']._serialized_end=2957
  _globals['_SEARCHRESOURCE']._serialized_start=2960
  _globals['_SEARCHRESOURCE']._serialized_end=3374
  _globals['_SEARCHRESOURCE_RESULT']._serialized_start=2841
  _globals['_SEARCHRESOURCE_RESULT']._serialized_end=2957
  _globals['_SEARCHACTION']._serialized_start=3377
  _globals['_SEARCHACTION']._serialized_end=3778
  _globals['_SEARCHACTION_RESULT']._serialized_start=3671
  _globals['_SEARCHACTION_RESULT']._serialized_end=3778
  _globals['_ISAUTHORIZED']._serialized_start=3781
  _globals['_ISAUTHORIZED']._serialized_end=5949
  _globals['_ISAUTHORIZED_REQUEST']._serialized_start=4338
  _globals['_ISAUTHORIZED_REQUEST']._serialized_end=4835
  _globals['_ISAUTHORIZED_REQUEST_RESOURCE']._serialized_start=4649
  _globals['_ISAUTHORIZED_REQUEST_RESOURCE']._serialized_end=4738
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=4740
  _globals['_ISAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=4835
  _globals['_ISAUTHORIZED_RESPONSE']._serialized_start=4838
  _globals['_ISAUTHORIZED_RESPONSE']._serialized_end=5949
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE']._serialized_start=5012
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE']._serialized_end=5229
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE_VALUESENTRY']._serialized_start=1119
  _globals['_ISAUTHORIZED_RESPONSE_ADVICE_VALUESENTRY']._serialized_end=1176
  _globals['_ISAUTHORIZED_RESPONSE_ACTION']._serialized_start=5231
  _globals['_ISAUTHORIZED_RESPONSE_ACTION']._serialized_end=5345
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=5348
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=5575
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_start=5459
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_end=5575
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=5578
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=5823
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_start=5703
  _globals['_ISAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_end=5823
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=5825
  _globals['_ISAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=5949
  _globals['_WHATAUTHORIZED']._serialized_start=5952
  _globals['_WHATAUTHORIZED']._serialized_end=7693
  _globals['_WHATAUTHORIZED_REQUEST']._serialized_start=6515
  _globals['_WHATAUTHORIZED_REQUEST']._serialized_end=7000
  _globals['_WHATAUTHORIZED_REQUEST_RESOURCETYPE']._serialized_start=6843
  _globals['_WHATAUTHORIZED_REQUEST_RESOURCETYPE']._serialized_end=6903
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=4740
  _globals['_WHATAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=4835
  _globals['_WHATAUTHORIZED_RESPONSE']._serialized_start=7003
  _globals['_WHATAUTHORIZED_RESPONSE']._serialized_end=7693
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=4649
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=4692
  _globals['_WHATAUTHORIZED_RESPONSE_ACTION']._serialized_start=7223
  _globals['_WHATAUTHORIZED_RESPONSE_ACTION']._serialized_end=7323
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=7326
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=7565
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._serialized_start=7447
  _globals['_WHATAUTHORIZED_RESPONSE_RESOURCETYPE_ACTIONSENTRY']._serialized_end=7565
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=7567
  _globals['_WHATAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=7693
  _globals['_WHOAUTHORIZED']._serialized_start=7696
  _globals['_WHOAUTHORIZED']._serialized_end=9625
  _globals['_WHOAUTHORIZED_REQUEST']._serialized_start=8256
  _globals['_WHOAUTHORIZED_REQUEST']._serialized_end=8679
  _globals['_WHOAUTHORIZED_REQUEST_RESOURCE']._serialized_start=4649
  _globals['_WHOAUTHORIZED_REQUEST_RESOURCE']._serialized_end=4738
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_start=4740
  _globals['_WHOAUTHORIZED_REQUEST_INPUTPARAMSENTRY']._serialized_end=4835
  _globals['_WHOAUTHORIZED_RESPONSE']._serialized_start=8682
  _globals['_WHOAUTHORIZED_RESPONSE']._serialized_end=9625
  _globals['_WHOAUTHORIZED_RESPONSE_SUBJECT']._serialized_start=8856
  _globals['_WHOAUTHORIZED_RESPONSE_SUBJECT']._serialized_end=8918
  _globals['_WHOAUTHORIZED_RESPONSE_ACTION']._serialized_start=8920
  _globals['_WHOAUTHORIZED_RESPONSE_ACTION']._serialized_end=9016
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE']._serialized_start=9019
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE']._serialized_end=9248
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_start=9131
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCE_ACTIONSENTRY']._serialized_end=9248
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_start=9251
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE']._serialized_end=9498
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_start=9377
  _globals['_WHOAUTHORIZED_RESPONSE_RESOURCETYPE_RESOURCESENTRY']._serialized_end=9498
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_start=9500
  _globals['_WHOAUTHORIZED_RESPONSE_DECISIONSENTRY']._serialized_end=9625
# @@protoc_insertion_point(module_scope)
