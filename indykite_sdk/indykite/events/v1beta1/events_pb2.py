# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/events/v1beta1/events.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.type import latlng_pb2 as google_dot_type_dot_latlng__pb2
from indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$indykite/events/v1beta1/events.proto\x12\x17indykite.events.v1beta1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x18google/type/latlng.proto\x1a%indykite/objects/v1beta1/struct.proto\"\xd5\x01\n\x0c\x45ventContext\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12U\n\nattributes\x18\x02 \x03(\x0b\x32\x35.indykite.events.v1beta1.EventContext.AttributesEntryR\nattributes\x1a^\n\x0f\x41ttributesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\"\xaa\x02\n\x13\x41uthenticationEvent\x12?\n\x07\x63ontext\x18\x01 \x01(\x0b\x32%.indykite.events.v1beta1.EventContextR\x07\x63ontext\x12?\n\x06result\x18\x02 \x01(\x0e\x32\'.indykite.events.v1beta1.LoginEventTypeR\x06result\x12\x18\n\x07subject\x18\x03 \x01(\tR\x07subject\x12\x39\n\nevent_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\teventTime\x12<\n\x0fsource_position\x18\x05 \x01(\x0b\x32\x13.google.type.LatLngR\x0esourcePosition\"5\n\x05\x45mail\x12\x18\n\x07\x61\x64\x64ress\x18\x01 \x01(\tR\x07\x61\x64\x64ress\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"\xf2\x07\n\x16SendTemplateEmailEvent\x12\x1f\n\x0btemplate_id\x18\x01 \x01(\tR\ntemplateId\x12\x32\n\x04\x66rom\x18\x02 \x01(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x04\x66rom\x12\x39\n\x08reply_to\x18\x03 \x01(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x07replyTo\x12.\n\x02to\x18\x04 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x02to\x12.\n\x02\x63\x63\x18\x05 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x02\x63\x63\x12\x30\n\x03\x62\x63\x63\x18\x06 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x03\x62\x63\x63\x12\x18\n\x07subject\x18\x07 \x01(\tR\x07subject\x12V\n\x07headers\x18\x08 \x03(\x0b\x32<.indykite.events.v1beta1.SendTemplateEmailEvent.HeadersEntryR\x07headers\x12`\n\x0b\x63ustom_args\x18\x0b \x03(\x0b\x32?.indykite.events.v1beta1.SendTemplateEmailEvent.CustomArgsEntryR\ncustomArgs\x12\x82\x01\n\x17\x64ynamic_template_values\x18\x0c \x03(\x0b\x32J.indykite.events.v1beta1.SendTemplateEmailEvent.DynamicTemplateValuesEntryR\x15\x64ynamicTemplateValues\x12\x1e\n\ncategories\x18\r \x03(\tR\ncategories\x12<\n\x0csend_at_time\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nsendAtTime\x12\x19\n\x08\x62\x61tch_id\x18\x0f \x01(\tR\x07\x62\x61tchId\x1a:\n\x0cHeadersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a=\n\x0f\x43ustomArgsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1ai\n\x1a\x44ynamicTemplateValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\"\x93\x08\n\x15SendMessageEmailEvent\x12\x32\n\x04\x66rom\x18\x01 \x01(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x04\x66rom\x12\x39\n\x08reply_to\x18\x02 \x01(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x07replyTo\x12.\n\x02to\x18\x03 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x02to\x12.\n\x02\x63\x63\x18\x04 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x02\x63\x63\x12\x30\n\x03\x62\x63\x63\x18\x05 \x03(\x0b\x32\x1e.indykite.events.v1beta1.EmailR\x03\x62\x63\x63\x12\x18\n\x07subject\x18\x06 \x01(\tR\x07subject\x12!\n\x0ctext_content\x18\x07 \x01(\tR\x0btextContent\x12!\n\x0chtml_content\x18\x08 \x01(\tR\x0bhtmlContent\x12U\n\x07headers\x18\t \x03(\x0b\x32;.indykite.events.v1beta1.SendMessageEmailEvent.HeadersEntryR\x07headers\x12_\n\x0b\x63ustom_args\x18\n \x03(\x0b\x32>.indykite.events.v1beta1.SendMessageEmailEvent.CustomArgsEntryR\ncustomArgs\x12\x81\x01\n\x17\x64ynamic_template_values\x18\x0b \x03(\x0b\x32I.indykite.events.v1beta1.SendMessageEmailEvent.DynamicTemplateValuesEntryR\x15\x64ynamicTemplateValues\x12\x1e\n\ncategories\x18\x0c \x03(\tR\ncategories\x12<\n\x0csend_at_time\x18\r \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nsendAtTime\x12\x19\n\x08\x62\x61tch_id\x18\x0e \x01(\tR\x07\x62\x61tchId\x1a:\n\x0cHeadersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a=\n\x0f\x43ustomArgsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1ai\n\x1a\x44ynamicTemplateValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05value:\x02\x38\x01\"\xf1\x05\n\x13OPADecisionLogEvent\x12P\n\x06labels\x18\x01 \x03(\x0b\x32\x38.indykite.events.v1beta1.OPADecisionLogEvent.LabelsEntryR\x06labels\x12\x1f\n\x0b\x64\x65\x63ision_id\x18\x02 \x01(\tR\ndecisionId\x12S\n\x07\x62undles\x18\x03 \x03(\x0b\x32\x39.indykite.events.v1beta1.OPADecisionLogEvent.BundlesEntryR\x07\x62undles\x12\x12\n\x04path\x18\x04 \x01(\tR\x04path\x12\x14\n\x05query\x18\x05 \x01(\tR\x05query\x12\x35\n\x05input\x18\x06 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x05input\x12\x37\n\x06result\x18\x07 \x01(\x0b\x32\x1f.indykite.objects.v1beta1.ValueR\x06result\x12\x16\n\x06\x65rased\x18\x08 \x03(\tR\x06\x65rased\x12\x16\n\x06masked\x18\t \x03(\tR\x06masked\x12\x14\n\x05\x65rror\x18\n \x01(\tR\x05\x65rror\x12!\n\x0crequested_by\x18\x0b \x01(\tR\x0brequestedBy\x12\x33\n\x07\x61t_time\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x06\x61tTime\x12<\n\x07metrics\x18\r \x01(\x0b\x32\".indykite.objects.v1beta1.MapValueR\x07metrics\x1a\x39\n\x0bLabelsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a\x61\n\x0c\x42undlesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12;\n\x05value\x18\x02 \x01(\x0b\x32%.indykite.events.v1beta1.BundleInfoV1R\x05value:\x02\x38\x01\"*\n\x0c\x42undleInfoV1\x12\x1a\n\x08revision\x18\x03 \x01(\tR\x08revision\"\xd1\x07\n\x0bHTTPRequest\x12\x18\n\x07version\x18\x01 \x01(\tR\x07version\x12\x1b\n\troute_key\x18\x02 \x01(\tR\x08routeKey\x12\x19\n\x08raw_path\x18\x03 \x01(\tR\x07rawPath\x12(\n\x10raw_query_string\x18\x04 \x01(\tR\x0erawQueryString\x12\x18\n\x07\x63ookies\x18\x05 \x03(\tR\x07\x63ookies\x12K\n\x07headers\x18\x06 \x03(\x0b\x32\x31.indykite.events.v1beta1.HTTPRequest.HeadersEntryR\x07headers\x12w\n\x17query_string_parameters\x18\x07 \x03(\x0b\x32?.indykite.events.v1beta1.HTTPRequest.QueryStringParametersEntryR\x15queryStringParameters\x12\x61\n\x0fpath_parameters\x18\x08 \x03(\x0b\x32\x38.indykite.events.v1beta1.HTTPRequest.PathParametersEntryR\x0epathParameters\x12T\n\x0frequest_context\x18\t \x01(\x0b\x32+.indykite.events.v1beta1.HTTPRequestContextR\x0erequestContext\x12\x61\n\x0fstage_variables\x18\n \x03(\x0b\x32\x38.indykite.events.v1beta1.HTTPRequest.StageVariablesEntryR\x0estageVariables\x12\x12\n\x04\x62ody\x18\x0b \x01(\tR\x04\x62ody\x12*\n\x11is_base64_encoded\x18\x0c \x01(\x08R\x0fisBase64Encoded\x1a:\n\x0cHeadersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1aH\n\x1aQueryStringParametersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a\x41\n\x13PathParametersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a\x41\n\x13StageVariablesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xb0\x03\n\x12HTTPRequestContext\x12\x1b\n\troute_key\x18\x01 \x01(\tR\x08routeKey\x12\x1d\n\naccount_id\x18\x02 \x01(\tR\taccountId\x12\x14\n\x05stage\x18\x03 \x01(\tR\x05stage\x12\x1d\n\nrequest_id\x18\x04 \x01(\tR\trequestId\x12`\n\nauthorizer\x18\x05 \x01(\x0b\x32@.indykite.events.v1beta1.HTTPRequestContextAuthorizerDescriptionR\nauthorizer\x12\x1f\n\x0b\x64omain_name\x18\x06 \x01(\tR\ndomainName\x12#\n\rdomain_prefix\x18\x07 \x01(\tR\x0c\x64omainPrefix\x12\x12\n\x04time\x18\x08 \x01(\tR\x04time\x12\x1d\n\ntime_epoch\x18\t \x01(\x03R\ttimeEpoch\x12N\n\x04http\x18\n \x01(\x0b\x32:.indykite.events.v1beta1.HTTPRequestContextHTTPDescriptionR\x04http\"\x80\x01\n\'HTTPRequestContextAuthorizerDescription\x12U\n\x03jwt\x18\x01 \x01(\x0b\x32\x43.indykite.events.v1beta1.HTTPRequestContextAuthorizerJWTDescriptionR\x03jwt\"\xe8\x01\n*HTTPRequestContextAuthorizerJWTDescription\x12g\n\x06\x63laims\x18\x01 \x03(\x0b\x32O.indykite.events.v1beta1.HTTPRequestContextAuthorizerJWTDescription.ClaimsEntryR\x06\x63laims\x12\x16\n\x06scopes\x18\x02 \x03(\tR\x06scopes\x1a\x39\n\x0b\x43laimsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xf3\x01\n!HTTPRequestContextHTTPDescription\x12;\n\x06method\x18\x01 \x01(\x0e\x32#.indykite.events.v1beta1.HTTPMethodR\x06method\x12\x12\n\x04path\x18\x02 \x01(\tR\x04path\x12\x41\n\x08protocol\x18\x03 \x01(\x0e\x32%.indykite.events.v1beta1.HTTPProtocolR\x08protocol\x12\x1b\n\tsource_ip\x18\x04 \x01(\tR\x08sourceIp\x12\x1d\n\nuser_agent\x18\x05 \x01(\tR\tuserAgent*i\n\x0eLoginEventType\x12\x1c\n\x18LOGIN_EVENT_TYPE_INVALID\x10\x00\x12\x1c\n\x18LOGIN_EVENT_TYPE_SUCCESS\x10\x01\x12\x1b\n\x17LOGIN_EVENT_TYPE_FAILED\x10\x02*\xf3\x01\n\nHTTPMethod\x12\x17\n\x13HTTP_METHOD_INVALID\x10\x00\x12\x13\n\x0fHTTP_METHOD_GET\x10\x01\x12\x14\n\x10HTTP_METHOD_HEAD\x10\x02\x12\x14\n\x10HTTP_METHOD_POST\x10\x03\x12\x13\n\x0fHTTP_METHOD_PUT\x10\x04\x12\x15\n\x11HTTP_METHOD_PATCH\x10\x05\x12\x16\n\x12HTTP_METHOD_DELETE\x10\x06\x12\x17\n\x13HTTP_METHOD_CONNECT\x10\x07\x12\x17\n\x13HTTP_METHOD_OPTIONS\x10\x08\x12\x15\n\x11HTTP_METHOD_TRACE\x10\t*a\n\x0cHTTPProtocol\x12\x19\n\x15HTTP_PROTOCOL_INVALID\x10\x00\x12\x1a\n\x16HTTP_PROTOCOL_HTTP_1_1\x10\x01\x12\x1a\n\x16HTTP_PROTOCOL_HTTP_2_0\x10\x02\x42\xe3\x01\n\x1b\x63om.indykite.events.v1beta1B\x0b\x45ventsProtoP\x01Z9github.com/indykite/jarvis/pkg/proto-gen/events/v1;events\xa2\x02\x03IEX\xaa\x02\x17Indykite.Events.V1beta1\xca\x02\x17Indykite\\Events\\V1beta1\xe2\x02#Indykite\\Events\\V1beta1\\GPBMetadata\xea\x02\x19Indykite::Events::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.events.v1beta1.events_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033com.indykite.events.v1beta1B\013EventsProtoP\001Z9github.com/indykite/jarvis/pkg/proto-gen/events/v1;events\242\002\003IEX\252\002\027Indykite.Events.V1beta1\312\002\027Indykite\\Events\\V1beta1\342\002#Indykite\\Events\\V1beta1\\GPBMetadata\352\002\031Indykite::Events::V1beta1'
  _EVENTCONTEXT_ATTRIBUTESENTRY._options = None
  _EVENTCONTEXT_ATTRIBUTESENTRY._serialized_options = b'8\001'
  _SENDTEMPLATEEMAILEVENT_HEADERSENTRY._options = None
  _SENDTEMPLATEEMAILEVENT_HEADERSENTRY._serialized_options = b'8\001'
  _SENDTEMPLATEEMAILEVENT_CUSTOMARGSENTRY._options = None
  _SENDTEMPLATEEMAILEVENT_CUSTOMARGSENTRY._serialized_options = b'8\001'
  _SENDTEMPLATEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY._options = None
  _SENDTEMPLATEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY._serialized_options = b'8\001'
  _SENDMESSAGEEMAILEVENT_HEADERSENTRY._options = None
  _SENDMESSAGEEMAILEVENT_HEADERSENTRY._serialized_options = b'8\001'
  _SENDMESSAGEEMAILEVENT_CUSTOMARGSENTRY._options = None
  _SENDMESSAGEEMAILEVENT_CUSTOMARGSENTRY._serialized_options = b'8\001'
  _SENDMESSAGEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY._options = None
  _SENDMESSAGEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY._serialized_options = b'8\001'
  _OPADECISIONLOGEVENT_LABELSENTRY._options = None
  _OPADECISIONLOGEVENT_LABELSENTRY._serialized_options = b'8\001'
  _OPADECISIONLOGEVENT_BUNDLESENTRY._options = None
  _OPADECISIONLOGEVENT_BUNDLESENTRY._serialized_options = b'8\001'
  _HTTPREQUEST_HEADERSENTRY._options = None
  _HTTPREQUEST_HEADERSENTRY._serialized_options = b'8\001'
  _HTTPREQUEST_QUERYSTRINGPARAMETERSENTRY._options = None
  _HTTPREQUEST_QUERYSTRINGPARAMETERSENTRY._serialized_options = b'8\001'
  _HTTPREQUEST_PATHPARAMETERSENTRY._options = None
  _HTTPREQUEST_PATHPARAMETERSENTRY._serialized_options = b'8\001'
  _HTTPREQUEST_STAGEVARIABLESENTRY._options = None
  _HTTPREQUEST_STAGEVARIABLESENTRY._serialized_options = b'8\001'
  _HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION_CLAIMSENTRY._options = None
  _HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION_CLAIMSENTRY._serialized_options = b'8\001'
  _globals['_LOGINEVENTTYPE']._serialized_start=5621
  _globals['_LOGINEVENTTYPE']._serialized_end=5726
  _globals['_HTTPMETHOD']._serialized_start=5729
  _globals['_HTTPMETHOD']._serialized_end=5972
  _globals['_HTTPPROTOCOL']._serialized_start=5974
  _globals['_HTTPPROTOCOL']._serialized_end=6071
  _globals['_EVENTCONTEXT']._serialized_start=164
  _globals['_EVENTCONTEXT']._serialized_end=377
  _globals['_EVENTCONTEXT_ATTRIBUTESENTRY']._serialized_start=283
  _globals['_EVENTCONTEXT_ATTRIBUTESENTRY']._serialized_end=377
  _globals['_AUTHENTICATIONEVENT']._serialized_start=380
  _globals['_AUTHENTICATIONEVENT']._serialized_end=678
  _globals['_EMAIL']._serialized_start=680
  _globals['_EMAIL']._serialized_end=733
  _globals['_SENDTEMPLATEEMAILEVENT']._serialized_start=736
  _globals['_SENDTEMPLATEEMAILEVENT']._serialized_end=1746
  _globals['_SENDTEMPLATEEMAILEVENT_HEADERSENTRY']._serialized_start=1518
  _globals['_SENDTEMPLATEEMAILEVENT_HEADERSENTRY']._serialized_end=1576
  _globals['_SENDTEMPLATEEMAILEVENT_CUSTOMARGSENTRY']._serialized_start=1578
  _globals['_SENDTEMPLATEEMAILEVENT_CUSTOMARGSENTRY']._serialized_end=1639
  _globals['_SENDTEMPLATEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY']._serialized_start=1641
  _globals['_SENDTEMPLATEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY']._serialized_end=1746
  _globals['_SENDMESSAGEEMAILEVENT']._serialized_start=1749
  _globals['_SENDMESSAGEEMAILEVENT']._serialized_end=2792
  _globals['_SENDMESSAGEEMAILEVENT_HEADERSENTRY']._serialized_start=1518
  _globals['_SENDMESSAGEEMAILEVENT_HEADERSENTRY']._serialized_end=1576
  _globals['_SENDMESSAGEEMAILEVENT_CUSTOMARGSENTRY']._serialized_start=1578
  _globals['_SENDMESSAGEEMAILEVENT_CUSTOMARGSENTRY']._serialized_end=1639
  _globals['_SENDMESSAGEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY']._serialized_start=1641
  _globals['_SENDMESSAGEEMAILEVENT_DYNAMICTEMPLATEVALUESENTRY']._serialized_end=1746
  _globals['_OPADECISIONLOGEVENT']._serialized_start=2795
  _globals['_OPADECISIONLOGEVENT']._serialized_end=3548
  _globals['_OPADECISIONLOGEVENT_LABELSENTRY']._serialized_start=3392
  _globals['_OPADECISIONLOGEVENT_LABELSENTRY']._serialized_end=3449
  _globals['_OPADECISIONLOGEVENT_BUNDLESENTRY']._serialized_start=3451
  _globals['_OPADECISIONLOGEVENT_BUNDLESENTRY']._serialized_end=3548
  _globals['_BUNDLEINFOV1']._serialized_start=3550
  _globals['_BUNDLEINFOV1']._serialized_end=3592
  _globals['_HTTPREQUEST']._serialized_start=3595
  _globals['_HTTPREQUEST']._serialized_end=4572
  _globals['_HTTPREQUEST_HEADERSENTRY']._serialized_start=1518
  _globals['_HTTPREQUEST_HEADERSENTRY']._serialized_end=1576
  _globals['_HTTPREQUEST_QUERYSTRINGPARAMETERSENTRY']._serialized_start=4366
  _globals['_HTTPREQUEST_QUERYSTRINGPARAMETERSENTRY']._serialized_end=4438
  _globals['_HTTPREQUEST_PATHPARAMETERSENTRY']._serialized_start=4440
  _globals['_HTTPREQUEST_PATHPARAMETERSENTRY']._serialized_end=4505
  _globals['_HTTPREQUEST_STAGEVARIABLESENTRY']._serialized_start=4507
  _globals['_HTTPREQUEST_STAGEVARIABLESENTRY']._serialized_end=4572
  _globals['_HTTPREQUESTCONTEXT']._serialized_start=4575
  _globals['_HTTPREQUESTCONTEXT']._serialized_end=5007
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERDESCRIPTION']._serialized_start=5010
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERDESCRIPTION']._serialized_end=5138
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION']._serialized_start=5141
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION']._serialized_end=5373
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION_CLAIMSENTRY']._serialized_start=5316
  _globals['_HTTPREQUESTCONTEXTAUTHORIZERJWTDESCRIPTION_CLAIMSENTRY']._serialized_end=5373
  _globals['_HTTPREQUESTCONTEXTHTTPDESCRIPTION']._serialized_start=5376
  _globals['_HTTPREQUESTCONTEXTHTTPDESCRIPTION']._serialized_end=5619
# @@protoc_insertion_point(module_scope)
