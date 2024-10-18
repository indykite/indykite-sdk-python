# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/ingest/v1beta3/ingest_api.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2 as indykite_dot_ingest_dot_v1beta3_dot_model__pb2
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2 as indykite_dot_knowledge_dot_objects_dot_v1beta1_dot_ikg__pb2
from indykite_sdk.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(indykite/ingest/v1beta3/ingest_api.proto\x12\x17indykite.ingest.v1beta3\x1a\x17google/rpc/status.proto\x1a#indykite/ingest/v1beta3/model.proto\x1a,indykite/knowledge/objects/v1beta1/ikg.proto\x1a\x17validate/validate.proto\"f\n\x17\x42\x61tchUpsertNodesRequest\x12K\n\x05nodes\x18\x01 \x03(\x0b\x32(.indykite.knowledge.objects.v1beta1.NodeB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\x05nodes\"S\n\x18\x42\x61tchUpsertNodesResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"{\n\x1f\x42\x61tchUpsertRelationshipsRequest\x12X\n\rrelationships\x18\x01 \x03(\x0b\x32%.indykite.ingest.v1beta3.RelationshipB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\rrelationships\"[\n BatchUpsertRelationshipsResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"`\n\x17\x42\x61tchDeleteNodesRequest\x12\x45\n\x05nodes\x18\x01 \x03(\x0b\x32\".indykite.ingest.v1beta3.NodeMatchB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\x05nodes\"S\n\x18\x42\x61tchDeleteNodesResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"{\n\x1f\x42\x61tchDeleteRelationshipsRequest\x12X\n\rrelationships\x18\x01 \x03(\x0b\x32%.indykite.ingest.v1beta3.RelationshipB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\rrelationships\"[\n BatchDeleteRelationshipsResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"\x8f\x01\n BatchDeleteNodePropertiesRequest\x12k\n\x0fnode_properties\x18\x01 \x03(\x0b\x32\x35.indykite.ingest.v1beta3.DeleteData.NodePropertyMatchB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\x0enodeProperties\"\\\n!BatchDeleteNodePropertiesResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"\xb0\x01\n(BatchDeleteRelationshipPropertiesRequest\x12\x83\x01\n\x17relationship_properties\x18\x01 \x03(\x0b\x32=.indykite.ingest.v1beta3.DeleteData.RelationshipPropertyMatchB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\x16relationshipProperties\"d\n)BatchDeleteRelationshipPropertiesResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"x\n\x1a\x42\x61tchDeleteNodeTagsRequest\x12Z\n\tnode_tags\x18\x01 \x03(\x0b\x32\x30.indykite.ingest.v1beta3.DeleteData.NodeTagMatchB\x0b\xfa\x42\x08\x92\x01\x05\x08\x01\x10\xfa\x01R\x08nodeTags\"V\n\x1b\x42\x61tchDeleteNodeTagsResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x07results\"Y\n\x14StreamRecordsRequest\x12\x41\n\x06record\x18\x01 \x01(\x0b\x32\x1f.indykite.ingest.v1beta3.RecordB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x06record\"\x97\x02\n\x15StreamRecordsResponse\x12\x1b\n\trecord_id\x18\x01 \x01(\tR\x08recordId\x12!\n\x0crecord_index\x18\x02 \x01(\rR\x0brecordIndex\x12I\n\x0crecord_error\x18\x03 \x01(\x0b\x32$.indykite.ingest.v1beta3.RecordErrorH\x00R\x0brecordError\x12\x37\n\x0cstatus_error\x18\x04 \x01(\x0b\x32\x12.google.rpc.StatusH\x00R\x0bstatusError\x12\x31\n\x04info\x18\x05 \x01(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x04infoB\x07\n\x05\x65rror\"X\n\x13IngestRecordRequest\x12\x41\n\x06record\x18\x01 \x01(\x0b\x32\x1f.indykite.ingest.v1beta3.RecordB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x06record\"f\n\x14IngestRecordResponse\x12\x1b\n\trecord_id\x18\x01 \x01(\tR\x08recordId\x12\x31\n\x04info\x18\x05 \x01(\x0b\x32\x1d.indykite.ingest.v1beta3.InfoR\x04info2\xcc\t\n\tIngestAPI\x12r\n\rStreamRecords\x12-.indykite.ingest.v1beta3.StreamRecordsRequest\x1a..indykite.ingest.v1beta3.StreamRecordsResponse(\x01\x30\x01\x12p\n\x0cIngestRecord\x12,.indykite.ingest.v1beta3.IngestRecordRequest\x1a-.indykite.ingest.v1beta3.IngestRecordResponse\"\x03\x88\x02\x01\x12w\n\x10\x42\x61tchUpsertNodes\x12\x30.indykite.ingest.v1beta3.BatchUpsertNodesRequest\x1a\x31.indykite.ingest.v1beta3.BatchUpsertNodesResponse\x12\x8f\x01\n\x18\x42\x61tchUpsertRelationships\x12\x38.indykite.ingest.v1beta3.BatchUpsertRelationshipsRequest\x1a\x39.indykite.ingest.v1beta3.BatchUpsertRelationshipsResponse\x12w\n\x10\x42\x61tchDeleteNodes\x12\x30.indykite.ingest.v1beta3.BatchDeleteNodesRequest\x1a\x31.indykite.ingest.v1beta3.BatchDeleteNodesResponse\x12\x8f\x01\n\x18\x42\x61tchDeleteRelationships\x12\x38.indykite.ingest.v1beta3.BatchDeleteRelationshipsRequest\x1a\x39.indykite.ingest.v1beta3.BatchDeleteRelationshipsResponse\x12\x92\x01\n\x19\x42\x61tchDeleteNodeProperties\x12\x39.indykite.ingest.v1beta3.BatchDeleteNodePropertiesRequest\x1a:.indykite.ingest.v1beta3.BatchDeleteNodePropertiesResponse\x12\xaa\x01\n!BatchDeleteRelationshipProperties\x12\x41.indykite.ingest.v1beta3.BatchDeleteRelationshipPropertiesRequest\x1a\x42.indykite.ingest.v1beta3.BatchDeleteRelationshipPropertiesResponse\x12\x80\x01\n\x13\x42\x61tchDeleteNodeTags\x12\x33.indykite.ingest.v1beta3.BatchDeleteNodeTagsRequest\x1a\x34.indykite.ingest.v1beta3.BatchDeleteNodeTagsResponseB\xab\x01\n\x1b\x63om.indykite.ingest.v1beta3B\x0eIngestApiProtoP\x01\xa2\x02\x03IIX\xaa\x02\x17Indykite.Ingest.V1beta3\xca\x02\x17Indykite\\Ingest\\V1beta3\xe2\x02#Indykite\\Ingest\\V1beta3\\GPBMetadata\xea\x02\x19Indykite::Ingest::V1beta3b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.ingest.v1beta3.ingest_api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\033com.indykite.ingest.v1beta3B\016IngestApiProtoP\001\242\002\003IIX\252\002\027Indykite.Ingest.V1beta3\312\002\027Indykite\\Ingest\\V1beta3\342\002#Indykite\\Ingest\\V1beta3\\GPBMetadata\352\002\031Indykite::Ingest::V1beta3'
  _globals['_BATCHUPSERTNODESREQUEST'].fields_by_name['nodes']._loaded_options = None
  _globals['_BATCHUPSERTNODESREQUEST'].fields_by_name['nodes']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHUPSERTRELATIONSHIPSREQUEST'].fields_by_name['relationships']._loaded_options = None
  _globals['_BATCHUPSERTRELATIONSHIPSREQUEST'].fields_by_name['relationships']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHDELETENODESREQUEST'].fields_by_name['nodes']._loaded_options = None
  _globals['_BATCHDELETENODESREQUEST'].fields_by_name['nodes']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHDELETERELATIONSHIPSREQUEST'].fields_by_name['relationships']._loaded_options = None
  _globals['_BATCHDELETERELATIONSHIPSREQUEST'].fields_by_name['relationships']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHDELETENODEPROPERTIESREQUEST'].fields_by_name['node_properties']._loaded_options = None
  _globals['_BATCHDELETENODEPROPERTIESREQUEST'].fields_by_name['node_properties']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESREQUEST'].fields_by_name['relationship_properties']._loaded_options = None
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESREQUEST'].fields_by_name['relationship_properties']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_BATCHDELETENODETAGSREQUEST'].fields_by_name['node_tags']._loaded_options = None
  _globals['_BATCHDELETENODETAGSREQUEST'].fields_by_name['node_tags']._serialized_options = b'\372B\010\222\001\005\010\001\020\372\001'
  _globals['_STREAMRECORDSREQUEST'].fields_by_name['record']._loaded_options = None
  _globals['_STREAMRECORDSREQUEST'].fields_by_name['record']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_INGESTRECORDREQUEST'].fields_by_name['record']._loaded_options = None
  _globals['_INGESTRECORDREQUEST'].fields_by_name['record']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_INGESTAPI'].methods_by_name['IngestRecord']._loaded_options = None
  _globals['_INGESTAPI'].methods_by_name['IngestRecord']._serialized_options = b'\210\002\001'
  _globals['_BATCHUPSERTNODESREQUEST']._serialized_start=202
  _globals['_BATCHUPSERTNODESREQUEST']._serialized_end=304
  _globals['_BATCHUPSERTNODESRESPONSE']._serialized_start=306
  _globals['_BATCHUPSERTNODESRESPONSE']._serialized_end=389
  _globals['_BATCHUPSERTRELATIONSHIPSREQUEST']._serialized_start=391
  _globals['_BATCHUPSERTRELATIONSHIPSREQUEST']._serialized_end=514
  _globals['_BATCHUPSERTRELATIONSHIPSRESPONSE']._serialized_start=516
  _globals['_BATCHUPSERTRELATIONSHIPSRESPONSE']._serialized_end=607
  _globals['_BATCHDELETENODESREQUEST']._serialized_start=609
  _globals['_BATCHDELETENODESREQUEST']._serialized_end=705
  _globals['_BATCHDELETENODESRESPONSE']._serialized_start=707
  _globals['_BATCHDELETENODESRESPONSE']._serialized_end=790
  _globals['_BATCHDELETERELATIONSHIPSREQUEST']._serialized_start=792
  _globals['_BATCHDELETERELATIONSHIPSREQUEST']._serialized_end=915
  _globals['_BATCHDELETERELATIONSHIPSRESPONSE']._serialized_start=917
  _globals['_BATCHDELETERELATIONSHIPSRESPONSE']._serialized_end=1008
  _globals['_BATCHDELETENODEPROPERTIESREQUEST']._serialized_start=1011
  _globals['_BATCHDELETENODEPROPERTIESREQUEST']._serialized_end=1154
  _globals['_BATCHDELETENODEPROPERTIESRESPONSE']._serialized_start=1156
  _globals['_BATCHDELETENODEPROPERTIESRESPONSE']._serialized_end=1248
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESREQUEST']._serialized_start=1251
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESREQUEST']._serialized_end=1427
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESRESPONSE']._serialized_start=1429
  _globals['_BATCHDELETERELATIONSHIPPROPERTIESRESPONSE']._serialized_end=1529
  _globals['_BATCHDELETENODETAGSREQUEST']._serialized_start=1531
  _globals['_BATCHDELETENODETAGSREQUEST']._serialized_end=1651
  _globals['_BATCHDELETENODETAGSRESPONSE']._serialized_start=1653
  _globals['_BATCHDELETENODETAGSRESPONSE']._serialized_end=1739
  _globals['_STREAMRECORDSREQUEST']._serialized_start=1741
  _globals['_STREAMRECORDSREQUEST']._serialized_end=1830
  _globals['_STREAMRECORDSRESPONSE']._serialized_start=1833
  _globals['_STREAMRECORDSRESPONSE']._serialized_end=2112
  _globals['_INGESTRECORDREQUEST']._serialized_start=2114
  _globals['_INGESTRECORDREQUEST']._serialized_end=2202
  _globals['_INGESTRECORDRESPONSE']._serialized_start=2204
  _globals['_INGESTRECORDRESPONSE']._serialized_end=2306
  _globals['_INGESTAPI']._serialized_start=2309
  _globals['_INGESTAPI']._serialized_end=3537
# @@protoc_insertion_point(module_scope)
