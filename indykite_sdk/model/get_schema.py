class GetSchemaHelpers:
    @classmethod
    def deserialize(cls, message):
        fields = [desc.name for desc, val in message.ListFields()]
        if "knowledge_graph_schema_helpers" in fields:
            get_schema_helpers = GetSchemaHelpers(
                knowledge_graph_schema_helpers=KnowledgeGraphSchemaHelpers.deserialize(
                    message.knowledge_graph_schema_helpers)
            )
            return get_schema_helpers
        return None

    def __init__(self, knowledge_graph_schema_helpers):
        self.knowledge_graph_schema_helpers = knowledge_graph_schema_helpers


class KnowledgeGraphSchemaHelpers:
    @classmethod
    def deserialize(cls, message):
        fields = [desc.name for desc, val in message.ListFields()]
        if "definitions" and "directives" in fields:
            get_schema_helpers = KnowledgeGraphSchemaHelpers(message.definitions, message.directives)
            return get_schema_helpers
        return None

    def __init__(self, definitions, directives):
        self.definitions = definitions
        self.directives = directives
