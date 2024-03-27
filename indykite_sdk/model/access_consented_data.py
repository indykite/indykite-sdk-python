from indykite_sdk.model.identity_knowledge import Node, Relationship


class AccessConsentedDataResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        access_consented_data = AccessConsentedDataResponse()

        nodes = []
        if "nodes" in fields:
            for node in message.nodes:
                nodes.append(Node.deserialize(node))
        access_consented_data.nodes = nodes
        relationships = []
        if "relationship" in fields:
            for relationship in message.relationships:
                relationships.append(Relationship.deserialize(relationship))
        access_consented_data.relationships = relationships

        return access_consented_data

    def __init__(self, nodes=None, relationships=None):
        self.nodes = nodes
        self.relationships = relationships
