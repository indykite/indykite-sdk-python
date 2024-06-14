# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/identity/v1beta2/import.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as indykite_dot_identity_dot_v1beta2_dot_attributes__pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as indykite_dot_identity_dot_v1beta2_dot_model__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&indykite/identity/v1beta2/import.proto\x12\x19indykite.identity.v1beta2\x1a*indykite/identity/v1beta2/attributes.proto\x1a%indykite/identity/v1beta2/model.proto\x1a\x17validate/validate.proto\"\xf0\x07\n\x19ImportDigitalTwinsRequest\x12\\\n\x08\x65ntities\x18\x01 \x03(\x0b\x32,.indykite.identity.v1beta2.ImportDigitalTwinB\x12\xfa\x42\x0f\x92\x01\x0c\x08\x01\x10\xe8\x07\"\x05\x8a\x01\x02\x10\x01R\x08\x65ntities\x12;\n\x06\x62\x63rypt\x18\x02 \x01(\x0b\x32!.indykite.identity.v1beta2.BcryptH\x00R\x06\x62\x63rypt\x12T\n\x0fstandard_scrypt\x18\x03 \x01(\x0b\x32).indykite.identity.v1beta2.StandardScryptH\x00R\x0estandardScrypt\x12;\n\x06scrypt\x18\x04 \x01(\x0b\x32!.indykite.identity.v1beta2.ScryptH\x00R\x06scrypt\x12?\n\x08hmac_md5\x18\x05 \x01(\x0b\x32\".indykite.identity.v1beta2.HMACMD5H\x00R\x07hmacMd5\x12\x42\n\thmac_sha1\x18\x06 \x01(\x0b\x32#.indykite.identity.v1beta2.HMACSHA1H\x00R\x08hmacSha1\x12H\n\x0bhmac_sha512\x18\x07 \x01(\x0b\x32%.indykite.identity.v1beta2.HMACSHA512H\x00R\nhmacSha512\x12H\n\x0bhmac_sha256\x18\x08 \x01(\x0b\x32%.indykite.identity.v1beta2.HMACSHA256H\x00R\nhmacSha256\x12\x32\n\x03md5\x18\t \x01(\x0b\x32\x1e.indykite.identity.v1beta2.MD5H\x00R\x03md5\x12N\n\rpbkdf2_sha256\x18\n \x01(\x0b\x32\'.indykite.identity.v1beta2.PBKDF2SHA256H\x00R\x0cpbkdf2Sha256\x12\x45\n\npbkdf_sha1\x18\x0b \x01(\x0b\x32$.indykite.identity.v1beta2.PBKDFSHA1H\x00R\tpbkdfSha1\x12\x35\n\x04sha1\x18\x0c \x01(\x0b\x32\x1f.indykite.identity.v1beta2.SHA1H\x00R\x04sha1\x12;\n\x06sha256\x18\r \x01(\x0b\x32!.indykite.identity.v1beta2.SHA256H\x00R\x06sha256\x12;\n\x06sha512\x18\x0e \x01(\x0b\x32!.indykite.identity.v1beta2.SHA512H\x00R\x06sha512B\x10\n\x0ehash_algorithm\"\xb0\x01\n\x18ImportDigitalTwinSuccess\x12I\n\x0c\x64igital_twin\x18\x01 \x01(\x0b\x32&.indykite.identity.v1beta2.DigitalTwinR\x0b\x64igitalTwin\x12I\n\x07results\x18\x02 \x03(\x0b\x32/.indykite.identity.v1beta2.BatchOperationResultR\x07results\"2\n\x16ImportDigitalTwinError\x12\x18\n\x07message\x18\x01 \x03(\tR\x07message\"\xda\x01\n\x17ImportDigitalTwinResult\x12\x14\n\x05index\x18\x01 \x01(\x04R\x05index\x12O\n\x07success\x18\x02 \x01(\x0b\x32\x33.indykite.identity.v1beta2.ImportDigitalTwinSuccessH\x00R\x07success\x12I\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x31.indykite.identity.v1beta2.ImportDigitalTwinErrorH\x00R\x05\x65rrorB\r\n\x06result\x12\x03\xf8\x42\x01\"j\n\x1aImportDigitalTwinsResponse\x12L\n\x07results\x18\x01 \x03(\x0b\x32\x32.indykite.identity.v1beta2.ImportDigitalTwinResultR\x07results\"\xb4\x05\n\x11ImportDigitalTwin\x12\x39\n\x02id\x18\x01 \x01(\tB)\xfa\x42&r$\x10\x1b\x18\x64\x32\x1b^gid:[A-Za-z0-9-_]{27,100}$\xd0\x01\x01R\x02id\x12\x46\n\ttenant_id\x18\x02 \x01(\tB)\xfa\x42&r$\x10\x1b\x18\x64\x32\x1b^gid:[A-Za-z0-9-_]{27,100}$\xd0\x01\x01R\x08tenantId\x12L\n\x04kind\x18\x03 \x01(\x0e\x32*.indykite.identity.v1beta2.DigitalTwinKindB\x0c\xfa\x42\t\x82\x01\x06\x10\x01\x18\x01\x18\x03R\x04kind\x12O\n\x05state\x18\x04 \x01(\x0e\x32+.indykite.identity.v1beta2.DigitalTwinStateB\x0c\xfa\x42\t\x82\x01\x06\x10\x01\x18\x01\x18\x02R\x05state\x12\x36\n\x04tags\x18\x05 \x03(\tB\"\xfa\x42\x1f\x92\x01\x1c\x10 \x18\x01\"\x16r\x14\x18@2\x10^([A-Z][a-z]+)+$R\x04tags\x12I\n\x08password\x18\x06 \x01(\x0b\x32-.indykite.identity.v1beta2.PasswordCredentialR\x08password\x12h\n\x12provider_user_info\x18\x07 \x03(\x0b\x32\'.indykite.identity.v1beta2.UserProviderB\x11\xfa\x42\x0e\x92\x01\x0b\x08\x00\x10\n\"\x05\x8a\x01\x02\x10\x01R\x10providerUserInfo\x12K\n\nproperties\x18\x08 \x01(\x0b\x32+.indykite.identity.v1beta2.ImportPropertiesR\nproperties\x12\x43\n\x08metadata\x18\t \x01(\x0b\x32\'.indykite.identity.v1beta2.UserMetadataR\x08metadata\"\x99\x01\n\x10ImportProperties\x12\x62\n\noperations\x18\x02 \x03(\x0b\x32\x31.indykite.identity.v1beta2.PropertyBatchOperationB\x0f\xfa\x42\x0c\x92\x01\t\x08\x01\"\x05\x8a\x01\x02\x10\x01R\noperations\x12!\n\x0c\x66orce_delete\x18\x04 \x01(\x08R\x0b\x66orceDelete\"\xa6\x01\n\x0cUserMetadata\x12-\n\x12\x63reation_timestamp\x18\x01 \x01(\x03R\x11\x63reationTimestamp\x12\x31\n\x15last_log_in_timestamp\x18\x02 \x01(\x03R\x12lastLogInTimestamp\x12\x34\n\x16last_refresh_timestamp\x18\x03 \x01(\x03R\x14lastRefreshTimestamp\"\\\n\x13\x43redentialReference\x12)\n\x0bprovider_id\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\x18\x80\x08R\nproviderId\x12\x1a\n\x03uid\x18\x02 \x01(\tB\x08\xfa\x42\x05r\x03\x18\x80\x08R\x03uid\"\x97\x01\n\x0cUserProvider\x12\x10\n\x03uid\x18\x01 \x01(\tR\x03uid\x12\x1f\n\x0bprovider_id\x18\x02 \x01(\tR\nproviderId\x12\x14\n\x05\x65mail\x18\x03 \x01(\tR\x05\x65mail\x12!\n\x0c\x64isplay_name\x18\x04 \x01(\tR\x0b\x64isplayName\x12\x1b\n\tphoto_url\x18\x05 \x01(\tR\x08photoUrl\"9\n\x05\x45mail\x12\x14\n\x05\x65mail\x18\x01 \x01(\tR\x05\x65mail\x12\x1a\n\x08verified\x18\x02 \x01(\x08R\x08verified\"^\n\x06Mobile\x12\x38\n\x06mobile\x18\x01 \x01(\tB \xfa\x42\x1dr\x1b\x32\x16^+.*[0-9A-Za-z]{7,16}$\xd0\x01\x01R\x06mobile\x12\x1a\n\x08verified\x18\x02 \x01(\x08R\x08verified\"\x93\x02\n\x12PasswordCredential\x12\x38\n\x05\x65mail\x18\x01 \x01(\x0b\x32 .indykite.identity.v1beta2.EmailH\x00R\x05\x65mail\x12;\n\x06mobile\x18\x02 \x01(\x0b\x32!.indykite.identity.v1beta2.MobileH\x00R\x06mobile\x12\x1c\n\x08username\x18\x03 \x01(\tH\x00R\x08username\x12\x16\n\x05value\x18\x04 \x01(\tH\x01R\x05value\x12=\n\x04hash\x18\x05 \x01(\x0b\x32\'.indykite.identity.v1beta2.PasswordHashH\x01R\x04hashB\x05\n\x03uidB\n\n\x08password\"G\n\x0cPasswordHash\x12#\n\rpassword_hash\x18\x04 \x01(\x0cR\x0cpasswordHash\x12\x12\n\x04salt\x18\x05 \x01(\x0cR\x04salt\"\x08\n\x06\x42\x63rypt\"\xa8\x01\n\x0eStandardScrypt\x12\x1d\n\nblock_size\x18\x01 \x01(\x03R\tblockSize\x12,\n\x12\x64\x65rived_key_length\x18\x02 \x01(\x03R\x10\x64\x65rivedKeyLength\x12\x1f\n\x0bmemory_cost\x18\x03 \x01(\x03R\nmemoryCost\x12(\n\x0fparallelization\x18\x04 \x01(\x03R\x0fparallelization\"z\n\x06Scrypt\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03key\x12%\n\x0esalt_separator\x18\x02 \x01(\x0cR\rsaltSeparator\x12\x16\n\x06rounds\x18\x03 \x01(\x03R\x06rounds\x12\x1f\n\x0bmemory_cost\x18\x04 \x01(\x03R\nmemoryCost\"\x1b\n\x07HMACMD5\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03key\"\x1c\n\x08HMACSHA1\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03key\"\x1e\n\nHMACSHA512\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03key\"\x1e\n\nHMACSHA256\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03key\"\x1d\n\x03MD5\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06rounds\"&\n\x0cPBKDF2SHA256\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06rounds\"#\n\tPBKDFSHA1\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06rounds\"\x1e\n\x04SHA1\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06rounds\" \n\x06SHA256\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06rounds\" \n\x06SHA512\x12\x16\n\x06rounds\x18\x01 \x01(\x03R\x06roundsB\xb2\x01\n\x1d\x63om.indykite.identity.v1beta2B\x0bImportProtoP\x01\xa2\x02\x03IIX\xaa\x02\x19Indykite.Identity.V1beta2\xca\x02\x19Indykite\\Identity\\V1beta2\xe2\x02%Indykite\\Identity\\V1beta2\\GPBMetadata\xea\x02\x1bIndykite::Identity::V1beta2b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.identity.v1beta2.import_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\035com.indykite.identity.v1beta2B\013ImportProtoP\001\242\002\003IIX\252\002\031Indykite.Identity.V1beta2\312\002\031Indykite\\Identity\\V1beta2\342\002%Indykite\\Identity\\V1beta2\\GPBMetadata\352\002\033Indykite::Identity::V1beta2'
  _globals['_IMPORTDIGITALTWINSREQUEST'].fields_by_name['entities']._loaded_options = None
  _globals['_IMPORTDIGITALTWINSREQUEST'].fields_by_name['entities']._serialized_options = b'\372B\017\222\001\014\010\001\020\350\007\"\005\212\001\002\020\001'
  _globals['_IMPORTDIGITALTWINRESULT'].oneofs_by_name['result']._loaded_options = None
  _globals['_IMPORTDIGITALTWINRESULT'].oneofs_by_name['result']._serialized_options = b'\370B\001'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['id']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['id']._serialized_options = b'\372B&r$\020\033\030d2\033^gid:[A-Za-z0-9-_]{27,100}$\320\001\001'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['tenant_id']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['tenant_id']._serialized_options = b'\372B&r$\020\033\030d2\033^gid:[A-Za-z0-9-_]{27,100}$\320\001\001'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['kind']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['kind']._serialized_options = b'\372B\t\202\001\006\020\001\030\001\030\003'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['state']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['state']._serialized_options = b'\372B\t\202\001\006\020\001\030\001\030\002'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['tags']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['tags']._serialized_options = b'\372B\037\222\001\034\020 \030\001\"\026r\024\030@2\020^([A-Z][a-z]+)+$'
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['provider_user_info']._loaded_options = None
  _globals['_IMPORTDIGITALTWIN'].fields_by_name['provider_user_info']._serialized_options = b'\372B\016\222\001\013\010\000\020\n\"\005\212\001\002\020\001'
  _globals['_IMPORTPROPERTIES'].fields_by_name['operations']._loaded_options = None
  _globals['_IMPORTPROPERTIES'].fields_by_name['operations']._serialized_options = b'\372B\014\222\001\t\010\001\"\005\212\001\002\020\001'
  _globals['_CREDENTIALREFERENCE'].fields_by_name['provider_id']._loaded_options = None
  _globals['_CREDENTIALREFERENCE'].fields_by_name['provider_id']._serialized_options = b'\372B\005r\003\030\200\010'
  _globals['_CREDENTIALREFERENCE'].fields_by_name['uid']._loaded_options = None
  _globals['_CREDENTIALREFERENCE'].fields_by_name['uid']._serialized_options = b'\372B\005r\003\030\200\010'
  _globals['_MOBILE'].fields_by_name['mobile']._loaded_options = None
  _globals['_MOBILE'].fields_by_name['mobile']._serialized_options = b'\372B\035r\0332\026^+.*[0-9A-Za-z]{7,16}$\320\001\001'
  _globals['_IMPORTDIGITALTWINSREQUEST']._serialized_start=178
  _globals['_IMPORTDIGITALTWINSREQUEST']._serialized_end=1186
  _globals['_IMPORTDIGITALTWINSUCCESS']._serialized_start=1189
  _globals['_IMPORTDIGITALTWINSUCCESS']._serialized_end=1365
  _globals['_IMPORTDIGITALTWINERROR']._serialized_start=1367
  _globals['_IMPORTDIGITALTWINERROR']._serialized_end=1417
  _globals['_IMPORTDIGITALTWINRESULT']._serialized_start=1420
  _globals['_IMPORTDIGITALTWINRESULT']._serialized_end=1638
  _globals['_IMPORTDIGITALTWINSRESPONSE']._serialized_start=1640
  _globals['_IMPORTDIGITALTWINSRESPONSE']._serialized_end=1746
  _globals['_IMPORTDIGITALTWIN']._serialized_start=1749
  _globals['_IMPORTDIGITALTWIN']._serialized_end=2441
  _globals['_IMPORTPROPERTIES']._serialized_start=2444
  _globals['_IMPORTPROPERTIES']._serialized_end=2597
  _globals['_USERMETADATA']._serialized_start=2600
  _globals['_USERMETADATA']._serialized_end=2766
  _globals['_CREDENTIALREFERENCE']._serialized_start=2768
  _globals['_CREDENTIALREFERENCE']._serialized_end=2860
  _globals['_USERPROVIDER']._serialized_start=2863
  _globals['_USERPROVIDER']._serialized_end=3014
  _globals['_EMAIL']._serialized_start=3016
  _globals['_EMAIL']._serialized_end=3073
  _globals['_MOBILE']._serialized_start=3075
  _globals['_MOBILE']._serialized_end=3169
  _globals['_PASSWORDCREDENTIAL']._serialized_start=3172
  _globals['_PASSWORDCREDENTIAL']._serialized_end=3447
  _globals['_PASSWORDHASH']._serialized_start=3449
  _globals['_PASSWORDHASH']._serialized_end=3520
  _globals['_BCRYPT']._serialized_start=3522
  _globals['_BCRYPT']._serialized_end=3530
  _globals['_STANDARDSCRYPT']._serialized_start=3533
  _globals['_STANDARDSCRYPT']._serialized_end=3701
  _globals['_SCRYPT']._serialized_start=3703
  _globals['_SCRYPT']._serialized_end=3825
  _globals['_HMACMD5']._serialized_start=3827
  _globals['_HMACMD5']._serialized_end=3854
  _globals['_HMACSHA1']._serialized_start=3856
  _globals['_HMACSHA1']._serialized_end=3884
  _globals['_HMACSHA512']._serialized_start=3886
  _globals['_HMACSHA512']._serialized_end=3916
  _globals['_HMACSHA256']._serialized_start=3918
  _globals['_HMACSHA256']._serialized_end=3948
  _globals['_MD5']._serialized_start=3950
  _globals['_MD5']._serialized_end=3979
  _globals['_PBKDF2SHA256']._serialized_start=3981
  _globals['_PBKDF2SHA256']._serialized_end=4019
  _globals['_PBKDFSHA1']._serialized_start=4021
  _globals['_PBKDFSHA1']._serialized_end=4056
  _globals['_SHA1']._serialized_start=4058
  _globals['_SHA1']._serialized_end=4088
  _globals['_SHA256']._serialized_start=4090
  _globals['_SHA256']._serialized_end=4122
  _globals['_SHA512']._serialized_start=4124
  _globals['_SHA512']._serialized_end=4156
# @@protoc_insertion_point(module_scope)
