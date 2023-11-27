from indykite_sdk.utils.message_to_value import arg_to_value, object_to_value


class IdentityKnowledgeResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        identity_knowledge = IdentityKnowledgeResponse()

        if "paths" in fields:
            paths = []
            for e in message.paths:
                paths.append(Path.deserialize(e))
            identity_knowledge.paths = paths

        return identity_knowledge

    def __init__(self, path=None):
        self.path = path


class Node:
    @classmethod
    def deserialize(cls, node):
        if node is None:
            return None
        ik_node = Node(
            id=node.id,
            external_id=node.external_id
        )
        if node.type:
            ik_node.type=node.type
        if node.tags:
            ik_node.tags = [tag for tag in node.tags]
        if node.properties:
            properties = [Property.deserialize(property) for property in node.properties]
            ik_node.properties = properties
        return ik_node

    @classmethod
    def get_property(cls, node, property):
        """
        get the property with a certain key from the node's list of properties
        :param cls:
        :param node: node object
        :param property: string
        :return: value if found, None if not found
        """
        if not node.properties:
            return None
        res = [p['value'] for p in node.properties if p['key'] == property]
        if len(res) > 0:
            return res[0].get('stringValue', None)
        return None

    def __init__(self, id=None, external_id=None, type=None, tags=None, properties=None):
        self.id = id
        self.external_id = external_id
        self.type = type
        self.tags = tags
        self.properties = properties


class Relationship:
    @classmethod
    def deserialize(cls, relationship):
        if relationship is None:
            return None
        ik_relationship = Relationship(
            id=relationship.id,
            type=relationship.type,
            source=relationship.source,
            target=relationship.target,
        )
        property_map = {
            k: Property(arg_to_value(v))
            for k, v in relationship.properties.items()
        }
        ik_relationship.properties = property_map
        return ik_relationship

    def __init__(self, id=None, type=None, source=None, target=None, properties=None):
        self.id = id
        self.type = type
        self.source = source
        self.target = target
        self.properties = properties


class Path:
    @classmethod
    def deserialize(cls, path):
        if path is None:
            return None
        ik_path = Path()
        nodes = []
        for node in path.nodes:
            nodes.append(Node.deserialize(node))
        ik_path.nodes = nodes
        relationships = []
        for relationship in path.relationships:
            relationships.append(Relationship.deserialize(relationship))
        ik_path.relationships = relationships
        return ik_path

    def __init__(self, nodes=[], relationships=[]):
        self.nodes = nodes
        self.relationships = relationships


class Property:
    @classmethod
    def deserialize(cls, property):
        if property is None:
            return None
        return Property(
            property.key if property.key else None,
            object_to_value(property.value) if property.value else None
        )

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
