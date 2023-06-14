class KnowledgeGraphSchemaConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        knowledge_graph_schema_config = KnowledgeGraphSchemaConfig(
            message_config.schema
        )
        return knowledge_graph_schema_config

    def __init__(self, schema):
        self.schema = schema
