from enum import Enum


class IngestMappingConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        ingest_mapping_config = UpsertData.deserialize(message_config.upsert)
        return ingest_mapping_config

    def __init__(self, upsert):
        self.upsert = upsert


class UpsertData:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        print(fields)
        upsert_data = UpsertData()
        if "entities" in fields:
            entities = []
            for e in message.entities:
                entities.append(Entity.deserialize(e))
            upsert_data.entities = entities
        return upsert_data

    def __init__(self, entities=None):
        self.entities = entities


class Entity:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        print(fields)
        entity = Entity(str(message.tenant_id))
        if "labels" in fields:
            labels = []
            for e in message.labels:
                labels.append(str(e))
            entity.labels = labels
        if "external_id" in fields:
            entity.external_id = Property.deserialize(message.external_id)
        if "properties" in fields:
            properties = []
            for e in message.properties:
                properties.append(Property.deserialize(e))
            entity.properties = properties
        if "relationships" in fields:
            relationships = []
            for e in message.relationships:
                relationships.append(Relationship.deserialize(e))
            entity.relationships = relationships
        return entity

    def __init__(self, tenant_id, labels=None, external_id=None, properties=None, relationships=None):
        self.tenant_id = tenant_id
        self.labels = labels
        self.external_id = external_id
        self.properties = properties
        self.relationships = relationships


class Property:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        entity_property = Property()
        if "source_name" in fields:
            entity_property.source_name = str(message.source_name)
        if "mapped_name" in fields:
            entity_property.mapped_name = str(message.mapped_name)
        if "is_required" in fields:
            entity_property.is_required = bool(message.is_required)
        return entity_property

    def __init__(self, source_name=None, mapped_name=None, is_required=None):
        self.source_name = source_name
        self.mapped_name = mapped_name
        self.is_required = is_required


class Relationship:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        relationship = Relationship()
        if "external_id" in fields:
            relationship.external_id = str(message.external_id)
        if "type" in fields:
            relationship.type = str(message.type)
        if "direction" in fields:
            relationship.direction = Direction(message.direction).name
        if "match_label" in fields:
            relationship.match_label = str(message.match_label)
        return relationship

    def __init__(self, external_id=None, type_relationship=None, direction=None, match_label=None):
        self.external_id = external_id
        self.type = type_relationship
        self.direction = direction
        self.match_label = match_label


class Direction(Enum):
    DIRECTION_INVALID = 0
    DIRECTION_INBOUND = 1
    DIRECTION_OUTBOUND = 2
