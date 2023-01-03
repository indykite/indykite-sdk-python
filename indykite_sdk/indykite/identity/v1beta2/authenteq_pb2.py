# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/identity/v1beta2/authenteq.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)indykite/identity/v1beta2/authenteq.proto\x12\x19indykite.identity.v1beta2\"y\n\x10\x41uthenteqDetails\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12U\n\rdocument_data\x18\x04 \x01(\x0b\x32\x30.indykite.identity.v1beta2.AuthenteqDocumentDataR\x0c\x64ocumentData\"\x98\x08\n\x15\x41uthenteqDocumentData\x12#\n\rdocument_type\x18\x01 \x01(\tR\x0c\x64ocumentType\x12\'\n\x0f\x64ocument_number\x18\x02 \x01(\tR\x0e\x64ocumentNumber\x12\'\n\x0fissuing_country\x18\x03 \x01(\tR\x0eissuingCountry\x12\"\n\x0cjurisdiction\x18\x04 \x01(\tR\x0cjurisdiction\x12 \n\x0bnationality\x18\x05 \x01(\tR\x0bnationality\x12\x35\n\x17surname_and_given_names\x18\x06 \x01(\tR\x14surnameAndGivenNames\x12\x18\n\x07surname\x18\x07 \x01(\tR\x07surname\x12\x1f\n\x0bgiven_names\x18\x08 \x01(\tR\ngivenNames\x12#\n\rname_suffixes\x18\t \x01(\tR\x0cnameSuffixes\x12#\n\rname_prefixes\x18\n \x01(\tR\x0cnamePrefixes\x12\x10\n\x03sex\x18\x0b \x01(\tR\x03sex\x12\"\n\rdate_of_birth\x18\x0c \x01(\tR\x0b\x64\x61teOfBirth\x12$\n\x0e\x64\x61te_of_expiry\x18\r \x01(\tR\x0c\x64\x61teOfExpiry\x12\"\n\rdate_of_issue\x18\x0e \x01(\tR\x0b\x64\x61teOfIssue\x12#\n\rlicense_class\x18\x0f \x01(\tR\x0clicenseClass\x12}\n\x15license_class_details\x18\x10 \x03(\x0b\x32I.indykite.identity.v1beta2.AuthenteqDocumentData.LicenseClassDetailsEntryR\x13licenseClassDetails\x12S\n\x13\x63ropped_front_image\x18\x11 \x01(\x0b\x32#.indykite.identity.v1beta2.WebImageR\x11\x63roppedFrontImage\x12Q\n\x12\x63ropped_back_image\x18\x12 \x01(\x0b\x32#.indykite.identity.v1beta2.WebImageR\x10\x63roppedBackImage\x12\x42\n\nface_image\x18\x13 \x01(\x0b\x32#.indykite.identity.v1beta2.WebImageR\tfaceImage\x1av\n\x18LicenseClassDetailsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x44\n\x05value\x18\x02 \x01(\x0b\x32..indykite.identity.v1beta2.LicenseClassDetailsR\x05value:\x02\x38\x01\"O\n\x13LicenseClassDetails\x12\x12\n\x04\x66rom\x18\x01 \x01(\tR\x04\x66rom\x12\x0e\n\x02to\x18\x02 \x01(\tR\x02to\x12\x14\n\x05notes\x18\x03 \x01(\tR\x05notes\"G\n\x08WebImage\x12!\n\x0c\x63ontent_type\x18\x01 \x01(\tR\x0b\x63ontentType\x12\x18\n\x07\x63ontent\x18\x02 \x01(\tR\x07\x63ontentB\xb5\x01\n\x1d\x63om.indykite.identity.v1beta2B\x0e\x41uthenteqProtoP\x01\xa2\x02\x03IIX\xaa\x02\x19Indykite.Identity.V1beta2\xca\x02\x19Indykite\\Identity\\V1beta2\xe2\x02%Indykite\\Identity\\V1beta2\\GPBMetadata\xea\x02\x1bIndykite::Identity::V1beta2b\x06proto3')



