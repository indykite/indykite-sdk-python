# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indykite/auditsink/v1beta1/config.proto
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
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'indykite/auditsink/v1beta1/config.proto\x12\x1aindykite.auditsink.v1beta1\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\"i\n\x0e\x43ontainersPath\x12\x1f\n\x0b\x63ustomer_id\x18\x01 \x01(\tR\ncustomerId\x12\x30\n\x14\x61pplication_space_id\x18\x02 \x01(\tR\x12\x61pplicationSpaceIdJ\x04\x08\x03\x10\x04\"\x9a\x03\n\rCreatedConfig\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12:\n\x04type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\x12N\n\x08location\x18\x03 \x01(\x0b\x32\x32.indykite.auditsink.v1beta1.CreatedConfig.LocationR\x08location\x12S\n\x0f\x63ontainers_path\x18\x05 \x01(\x0b\x32*.indykite.auditsink.v1beta1.ContainersPathR\x0e\x63ontainersPath\x12@\n\x06\x64\x65tail\x18\x04 \x01(\x0b\x32(.indykite.auditsink.v1beta1.ConfigDetailR\x06\x64\x65tail\x1aV\n\x08Location\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12:\n\x04type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\"\xb6\x03\n\nReadConfig\x12\x10\n\x02id\x18\x01 \x01(\tH\x00R\x02id\x12K\n\x04name\x18\x02 \x01(\x0b\x32\x35.indykite.auditsink.v1beta1.ReadConfig.NameIdentifierH\x00R\x04name\x12S\n\x0f\x63ontainers_path\x18\x04 \x01(\x0b\x32*.indykite.auditsink.v1beta1.ContainersPathR\x0e\x63ontainersPath\x12:\n\x04type\x18\x03 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\x1a\xa9\x01\n\x0eNameIdentifier\x12\x1f\n\x0blocation_id\x18\x01 \x01(\tR\nlocationId\x12P\n\rlocation_type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeH\x00R\x0clocationType\x88\x01\x01\x12\x12\n\x04name\x18\x03 \x01(\tR\x04nameB\x10\n\x0e_location_typeB\x0c\n\nidentifier\"\xb2\x02\n\rUpdatedConfig\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12:\n\x04type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\x12S\n\x0f\x63ontainers_path\x18\x05 \x01(\x0b\x32*.indykite.auditsink.v1beta1.ContainersPathR\x0e\x63ontainersPath\x12@\n\x06\x62\x65\x66ore\x18\x03 \x01(\x0b\x32(.indykite.auditsink.v1beta1.ConfigDetailR\x06\x62\x65\x66ore\x12>\n\x05\x61\x66ter\x18\x04 \x01(\x0b\x32(.indykite.auditsink.v1beta1.ConfigDetailR\x05\x61\x66ter\"\xb0\x01\n\rDeletedConfig\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12:\n\x04type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\x04type\x12S\n\x0f\x63ontainers_path\x18\x03 \x01(\x0b\x32*.indykite.auditsink.v1beta1.ContainersPathR\x0e\x63ontainersPath\"\xb0\n\n\x0c\x43onfigDetail\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12!\n\x0c\x64isplay_name\x18\x02 \x01(\tR\x0b\x64isplayName\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x18\n\x07version\x18\x04 \x01(\x03R\x07version\x12\x80\x01\n\x1c\x61pplication_agent_credential\x18\x08 \x01(\x0b\x32<.indykite.auditsink.v1beta1.ApplicationAgentCredentialConfigH\x00R\x1a\x61pplicationAgentCredential\x12z\n\x1aservice_account_credential\x18\t \x01(\x0b\x32:.indykite.auditsink.v1beta1.ServiceAccountCredentialConfigH\x00R\x18serviceAccountCredential\x12Y\n\x11\x61udit_sink_config\x18\x0c \x01(\x0b\x32+.indykite.auditsink.v1beta1.AuditSinkConfigH\x00R\x0f\x61uditSinkConfig\x12w\n\x1b\x61uthorization_policy_config\x18\x0f \x01(\x0b\x32\x35.indykite.auditsink.v1beta1.AuthorizationPolicyConfigH\x00R\x19\x61uthorizationPolicyConfig\x12k\n\x17token_introspect_config\x18\x13 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.TokenIntrospectConfigH\x00R\x15tokenIntrospectConfig\x12{\n\x1d\x65xternal_data_resolver_config\x18\x16 \x01(\x0b\x32\x36.indykite.auditsink.v1beta1.ExternalDataResolverConfigH\x00R\x1a\x65xternalDataResolverConfig\x12r\n\x1atrust_score_profile_config\x18\x17 \x01(\x0b\x32\x33.indykite.auditsink.v1beta1.TrustScoreProfileConfigH\x00R\x17trustScoreProfileConfig\x12Y\n\x0e\x63onsent_config\x18\x12 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.ConsentConfigurationH\x00R\rconsentConfig\x12h\n\x16ingest_pipeline_config\x18\x14 \x01(\x0b\x32\x30.indykite.auditsink.v1beta1.IngestPipelineConfigH\x00R\x14ingestPipelineConfig\x12\x81\x01\n\x1f\x65ntity_matching_pipeline_config\x18\x15 \x01(\x0b\x32\x38.indykite.auditsink.v1beta1.EntityMatchingPipelineConfigH\x00R\x1c\x65ntityMatchingPipelineConfigB\x0f\n\rconfigurationJ\x04\x08\n\x10\x0bJ\x04\x08\x0b\x10\x0cJ\x04\x08\r\x10\x0eJ\x04\x08\x0e\x10\x0fJ\x04\x08\x10\x10\x11J\x04\x08\x11\x10\x12\"\xb3\x01\n ApplicationAgentCredentialConfig\x12\x10\n\x03kid\x18\x01 \x01(\tR\x03kid\x12\x1d\n\nkey_format\x18\x02 \x01(\tR\tkeyFormat\x12!\n\x0coriginal_kid\x18\x03 \x01(\tR\x0boriginalKid\x12;\n\x0b\x65xpire_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpireTime\"\xb1\x01\n\x1eServiceAccountCredentialConfig\x12\x10\n\x03kid\x18\x01 \x01(\tR\x03kid\x12\x1d\n\nkey_format\x18\x02 \x01(\tR\tkeyFormat\x12!\n\x0coriginal_kid\x18\x03 \x01(\tR\x0boriginalKid\x12;\n\x0b\x65xpire_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpireTime\"\xa3\x02\n\x0f\x41uditSinkConfig\x12I\n\x05kafka\x18\x01 \x01(\x0b\x32\x31.indykite.auditsink.v1beta1.AuditSinkConfig.KafkaH\x00R\x05kafka\x1a\xb8\x01\n\x05Kafka\x12\x18\n\x07\x62rokers\x18\x01 \x03(\tR\x07\x62rokers\x12\x14\n\x05topic\x18\x02 \x01(\tR\x05topic\x12\x1f\n\x0b\x64isable_tls\x18\x03 \x01(\x08R\ndisableTls\x12&\n\x0ftls_skip_verify\x18\x04 \x01(\x08R\rtlsSkipVerify\x12\x1a\n\x08username\x18\x05 \x01(\tR\x08username\x12\x1a\n\x08password\x18\x06 \x01(\tR\x08passwordB\n\n\x08provider\"\xc7\x04\n\x1a\x45xternalDataResolverConfig\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x16\n\x06method\x18\x02 \x01(\tR\x06method\x12]\n\x07headers\x18\x03 \x03(\x0b\x32\x43.indykite.auditsink.v1beta1.ExternalDataResolverConfig.HeadersEntryR\x07headers\x12\x65\n\x0crequest_type\x18\x04 \x01(\x0e\x32\x42.indykite.auditsink.v1beta1.ExternalDataResolverConfig.ContentTypeR\x0brequestType\x12\'\n\x0frequest_payload\x18\x05 \x01(\tR\x0erequestPayload\x12g\n\rresponse_type\x18\x06 \x01(\x0e\x32\x42.indykite.auditsink.v1beta1.ExternalDataResolverConfig.ContentTypeR\x0cresponseType\x12+\n\x11response_selector\x18\x07 \x01(\tR\x10responseSelector\x1a:\n\x0cHeadersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\">\n\x0b\x43ontentType\x12\x18\n\x14\x43ONTENT_TYPE_INVALID\x10\x00\x12\x15\n\x11\x43ONTENT_TYPE_JSON\x10\x01\"\xf5\x01\n\x19\x41uthorizationPolicyConfig\x12\x16\n\x06policy\x18\x01 \x01(\tR\x06policy\x12T\n\x06status\x18\x02 \x01(\x0e\x32<.indykite.auditsink.v1beta1.AuthorizationPolicyConfig.StatusR\x06status\x12\x12\n\x04tags\x18\x03 \x03(\tR\x04tags\"V\n\x06Status\x12\x12\n\x0eSTATUS_INVALID\x10\x00\x12\x11\n\rSTATUS_ACTIVE\x10\x01\x12\x13\n\x0fSTATUS_INACTIVE\x10\x02\x12\x10\n\x0cSTATUS_DRAFT\x10\x03\"\xaa\x02\n\x17\x41ssignConfigPermissions\x12+\n\x11target_identifier\x18\x01 \x01(\tR\x10targetIdentifier\x12G\n\x0btarget_type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\ntargetType\x12\x12\n\x04role\x18\x03 \x01(\tR\x04role\x12\x1f\n\x0b\x63ustomer_id\x18\x04 \x01(\tR\ncustomerId\x12\x1b\n\tobject_id\x18\x05 \x01(\tR\x08objectId\x12G\n\x0bobject_type\x18\x06 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\nobjectType\"\xaa\x02\n\x17RevokeConfigPermissions\x12+\n\x11target_identifier\x18\x01 \x01(\tR\x10targetIdentifier\x12G\n\x0btarget_type\x18\x02 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\ntargetType\x12\x12\n\x04role\x18\x03 \x01(\tR\x04role\x12\x1f\n\x0b\x63ustomer_id\x18\x04 \x01(\tR\ncustomerId\x12\x1b\n\tobject_id\x18\x05 \x01(\tR\x08objectId\x12G\n\x0bobject_type\x18\x06 \x01(\x0e\x32&.indykite.auditsink.v1beta1.ConfigTypeR\nobjectType\"\xb8\x07\n\x15TokenIntrospectConfig\x12I\n\x03jwt\x18\x01 \x01(\x0b\x32\x35.indykite.auditsink.v1beta1.TokenIntrospectConfig.JWTH\x00R\x03jwt\x12R\n\x06opaque\x18\x02 \x01(\x0b\x32\x38.indykite.auditsink.v1beta1.TokenIntrospectConfig.OpaqueH\x00R\x06opaque\x12U\n\x07offline\x18\x03 \x01(\x0b\x32\x39.indykite.auditsink.v1beta1.TokenIntrospectConfig.OfflineH\x01R\x07offline\x12R\n\x06online\x18\x04 \x01(\x0b\x32\x38.indykite.auditsink.v1beta1.TokenIntrospectConfig.OnlineH\x01R\x06online\x12k\n\x0e\x63laims_mapping\x18\x07 \x03(\x0b\x32\x44.indykite.auditsink.v1beta1.TokenIntrospectConfig.ClaimsMappingEntryR\rclaimsMapping\x12\"\n\rikg_node_type\x18\x05 \x01(\tR\x0bikgNodeType\x12%\n\x0eperform_upsert\x18\x06 \x01(\x08R\rperformUpsert\x1a\x39\n\x03JWT\x12\x16\n\x06issuer\x18\x01 \x01(\tR\x06issuer\x12\x1a\n\x08\x61udience\x18\x02 \x01(\tR\x08\x61udience\x1a\x08\n\x06Opaque\x1a*\n\x07Offline\x12\x1f\n\x0bpublic_jwks\x18\x01 \x03(\x0cR\npublicJwks\x1am\n\x06Online\x12+\n\x11userinfo_endpoint\x18\x01 \x01(\tR\x10userinfoEndpoint\x12\x36\n\tcache_ttl\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationR\x08\x63\x61\x63heTtl\x1a#\n\x05\x43laim\x12\x1a\n\x08selector\x18\x01 \x01(\tR\x08selector\x1ay\n\x12\x43laimsMappingEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12M\n\x05value\x18\x02 \x01(\x0b\x32\x37.indykite.auditsink.v1beta1.TokenIntrospectConfig.ClaimR\x05value:\x02\x38\x01\x42\x0f\n\rtoken_matcherB\x0c\n\nvalidation\"\x9f\x02\n\x14\x43onsentConfiguration\x12\x18\n\x07purpose\x18\x01 \x01(\tR\x07purpose\x12\x1f\n\x0b\x64\x61ta_points\x18\x02 \x03(\tR\ndataPoints\x12%\n\x0e\x61pplication_id\x18\x03 \x01(\tR\rapplicationId\x12\'\n\x0fvalidity_period\x18\x04 \x01(\x04R\x0evalidityPeriod\x12(\n\x10revoke_after_use\x18\x05 \x01(\x08R\x0erevokeAfterUse\x12R\n\x0ctoken_status\x18\x07 \x01(\x0e\x32/.indykite.auditsink.v1beta1.ExternalTokenStatusR\x0btokenStatus\"\xad\x01\n\x14IngestPipelineConfig\x12\x18\n\x07sources\x18\x01 \x03(\tR\x07sources\x12S\n\noperations\x18\x02 \x03(\x0e\x32\x33.indykite.auditsink.v1beta1.IngestPipelineOperationR\noperations\x12&\n\x0f\x61pp_agent_token\x18\x03 \x01(\tR\rappAgentToken\"\x8e\x0b\n\x1c\x45ntityMatchingPipelineConfig\x12\x64\n\x0bnode_filter\x18\x01 \x01(\x0b\x32\x43.indykite.auditsink.v1beta1.EntityMatchingPipelineConfig.NodeFilterR\nnodeFilter\x12\x36\n\x17similarity_score_cutoff\x18\x02 \x01(\x02R\x15similarityScoreCutoff\x12w\n\x17property_mapping_status\x18\x03 \x01(\x0e\x32?.indykite.auditsink.v1beta1.EntityMatchingPipelineConfig.StatusR\x15propertyMappingStatus\x12V\n\x18property_mapping_message\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x16propertyMappingMessage\x12u\n\x16\x65ntity_matching_status\x18\x04 \x01(\x0e\x32?.indykite.auditsink.v1beta1.EntityMatchingPipelineConfig.StatusR\x14\x65ntityMatchingStatus\x12T\n\x17\x65ntity_matching_message\x18\t \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x15\x65ntityMatchingMessage\x12u\n\x11property_mappings\x18\x05 \x03(\x0b\x32H.indykite.auditsink.v1beta1.EntityMatchingPipelineConfig.PropertyMappingR\x10propertyMappings\x12%\n\x0ererun_interval\x18\x06 \x01(\tR\rrerunInterval\x12>\n\rlast_run_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0blastRunTime\x12;\n\nreport_url\x18\n \x01(\x0b\x32\x1c.google.protobuf.StringValueR\treportUrl\x12=\n\x0breport_type\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.StringValueR\nreportType\x1a\x64\n\nNodeFilter\x12*\n\x11source_node_types\x18\x01 \x03(\tR\x0fsourceNodeTypes\x12*\n\x11target_node_types\x18\x02 \x03(\tR\x0ftargetNodeTypes\x1a\x81\x02\n\x0fPropertyMapping\x12(\n\x10source_node_type\x18\x01 \x01(\tR\x0esourceNodeType\x12\x30\n\x14source_node_property\x18\x02 \x01(\tR\x12sourceNodeProperty\x12(\n\x10target_node_type\x18\x03 \x01(\tR\x0etargetNodeType\x12\x30\n\x14target_node_property\x18\x04 \x01(\tR\x12targetNodeProperty\x12\x36\n\x17similarity_score_cutoff\x18\x05 \x01(\x02R\x15similarityScoreCutoff\"n\n\x06Status\x12\x12\n\x0eSTATUS_INVALID\x10\x00\x12\x12\n\x0eSTATUS_PENDING\x10\x01\x12\x16\n\x12STATUS_IN_PROGRESS\x10\x02\x12\x12\n\x0eSTATUS_SUCCESS\x10\x03\x12\x10\n\x0cSTATUS_ERROR\x10\x04\"\xf7\x01\n\x13TrustScoreDimension\x12H\n\x04name\x18\x01 \x01(\x0e\x32\x34.indykite.auditsink.v1beta1.TrustScoreDimension.NameR\x04name\x12\x16\n\x06weight\x18\x02 \x01(\x02R\x06weight\"~\n\x04Name\x12\x10\n\x0cNAME_INVALID\x10\x00\x12\x12\n\x0eNAME_FRESHNESS\x10\x01\x12\x15\n\x11NAME_COMPLETENESS\x10\x02\x12\x11\n\rNAME_VALIDITY\x10\x03\x12\x0f\n\x0bNAME_ORIGIN\x10\x04\x12\x15\n\x11NAME_VERIFICATION\x10\x05\"\xaf\x03\n\x17TrustScoreProfileConfig\x12/\n\x13node_classification\x18\x01 \x01(\tR\x12nodeClassification\x12O\n\ndimensions\x18\x02 \x03(\x0b\x32/.indykite.auditsink.v1beta1.TrustScoreDimensionR\ndimensions\x12_\n\x08schedule\x18\x03 \x01(\x0e\x32\x43.indykite.auditsink.v1beta1.TrustScoreProfileConfig.UpdateFrequencyR\x08schedule\"\xb0\x01\n\x0fUpdateFrequency\x12\x1c\n\x18UPDATE_FREQUENCY_INVALID\x10\x00\x12 \n\x1cUPDATE_FREQUENCY_THREE_HOURS\x10\x01\x12\x1e\n\x1aUPDATE_FREQUENCY_SIX_HOURS\x10\x02\x12!\n\x1dUPDATE_FREQUENCY_TWELVE_HOURS\x10\x03\x12\x1a\n\x16UPDATE_FREQUENCY_DAILY\x10\x04*\x8c\x05\n\nConfigType\x12\x17\n\x13\x43ONFIG_TYPE_INVALID\x10\x00\x12\x18\n\x14\x43ONFIG_TYPE_CUSTOMER\x10\x01\x12!\n\x1d\x43ONFIG_TYPE_APPLICATION_SPACE\x10\x02\x12\x1b\n\x17\x43ONFIG_TYPE_APPLICATION\x10\x04\x12\x19\n\x15\x43ONFIG_TYPE_APP_AGENT\x10\x05\x12$\n CONFIG_TYPE_APP_AGENT_CREDENTIAL\x10\x06\x12\x1f\n\x1b\x43ONFIG_TYPE_SERVICE_ACCOUNT\x10\x12\x12\"\n\x1e\x43ONFIG_TYPE_SERVICE_CREDENTIAL\x10\x13\x12\x1c\n\x18\x43ONFIG_TYPE_DIGITAL_TWIN\x10\x15\x12\x1a\n\x16\x43ONFIG_TYPE_AUDIT_SINK\x10\x1b\x12 \n\x1c\x43ONFIG_TYPE_TOKEN_INTROSPECT\x10\x1e\x12$\n CONFIG_TYPE_AUTHORIZATION_POLICY\x10\x16\x12\x17\n\x13\x43ONFIG_TYPE_CONSENT\x10\x1d\x12\x1f\n\x1b\x43ONFIG_TYPE_INGEST_PIPELINE\x10\x1f\x12(\n$CONFIG_TYPE_ENTITY_MATCHING_PIPELINE\x10 \x12&\n\"CONFIG_TYPE_EXTERNAL_DATA_RESOLVER\x10!\x12#\n\x1f\x43ONFIG_TYPE_TRUST_SCORE_PROFILE\x10\"\"\x04\x08\x0f\x10\x0f\"\x04\x08\x03\x10\x03\"\x04\x08\x07\x10\x07\"\x04\x08\x08\x10\x08\"\x04\x08\t\x10\t\"\x04\x08\n\x10\n\"\x04\x08\x0b\x10\x0b\"\x04\x08\x0c\x10\x0c\"\x04\x08\r\x10\r\"\x04\x08\x0e\x10\x0e\"\x04\x08\x10\x10\x10\"\x04\x08\x11\x10\x11\"\x04\x08\x18\x10\x18\"\x04\x08\x17\x10\x17*\xa0\x01\n\x13\x45xternalTokenStatus\x12!\n\x1d\x45XTERNAL_TOKEN_STATUS_INVALID\x10\x00\x12!\n\x1d\x45XTERNAL_TOKEN_STATUS_ENFORCE\x10\x01\x12\x1f\n\x1b\x45XTERNAL_TOKEN_STATUS_ALLOW\x10\x02\x12\"\n\x1e\x45XTERNAL_TOKEN_STATUS_DISALLOW\x10\x03*\xec\x02\n\x17IngestPipelineOperation\x12%\n!INGEST_PIPELINE_OPERATION_INVALID\x10\x00\x12)\n%INGEST_PIPELINE_OPERATION_UPSERT_NODE\x10\x01\x12\x31\n-INGEST_PIPELINE_OPERATION_UPSERT_RELATIONSHIP\x10\x02\x12)\n%INGEST_PIPELINE_OPERATION_DELETE_NODE\x10\x03\x12\x31\n-INGEST_PIPELINE_OPERATION_DELETE_RELATIONSHIP\x10\x04\x12\x32\n.INGEST_PIPELINE_OPERATION_DELETE_NODE_PROPERTY\x10\x05\x12:\n6INGEST_PIPELINE_OPERATION_DELETE_RELATIONSHIP_PROPERTY\x10\x06\x42\xb7\x01\n\x1e\x63om.indykite.auditsink.v1beta1B\x0b\x43onfigProtoP\x01\xa2\x02\x03IAX\xaa\x02\x1aIndykite.Auditsink.V1beta1\xca\x02\x1aIndykite\\Auditsink\\V1beta1\xe2\x02&Indykite\\Auditsink\\V1beta1\\GPBMetadata\xea\x02\x1cIndykite::Auditsink::V1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'indykite.auditsink.v1beta1.config_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.indykite.auditsink.v1beta1B\013ConfigProtoP\001\242\002\003IAX\252\002\032Indykite.Auditsink.V1beta1\312\002\032Indykite\\Auditsink\\V1beta1\342\002&Indykite\\Auditsink\\V1beta1\\GPBMetadata\352\002\034Indykite::Auditsink::V1beta1'
  _globals['_EXTERNALDATARESOLVERCONFIG_HEADERSENTRY']._loaded_options = None
  _globals['_EXTERNALDATARESOLVERCONFIG_HEADERSENTRY']._serialized_options = b'8\001'
  _globals['_TOKENINTROSPECTCONFIG_CLAIMSMAPPINGENTRY']._loaded_options = None
  _globals['_TOKENINTROSPECTCONFIG_CLAIMSMAPPINGENTRY']._serialized_options = b'8\001'
  _globals['_CONFIGTYPE']._serialized_start=8571
  _globals['_CONFIGTYPE']._serialized_end=9223
  _globals['_EXTERNALTOKENSTATUS']._serialized_start=9226
  _globals['_EXTERNALTOKENSTATUS']._serialized_end=9386
  _globals['_INGESTPIPELINEOPERATION']._serialized_start=9389
  _globals['_INGESTPIPELINEOPERATION']._serialized_end=9753
  _globals['_CONTAINERSPATH']._serialized_start=168
  _globals['_CONTAINERSPATH']._serialized_end=273
  _globals['_CREATEDCONFIG']._serialized_start=276
  _globals['_CREATEDCONFIG']._serialized_end=686
  _globals['_CREATEDCONFIG_LOCATION']._serialized_start=600
  _globals['_CREATEDCONFIG_LOCATION']._serialized_end=686
  _globals['_READCONFIG']._serialized_start=689
  _globals['_READCONFIG']._serialized_end=1127
  _globals['_READCONFIG_NAMEIDENTIFIER']._serialized_start=944
  _globals['_READCONFIG_NAMEIDENTIFIER']._serialized_end=1113
  _globals['_UPDATEDCONFIG']._serialized_start=1130
  _globals['_UPDATEDCONFIG']._serialized_end=1436
  _globals['_DELETEDCONFIG']._serialized_start=1439
  _globals['_DELETEDCONFIG']._serialized_end=1615
  _globals['_CONFIGDETAIL']._serialized_start=1618
  _globals['_CONFIGDETAIL']._serialized_end=2946
  _globals['_APPLICATIONAGENTCREDENTIALCONFIG']._serialized_start=2949
  _globals['_APPLICATIONAGENTCREDENTIALCONFIG']._serialized_end=3128
  _globals['_SERVICEACCOUNTCREDENTIALCONFIG']._serialized_start=3131
  _globals['_SERVICEACCOUNTCREDENTIALCONFIG']._serialized_end=3308
  _globals['_AUDITSINKCONFIG']._serialized_start=3311
  _globals['_AUDITSINKCONFIG']._serialized_end=3602
  _globals['_AUDITSINKCONFIG_KAFKA']._serialized_start=3406
  _globals['_AUDITSINKCONFIG_KAFKA']._serialized_end=3590
  _globals['_EXTERNALDATARESOLVERCONFIG']._serialized_start=3605
  _globals['_EXTERNALDATARESOLVERCONFIG']._serialized_end=4188
  _globals['_EXTERNALDATARESOLVERCONFIG_HEADERSENTRY']._serialized_start=4066
  _globals['_EXTERNALDATARESOLVERCONFIG_HEADERSENTRY']._serialized_end=4124
  _globals['_EXTERNALDATARESOLVERCONFIG_CONTENTTYPE']._serialized_start=4126
  _globals['_EXTERNALDATARESOLVERCONFIG_CONTENTTYPE']._serialized_end=4188
  _globals['_AUTHORIZATIONPOLICYCONFIG']._serialized_start=4191
  _globals['_AUTHORIZATIONPOLICYCONFIG']._serialized_end=4436
  _globals['_AUTHORIZATIONPOLICYCONFIG_STATUS']._serialized_start=4350
  _globals['_AUTHORIZATIONPOLICYCONFIG_STATUS']._serialized_end=4436
  _globals['_ASSIGNCONFIGPERMISSIONS']._serialized_start=4439
  _globals['_ASSIGNCONFIGPERMISSIONS']._serialized_end=4737
  _globals['_REVOKECONFIGPERMISSIONS']._serialized_start=4740
  _globals['_REVOKECONFIGPERMISSIONS']._serialized_end=5038
  _globals['_TOKENINTROSPECTCONFIG']._serialized_start=5041
  _globals['_TOKENINTROSPECTCONFIG']._serialized_end=5993
  _globals['_TOKENINTROSPECTCONFIG_JWT']._serialized_start=5580
  _globals['_TOKENINTROSPECTCONFIG_JWT']._serialized_end=5637
  _globals['_TOKENINTROSPECTCONFIG_OPAQUE']._serialized_start=5639
  _globals['_TOKENINTROSPECTCONFIG_OPAQUE']._serialized_end=5647
  _globals['_TOKENINTROSPECTCONFIG_OFFLINE']._serialized_start=5649
  _globals['_TOKENINTROSPECTCONFIG_OFFLINE']._serialized_end=5691
  _globals['_TOKENINTROSPECTCONFIG_ONLINE']._serialized_start=5693
  _globals['_TOKENINTROSPECTCONFIG_ONLINE']._serialized_end=5802
  _globals['_TOKENINTROSPECTCONFIG_CLAIM']._serialized_start=5804
  _globals['_TOKENINTROSPECTCONFIG_CLAIM']._serialized_end=5839
  _globals['_TOKENINTROSPECTCONFIG_CLAIMSMAPPINGENTRY']._serialized_start=5841
  _globals['_TOKENINTROSPECTCONFIG_CLAIMSMAPPINGENTRY']._serialized_end=5962
  _globals['_CONSENTCONFIGURATION']._serialized_start=5996
  _globals['_CONSENTCONFIGURATION']._serialized_end=6283
  _globals['_INGESTPIPELINECONFIG']._serialized_start=6286
  _globals['_INGESTPIPELINECONFIG']._serialized_end=6459
  _globals['_ENTITYMATCHINGPIPELINECONFIG']._serialized_start=6462
  _globals['_ENTITYMATCHINGPIPELINECONFIG']._serialized_end=7884
  _globals['_ENTITYMATCHINGPIPELINECONFIG_NODEFILTER']._serialized_start=7412
  _globals['_ENTITYMATCHINGPIPELINECONFIG_NODEFILTER']._serialized_end=7512
  _globals['_ENTITYMATCHINGPIPELINECONFIG_PROPERTYMAPPING']._serialized_start=7515
  _globals['_ENTITYMATCHINGPIPELINECONFIG_PROPERTYMAPPING']._serialized_end=7772
  _globals['_ENTITYMATCHINGPIPELINECONFIG_STATUS']._serialized_start=7774
  _globals['_ENTITYMATCHINGPIPELINECONFIG_STATUS']._serialized_end=7884
  _globals['_TRUSTSCOREDIMENSION']._serialized_start=7887
  _globals['_TRUSTSCOREDIMENSION']._serialized_end=8134
  _globals['_TRUSTSCOREDIMENSION_NAME']._serialized_start=8008
  _globals['_TRUSTSCOREDIMENSION_NAME']._serialized_end=8134
  _globals['_TRUSTSCOREPROFILECONFIG']._serialized_start=8137
  _globals['_TRUSTSCOREPROFILECONFIG']._serialized_end=8568
  _globals['_TRUSTSCOREPROFILECONFIG_UPDATEFREQUENCY']._serialized_start=8392
  _globals['_TRUSTSCOREPROFILECONFIG_UPDATEFREQUENCY']._serialized_end=8568
# @@protoc_insertion_point(module_scope)
