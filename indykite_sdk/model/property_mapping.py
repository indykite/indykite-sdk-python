class PropertyMapping:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        property_mapping = PropertyMapping(
            source_node_type=message_config.source_node_type,
            source_node_property=message_config.source_node_property,
            target_node_type=message_config.target_node_type,
            target_node_property=message_config.target_node_property,
        )
        if "similarity_score_cutoff" in fields:
            property_mapping.similarity_score_cutoff = float(message_config.similarity_score_cutoff)
        return property_mapping

    def __init__(self,
                 source_node_type,
                 source_node_property,
                 target_node_type,
                 target_node_property,
                 similarity_score_cutoff=None):

        self.source_node_type = source_node_type
        self.source_node_property = source_node_property
        self.target_node_type = target_node_type
        self.target_node_property = target_node_property
        self.similarity_score_cutoff = similarity_score_cutoff