_AUTHENTEQDETAILS = DESCRIPTOR.message_types_by_name['AuthenteqDetails']
_AUTHENTEQDOCUMENTDATA = DESCRIPTOR.message_types_by_name['AuthenteqDocumentData']
_AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY = _AUTHENTEQDOCUMENTDATA.nested_types_by_name['LicenseClassDetailsEntry']
_LICENSECLASSDETAILS = DESCRIPTOR.message_types_by_name['LicenseClassDetails']
_WEBIMAGE = DESCRIPTOR.message_types_by_name['WebImage']
AuthenteqDetails = _reflection.GeneratedProtocolMessageType('AuthenteqDetails', (_message.Message,), {
  'DESCRIPTOR' : _AUTHENTEQDETAILS,
  '__module__' : 'indykite.identity.v1beta2.authenteq_pb2'
  # @@protoc_insertion_point(class_scope:indykite.identity.v1beta2.AuthenteqDetails)
  })
_sym_db.RegisterMessage(AuthenteqDetails)

AuthenteqDocumentData = _reflection.GeneratedProtocolMessageType('AuthenteqDocumentData', (_message.Message,), {

  'LicenseClassDetailsEntry' : _reflection.GeneratedProtocolMessageType('LicenseClassDetailsEntry', (_message.Message,), {
    'DESCRIPTOR' : _AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY,
    '__module__' : 'indykite.identity.v1beta2.authenteq_pb2'
    # @@protoc_insertion_point(class_scope:indykite.identity.v1beta2.AuthenteqDocumentData.LicenseClassDetailsEntry)
    })
  ,
  'DESCRIPTOR' : _AUTHENTEQDOCUMENTDATA,
  '__module__' : 'indykite.identity.v1beta2.authenteq_pb2'
  # @@protoc_insertion_point(class_scope:indykite.identity.v1beta2.AuthenteqDocumentData)
  })
_sym_db.RegisterMessage(AuthenteqDocumentData)
_sym_db.RegisterMessage(AuthenteqDocumentData.LicenseClassDetailsEntry)

LicenseClassDetails = _reflection.GeneratedProtocolMessageType('LicenseClassDetails', (_message.Message,), {
  'DESCRIPTOR' : _LICENSECLASSDETAILS,
  '__module__' : 'indykite.identity.v1beta2.authenteq_pb2'
  # @@protoc_insertion_point(class_scope:indykite.identity.v1beta2.LicenseClassDetails)
  })
_sym_db.RegisterMessage(LicenseClassDetails)

WebImage = _reflection.GeneratedProtocolMessageType('WebImage', (_message.Message,), {
  'DESCRIPTOR' : _WEBIMAGE,
  '__module__' : 'indykite.identity.v1beta2.authenteq_pb2'
  # @@protoc_insertion_point(class_scope:indykite.identity.v1beta2.WebImage)
  })
_sym_db.RegisterMessage(WebImage)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.indykite.identity.v1beta2B\016AuthenteqProtoP\001\242\002\003IIX\252\002\031Indykite.Identity.V1beta2\312\002\031Indykite\\Identity\\V1beta2\342\002%Indykite\\Identity\\V1beta2\\GPBMetadata\352\002\033Indykite::Identity::V1beta2'
  _AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY._options = None
  _AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY._serialized_options = b'8\001'
  _AUTHENTEQDETAILS._serialized_start=72
  _AUTHENTEQDETAILS._serialized_end=193
  _AUTHENTEQDOCUMENTDATA._serialized_start=196
  _AUTHENTEQDOCUMENTDATA._serialized_end=1244
  _AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY._serialized_start=1126
  _AUTHENTEQDOCUMENTDATA_LICENSECLASSDETAILSENTRY._serialized_end=1244
  _LICENSECLASSDETAILS._serialized_start=1246
  _LICENSECLASSDETAILS._serialized_end=1325
  _WEBIMAGE._serialized_start=1327
  _WEBIMAGE._serialized_end=1398
# @@protoc_insertion_point(module_scope)