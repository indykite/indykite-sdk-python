from indykite_sdk.indykite.config.v1beta1.model_pb2 import IngestMappingConfig


class IngestMappingConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        ingest_mapping_config=IngestMappingConfig(
            upsert=IngestMappingConfig.UpsertData(
                entities=list(IngestMappingConfig.Entity(
                    tenant_id=str(message_config.upsert.entities.tenant_id),
                    labels=list(str(message_config.upsert.entities.labels)),
                    external_id=IngestMappingConfig.Property(
                        source_name=str(message_config.upsert.entities.external_id.source_name),
                        mapped_name=str(message_config.upsert.entities.external_id.mapped_name),
                        is_required=bool(message_config.upsert.entities.external_id.is_required)),
                    properties=list(IngestMappingConfig.Property(
                        source_name=str(message_config.upsert.entities.properties.source_name),
                        mapped_name=str(message_config.upsert.entities.properties.mapped_name),
                        is_required=bool(message_config.upsert.entities.properties.is_required))),
                    relationships=list(IngestMappingConfig.Relationship(
                        external_id=str(message_config.upsert.entities.relationships.external_id),
                        type=str(message_config.upsert.entities.relationships.type),
                        direction=IngestMappingConfig.Direction(message_config.upsert.entities.relationships.direction),
                        match_label=str(message_config.upsert.entities.relationships.match_label)))
                ))
            )
        )
        return ingest_mapping_config

    def __init__(self, upsert):
        self.upsert = upsert

