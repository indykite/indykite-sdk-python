class NodeFilter:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        node_filter = NodeFilter(
            source_node_types=[str(r) for r in message_config.source_node_types],
            target_node_types=[str(r) for r in message_config.target_node_types]
        )
        return node_filter

    def __init__(self,
                 source_node_types,
                 target_node_types):

        self.source_node_types = source_node_types
        self.target_node_types = target_node_types
