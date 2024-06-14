# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/identity/v1beta1/model.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from indykite_sdk.indykite.identity.v1beta1 import attributes_pb2 as indykite_dot_identity_dot_v1beta1_dot_attributes__pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as indykite_dot_objects_dot_v1beta1_dot_struct__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%indykite/identity/v1beta1/model.proto\x12\x19indykite.identity.v1beta1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a*indykite/identity/v1beta1/attributes.proto\x1a%indykite/objects/v1beta1/struct.proto\x1a\x17validate/validate.proto\"\x92\x02\n\x0b\x44igitalTwin\x12\x17\n\x02id\x18\x01 \x01(\x0c\x42\x07\xfa\x42\x04z\x02h\x10R\x02id\x12\x1b\n\ttenant_id\x18\x02 \x01(\x0cR\x08tenantId\x12H\n\x04kind\x18\x03 \x01(\x0e\x32*.indykite.identity.v1beta1.DigitalTwinKindB\x08\xfa\x42\x05\x82\x01\x02\x10\x01R\x04kind\x12K\n\x05state\x18\x04 \x01(\x0e\x32+.indykite.identity.v1beta1.DigitalTwinStateB\x08\xfa\x42\x05\x82\x01\x02\x10\x01R\x05state\x12\x36\n\x04tags\x18\x05 \x03(\tB\"\xfa\x42\x1f\x92\x01\x1c\x10 \x18\x01\"\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04tags\"\xdc\x01\n\rDigitalEntity\x12I\n\x0c\x64igital_twin\x18\x01 \x01(\x0b\x32&.indykite.identity.v1beta1.DigitalTwinR\x0b\x64igitalTwin\x12;\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12\x43\n\nproperties\x18\x03 \x03(\x0b\x32#.indykite.identity.v1beta1.PropertyR\nproperties\"\x92\x01\n\x0c\x45rrorMessage\x12\x38\n\x04\x63ode\x18\x01 \x01(\x0e\x32$.indykite.identity.v1beta1.ErrorCodeR\x04\x63ode\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12.\n\x06\x64\x65tail\x18\x03 \x01(\x0b\x32\x16.google.protobuf.ValueR\x06\x64\x65tail\"\xeb\x03\n\nInvitation\x12\x1b\n\ttenant_id\x18\x01 \x01(\x0cR\x08tenantId\x12!\n\x0creference_id\x18\x02 \x01(\tR\x0breferenceId\x12@\n\x0einvite_at_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0cinviteAtTime\x12;\n\x0b\x65xpire_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpireTime\x12Q\n\x12message_attributes\x18\x05 \x01(\x0b\x32\".indykite.objects.v1beta1.MapValueR\x11messageAttributes\x12G\n\x0b\x61\x63\x63\x65pted_by\x18\x08 \x01(\x0b\x32&.indykite.identity.v1beta1.DigitalTwinR\nacceptedBy\x12@\n\x05state\x18\t \x01(\x0e\x32*.indykite.identity.v1beta1.InvitationStateR\x05state\x12\x16\n\x05\x65mail\x18\x06 \x01(\tH\x00R\x05\x65mail\x12\x18\n\x06mobile\x18\x07 \x01(\tH\x00R\x06mobileB\x0e\n\x07invitee\x12\x03\xf8\x42\x01\"\xc4\x0b\n\tWellKnown\x12\x16\n\x06issuer\x18\x01 \x01(\tR\x06issuer\x12\x35\n\x16\x61uthorization_endpoint\x18\x02 \x01(\tR\x15\x61uthorizationEndpoint\x12\x33\n\x15registration_endpoint\x18\x03 \x01(\tR\x14registrationEndpoint\x12%\n\x0etoken_endpoint\x18\x04 \x01(\tR\rtokenEndpoint\x12\x19\n\x08jwks_uri\x18\x05 \x01(\tR\x07jwksUri\x12\x36\n\x17subject_types_supported\x18\x06 \x03(\tR\x15subjectTypesSupported\x12\x38\n\x18response_types_supported\x18\x07 \x03(\tR\x16responseTypesSupported\x12)\n\x10\x63laims_supported\x18\x08 \x03(\tR\x0f\x63laimsSupported\x12\x32\n\x15grant_types_supported\x18\t \x03(\tR\x13grantTypesSupported\x12\x38\n\x18response_modes_supported\x18\n \x03(\tR\x16responseModesSupported\x12+\n\x11userinfo_endpoint\x18\x0b \x01(\tR\x10userinfoEndpoint\x12)\n\x10scopes_supported\x18\x0c \x03(\tR\x0fscopesSupported\x12P\n%token_endpoint_auth_methods_supported\x18\r \x03(\tR!tokenEndpointAuthMethodsSupported\x12P\n%userinfo_signing_alg_values_supported\x18\x0e \x03(\tR!userinfoSigningAlgValuesSupported\x12O\n%id_token_signing_alg_values_supported\x18\x0f \x03(\tR idTokenSigningAlgValuesSupported\x12>\n\x1brequest_parameter_supported\x18\x10 \x01(\x08R\x19requestParameterSupported\x12\x45\n\x1frequest_uri_parameter_supported\x18\x11 \x01(\x08R\x1crequestUriParameterSupported\x12G\n require_request_uri_registration\x18\x12 \x01(\x08R\x1drequireRequestUriRegistration\x12<\n\x1a\x63laims_parameter_supported\x18\x13 \x01(\x08R\x18\x63laimsParameterSupported\x12/\n\x13revocation_endpoint\x18\x14 \x01(\tR\x12revocationEndpoint\x12@\n\x1c\x62\x61\x63kchannel_logout_supported\x18\x15 \x01(\x08R\x1a\x62\x61\x63kchannelLogoutSupported\x12O\n$backchannel_logout_session_supported\x18\x16 \x01(\x08R!backchannelLogoutSessionSupported\x12\x42\n\x1d\x66rontchannel_logout_supported\x18\x17 \x01(\x08R\x1b\x66rontchannelLogoutSupported\x12Q\n%frontchannel_logout_session_supported\x18\x18 \x01(\x08R\"frontchannelLogoutSessionSupported\x12\x30\n\x14\x65nd_session_endpoint\x18\x19 \x01(\tR\x12\x65ndSessionEndpoint\"\xcc\x01\n\x13OAuth2TokenResponse\x12\x1d\n\nexpires_in\x18\x01 \x01(\x03R\texpiresIn\x12\x14\n\x05scope\x18\x02 \x01(\tR\x05scope\x12\x19\n\x08id_token\x18\x03 \x01(\tR\x07idToken\x12!\n\x0c\x61\x63\x63\x65ss_token\x18\x04 \x01(\tR\x0b\x61\x63\x63\x65ssToken\x12#\n\rrefresh_token\x18\x05 \x01(\tR\x0crefreshToken\x12\x1d\n\ntoken_type\x18\x06 \x01(\tR\ttokenType\"?\n FlushInactiveOAuth2TokensRequest\x12\x1b\n\tnot_after\x18\x01 \x01(\x03R\x08notAfter\"\x9a\x05\n\x11IdentityTokenInfo\x12\x1f\n\x0b\x63ustomer_id\x18\x01 \x01(\x0cR\ncustomerId\x12 \n\x0c\x61pp_space_id\x18\x02 \x01(\x0cR\nappSpaceId\x12%\n\x0e\x61pplication_id\x18\x03 \x01(\x0cR\rapplicationId\x12@\n\x07subject\x18\x04 \x01(\x0b\x32&.indykite.identity.v1beta1.DigitalTwinR\x07subject\x12J\n\x0cimpersonated\x18\x05 \x01(\x0b\x32&.indykite.identity.v1beta1.DigitalTwinR\x0cimpersonated\x12\x39\n\nissue_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tissueTime\x12;\n\x0b\x65xpire_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpireTime\x12K\n\x13\x61uthentication_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x12\x61uthenticationTime\x12L\n\rprovider_info\x18\t \x03(\x0b\x32\'.indykite.identity.v1beta1.ProviderInfoR\x0cproviderInfo\x12>\n\x0esession_claims\x18\n \x01(\x0b\x32\x17.google.protobuf.StructR\rsessionClaims\x12:\n\x0ctoken_claims\x18\x0b \x01(\x0b\x32\x17.google.protobuf.StructR\x0btokenClaims\"c\n\x0cProviderInfo\x12;\n\x04type\x18\x01 \x01(\x0e\x32\'.indykite.identity.v1beta1.ProviderTypeR\x04type\x12\x16\n\x06issuer\x18\x02 \x01(\tR\x06issuer\"\xd6\x04\n\x17UserInfoResponsePayload\x12\x10\n\x03sub\x18\x01 \x01(\tR\x03sub\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12\x1d\n\ngiven_name\x18\x03 \x01(\tR\tgivenName\x12\x1f\n\x0b\x66\x61mily_name\x18\x04 \x01(\tR\nfamilyName\x12\x1f\n\x0bmiddle_name\x18\x05 \x01(\tR\nmiddleName\x12\x1a\n\x08nickname\x18\x06 \x01(\tR\x08nickname\x12-\n\x12preferred_username\x18\x07 \x01(\tR\x11preferredUsername\x12\x18\n\x07profile\x18\x08 \x01(\tR\x07profile\x12\x18\n\x07picture\x18\t \x01(\tR\x07picture\x12\x18\n\x07website\x18\n \x01(\tR\x07website\x12\x14\n\x05\x65mail\x18\x0b \x01(\tR\x05\x65mail\x12%\n\x0e\x65mail_verified\x18\x0c \x01(\x08R\remailVerified\x12\x16\n\x06gender\x18\r \x01(\tR\x06gender\x12\x1c\n\tbirthdate\x18\x0e \x01(\tR\tbirthdate\x12\x1a\n\x08zoneinfo\x18\x0f \x01(\tR\x08zoneinfo\x12\x16\n\x06locale\x18\x10 \x01(\tR\x06locale\x12!\n\x0cphone_number\x18\x11 \x01(\tR\x0bphoneNumber\x12\x32\n\x15phone_number_verified\x18\x12 \x01(\x08R\x13phoneNumberVerified\x12\x1d\n\nupdated_at\x18\x13 \x01(\x03R\tupdatedAt\"\xf8\x0b\n\rPostalAddress\x12l\n\x0c\x61\x64\x64ress_type\x18\x0f \x01(\tBI\xfa\x42\x46rDR\x04homeR\x0ehome_preferredR\x04workR\x0ework_preferredR\x05otherR\x0fother_preferredR\x0b\x61\x64\x64ressType\x12\x31\n\x0f\x61\x64\x64ress_country\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\x18\xfe\x01R\x0e\x61\x64\x64ressCountry\x12\x9e\x08\n\x14\x61\x64\x64ress_country_code\x18\x02 \x01(\tB\xeb\x07\xfa\x42\xe7\x07r\xe4\x07R\x02\x41\x46R\x02\x41XR\x02\x41LR\x02\x44ZR\x02\x41SR\x02\x41\x44R\x02\x41OR\x02\x41IR\x02\x41QR\x02\x41GR\x02\x41RR\x02\x41MR\x02\x41WR\x02\x41UR\x02\x41TR\x02\x41ZR\x02\x42SR\x02\x42HR\x02\x42\x44R\x02\x42\x42R\x02\x42YR\x02\x42\x45R\x02\x42ZR\x02\x42JR\x02\x42MR\x02\x42TR\x02\x42OR\x02\x42QR\x02\x42\x41R\x02\x42WR\x02\x42VR\x02\x42RR\x02IOR\x02\x42NR\x02\x42GR\x02\x42\x46R\x02\x42IR\x02KHR\x02\x43MR\x02\x43\x41R\x02\x43VR\x02KYR\x02\x43\x46R\x02TDR\x02\x43LR\x02\x43NR\x02\x43XR\x02\x43\x43R\x02\x43OR\x02KMR\x02\x43GR\x02\x43\x44R\x02\x43KR\x02\x43RR\x02\x43IR\x02HRR\x02\x43UR\x02\x43WR\x02\x43YR\x02\x43ZR\x02\x44KR\x02\x44JR\x02\x44MR\x02\x44OR\x02\x45\x43R\x02\x45GR\x02SVR\x02GQR\x02\x45RR\x02\x45\x45R\x02\x45TR\x02\x46KR\x02\x46OR\x02\x46JR\x02\x46IR\x02\x46RR\x02GFR\x02PFR\x02TFR\x02GAR\x02GMR\x02GER\x02\x44\x45R\x02GHR\x02GIR\x02GRR\x02GLR\x02GDR\x02GPR\x02GUR\x02GTR\x02GGR\x02GNR\x02GWR\x02GYR\x02HTR\x02HMR\x02VAR\x02HNR\x02HKR\x02HUR\x02ISR\x02INR\x02IDR\x02IRR\x02IQR\x02IER\x02IMR\x02ILR\x02ITR\x02JMR\x02JPR\x02JER\x02JOR\x02KZR\x02KER\x02KIR\x02KPR\x02KRR\x02KWR\x02KGR\x02LAR\x02LVR\x02LBR\x02LSR\x02LRR\x02LYR\x02LIR\x02LTR\x02LUR\x02MOR\x02MKR\x02MGR\x02MWR\x02MYR\x02MVR\x02MLR\x02MTR\x02MHR\x02MQR\x02MRR\x02MUR\x02YTR\x02MXR\x02\x46MR\x02MDR\x02MCR\x02MNR\x02MER\x02MSR\x02MAR\x02MZR\x02MMR\x02NAR\x02NRR\x02NPR\x02NLR\x02NCR\x02NZR\x02NIR\x02NER\x02NGR\x02NUR\x02NFR\x02MPR\x02NOR\x02OMR\x02PKR\x02PWR\x02PSR\x02PAR\x02PGR\x02PYR\x02PER\x02PHR\x02PNR\x02PLR\x02PTR\x02PRR\x02QAR\x02RER\x02ROR\x02RUR\x02RWR\x02\x42LR\x02SHR\x02KNR\x02LCR\x02MFR\x02PMR\x02VCR\x02WSR\x02SMR\x02STR\x02SAR\x02SNR\x02RSR\x02SCR\x02SLR\x02SGR\x02SXR\x02SKR\x02SIR\x02SBR\x02SOR\x02ZAR\x02GSR\x02SSR\x02\x45SR\x02LKR\x02SDR\x02SRR\x02SJR\x02SZR\x02SER\x02\x43HR\x02SYR\x02TWR\x02TJR\x02TZR\x02THR\x02TLR\x02TGR\x02TKR\x02TOR\x02TTR\x02TNR\x02TRR\x02TMR\x02TCR\x02TVR\x02UGR\x02UAR\x02\x41\x45R\x02GBR\x02USR\x02UMR\x02UYR\x02UZR\x02VUR\x02VER\x02VNR\x02VGR\x02VIR\x02WFR\x02\x45HR\x02YER\x02ZMR\x02ZWR\x12\x61\x64\x64ressCountryCode\x12\x33\n\x10\x61\x64\x64ress_locality\x18\x03 \x01(\tB\x08\xfa\x42\x05r\x03\x18\xfe\x01R\x0f\x61\x64\x64ressLocality\x12/\n\x0e\x61\x64\x64ress_region\x18\x04 \x01(\tB\x08\xfa\x42\x05r\x03\x18\xfe\x01R\raddressRegion\x12<\n\x16post_office_box_number\x18\x05 \x01(\tB\x07\xfa\x42\x04r\x02\x18\x32R\x13postOfficeBoxNumber\x12(\n\x0bpostal_code\x18\x06 \x01(\tB\x07\xfa\x42\x04r\x02\x18\x32R\npostalCode\x12/\n\x0estreet_address\x18\x07 \x01(\tB\x08\xfa\x42\x05r\x03\x18\xfe\x01R\rstreetAddress\x12&\n\tformatted\x18\x08 \x01(\tB\x08\xfa\x42\x05r\x03\x18\x80\x08R\tformatted*\x94\x01\n\x10\x44igitalTwinState\x12\x1e\n\x1a\x44IGITAL_TWIN_STATE_INVALID\x10\x00\x12\x1d\n\x19\x44IGITAL_TWIN_STATE_ACTIVE\x10\x01\x12\x1f\n\x1b\x44IGITAL_TWIN_STATE_DISABLED\x10\x02\x12 \n\x1c\x44IGITAL_TWIN_STATE_TOMBSTONE\x10\x04*\x8a\x01\n\x0f\x44igitalTwinKind\x12\x1d\n\x19\x44IGITAL_TWIN_KIND_INVALID\x10\x00\x12\x1c\n\x18\x44IGITAL_TWIN_KIND_PERSON\x10\x01\x12\x1d\n\x19\x44IGITAL_TWIN_KIND_SERVICE\x10\x02\x12\x1b\n\x17\x44IGITAL_TWIN_KIND_THING\x10\x03*`\n\tErrorCode\x12\x16\n\x12\x45RROR_CODE_INVALID\x10\x00\x12\x1e\n\x1a\x45RROR_CODE_INVALID_REQUEST\x10\x01\x12\x1b\n\x17\x45RROR_CODE_UNAUTHORIZED\x10\x02*\xca\x01\n\x0fInvitationState\x12\x1c\n\x18INVITATION_STATE_INVALID\x10\x00\x12\x1e\n\x1aINVITATION_STATE_IN_FUTURE\x10\x01\x12\x1c\n\x18INVITATION_STATE_PENDING\x10\x02\x12\x1d\n\x19INVITATION_STATE_ACCEPTED\x10\x03\x12\x1c\n\x18INVITATION_STATE_EXPIRED\x10\x04\x12\x1e\n\x1aINVITATION_STATE_CANCELLED\x10\x05*\xa9\x01\n\x0cProviderType\x12\x19\n\x15PROVIDER_TYPE_INVALID\x10\x00\x12\x1a\n\x16PROVIDER_TYPE_PASSWORD\x10\x01\x12\x16\n\x12PROVIDER_TYPE_OIDC\x10\x02\x12\x1a\n\x16PROVIDER_TYPE_WEBAUTHN\x10\x03\x12\x17\n\x13PROVIDER_TYPE_EMAIL\x10\x04\x12\x15\n\x11PROVIDER_TYPE_SMS\x10\x05\x42\xb1\x01\n\x1d\x63om.indykite.identity.v1beta1B\nModelProtoP\x01\xa2\x02\x03IIX\xaa\x02\x19Indykite.Identity.V1beta1\xca\x02\x19Indykite\\Identity\\V1beta1\xe2\x02%Indykite\\Identity\\V1beta1\\GPBMetadata\xea\x02\x1bIndykite::Identity::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.identity.v1beta1.model_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\035com.indykite.identity.v1beta1B\nModelProtoP\001\242\002\003IIX\252\002\031Indykite.Identity.V1beta1\312\002\031Indykite\\Identity\\V1beta1\342\002%Indykite\\Identity\\V1beta1\\GPBMetadata\352\002\033Indykite::Identity::V1beta1'
  _globals['_DIGITALTWIN'].fields_by_name['id']._loaded_options = None
  _globals['_DIGITALTWIN'].fields_by_name['id']._serialized_options = b'\372B\004z\002h\020'
  _globals['_DIGITALTWIN'].fields_by_name['kind']._loaded_options = None
  _globals['_DIGITALTWIN'].fields_by_name['kind']._serialized_options = b'\372B\005\202\001\002\020\001'
  _globals['_DIGITALTWIN'].fields_by_name['state']._loaded_options = None
  _globals['_DIGITALTWIN'].fields_by_name['state']._serialized_options = b'\372B\005\202\001\002\020\001'
  _globals['_DIGITALTWIN'].fields_by_name['tags']._loaded_options = None
  _globals['_DIGITALTWIN'].fields_by_name['tags']._serialized_options = b'\372B\037\222\001\034\020 \030\001\"\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_INVITATION'].oneofs_by_name['invitee']._loaded_options = None
  _globals['_INVITATION'].oneofs_by_name['invitee']._serialized_options = b'\370B\001'
  _globals['_POSTALADDRESS'].fields_by_name['address_type']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['address_type']._serialized_options = b'\372BFrDR\004homeR\016home_preferredR\004workR\016work_preferredR\005otherR\017other_preferred'
  _globals['_POSTALADDRESS'].fields_by_name['address_country']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['address_country']._serialized_options = b'\372B\005r\003\030\376\001'
  _globals['_POSTALADDRESS'].fields_by_name['address_country_code']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['address_country_code']._serialized_options = b'\372B\347\007r\344\007R\002AFR\002AXR\002ALR\002DZR\002ASR\002ADR\002AOR\002AIR\002AQR\002AGR\002ARR\002AMR\002AWR\002AUR\002ATR\002AZR\002BSR\002BHR\002BDR\002BBR\002BYR\002BER\002BZR\002BJR\002BMR\002BTR\002BOR\002BQR\002BAR\002BWR\002BVR\002BRR\002IOR\002BNR\002BGR\002BFR\002BIR\002KHR\002CMR\002CAR\002CVR\002KYR\002CFR\002TDR\002CLR\002CNR\002CXR\002CCR\002COR\002KMR\002CGR\002CDR\002CKR\002CRR\002CIR\002HRR\002CUR\002CWR\002CYR\002CZR\002DKR\002DJR\002DMR\002DOR\002ECR\002EGR\002SVR\002GQR\002ERR\002EER\002ETR\002FKR\002FOR\002FJR\002FIR\002FRR\002GFR\002PFR\002TFR\002GAR\002GMR\002GER\002DER\002GHR\002GIR\002GRR\002GLR\002GDR\002GPR\002GUR\002GTR\002GGR\002GNR\002GWR\002GYR\002HTR\002HMR\002VAR\002HNR\002HKR\002HUR\002ISR\002INR\002IDR\002IRR\002IQR\002IER\002IMR\002ILR\002ITR\002JMR\002JPR\002JER\002JOR\002KZR\002KER\002KIR\002KPR\002KRR\002KWR\002KGR\002LAR\002LVR\002LBR\002LSR\002LRR\002LYR\002LIR\002LTR\002LUR\002MOR\002MKR\002MGR\002MWR\002MYR\002MVR\002MLR\002MTR\002MHR\002MQR\002MRR\002MUR\002YTR\002MXR\002FMR\002MDR\002MCR\002MNR\002MER\002MSR\002MAR\002MZR\002MMR\002NAR\002NRR\002NPR\002NLR\002NCR\002NZR\002NIR\002NER\002NGR\002NUR\002NFR\002MPR\002NOR\002OMR\002PKR\002PWR\002PSR\002PAR\002PGR\002PYR\002PER\002PHR\002PNR\002PLR\002PTR\002PRR\002QAR\002RER\002ROR\002RUR\002RWR\002BLR\002SHR\002KNR\002LCR\002MFR\002PMR\002VCR\002WSR\002SMR\002STR\002SAR\002SNR\002RSR\002SCR\002SLR\002SGR\002SXR\002SKR\002SIR\002SBR\002SOR\002ZAR\002GSR\002SSR\002ESR\002LKR\002SDR\002SRR\002SJR\002SZR\002SER\002CHR\002SYR\002TWR\002TJR\002TZR\002THR\002TLR\002TGR\002TKR\002TOR\002TTR\002TNR\002TRR\002TMR\002TCR\002TVR\002UGR\002UAR\002AER\002GBR\002USR\002UMR\002UYR\002UZR\002VUR\002VER\002VNR\002VGR\002VIR\002WFR\002EHR\002YER\002ZMR\002ZW'
  _globals['_POSTALADDRESS'].fields_by_name['address_locality']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['address_locality']._serialized_options = b'\372B\005r\003\030\376\001'
  _globals['_POSTALADDRESS'].fields_by_name['address_region']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['address_region']._serialized_options = b'\372B\005r\003\030\376\001'
  _globals['_POSTALADDRESS'].fields_by_name['post_office_box_number']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['post_office_box_number']._serialized_options = b'\372B\004r\002\0302'
  _globals['_POSTALADDRESS'].fields_by_name['postal_code']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['postal_code']._serialized_options = b'\372B\004r\002\0302'
  _globals['_POSTALADDRESS'].fields_by_name['street_address']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['street_address']._serialized_options = b'\372B\005r\003\030\376\001'
  _globals['_POSTALADDRESS'].fields_by_name['formatted']._loaded_options = None
  _globals['_POSTALADDRESS'].fields_by_name['formatted']._serialized_options = b'\372B\005r\003\030\200\010'
  _globals['_DIGITALTWINSTATE']._serialized_start=6036
  _globals['_DIGITALTWINSTATE']._serialized_end=6184
  _globals['_DIGITALTWINKIND']._serialized_start=6187
  _globals['_DIGITALTWINKIND']._serialized_end=6325
  _globals['_ERRORCODE']._serialized_start=6327
  _globals['_ERRORCODE']._serialized_end=6423
  _globals['_INVITATIONSTATE']._serialized_start=6426
  _globals['_INVITATIONSTATE']._serialized_end=6628
  _globals['_PROVIDERTYPE']._serialized_start=6631
  _globals['_PROVIDERTYPE']._serialized_end=6800
  _globals['_DIGITALTWIN']._serialized_start=240
  _globals['_DIGITALTWIN']._serialized_end=514
  _globals['_DIGITALENTITY']._serialized_start=517
  _globals['_DIGITALENTITY']._serialized_end=737
  _globals['_ERRORMESSAGE']._serialized_start=740
  _globals['_ERRORMESSAGE']._serialized_end=886
  _globals['_INVITATION']._serialized_start=889
  _globals['_INVITATION']._serialized_end=1380
  _globals['_WELLKNOWN']._serialized_start=1383
  _globals['_WELLKNOWN']._serialized_end=2859
  _globals['_OAUTH2TOKENRESPONSE']._serialized_start=2862
  _globals['_OAUTH2TOKENRESPONSE']._serialized_end=3066
  _globals['_FLUSHINACTIVEOAUTH2TOKENSREQUEST']._serialized_start=3068
  _globals['_FLUSHINACTIVEOAUTH2TOKENSREQUEST']._serialized_end=3131
  _globals['_IDENTITYTOKENINFO']._serialized_start=3134
  _globals['_IDENTITYTOKENINFO']._serialized_end=3800
  _globals['_PROVIDERINFO']._serialized_start=3802
  _globals['_PROVIDERINFO']._serialized_end=3901
  _globals['_USERINFORESPONSEPAYLOAD']._serialized_start=3904
  _globals['_USERINFORESPONSEPAYLOAD']._serialized_end=4502
  _globals['_POSTALADDRESS']._serialized_start=4505
  _globals['_POSTALADDRESS']._serialized_end=6033
# @@protoc_insertion_point(module_scope)
