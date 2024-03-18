from indykite_sdk.utils.message_to_value import arg_to_value, grpc_to_value
from indykite_sdk.utils import timestamp_to_date


class IdentityKnowledgeReadResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        identity_knowledge = IdentityKnowledgeReadResponse()

        nodes = []
        if "nodes" in fields:
            for node in message.nodes:
                nodes.append(Node.deserialize(node))
        identity_knowledge.nodes = nodes
        relationships = []
        if "relationship" in fields:
            for relationship in message.relationships:
                relationships.append(Relationship.deserialize(relationship))
        identity_knowledge.relationships = relationships

        return identity_knowledge

    def __init__(self, nodes=None, relationships=None):
        self.nodes = nodes
        self.relationships = relationships


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
        if node.create_time:
            ik_node.create_time = timestamp_to_date(node.create_time)
        if node.update_time:
            ik_node.update_time = timestamp_to_date(node.update_time)
        ik_node.is_identity=False
        if node.is_identity:
            ik_node.is_identity=node.is_identity
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

    @classmethod
    def get_metadata(cls, node, property):
        """
        get the property metadata from the node's list of properties
        :param cls:
        :param node: node object
        :param property: string
        :return: value if found, None if not found
        """
        if not node.properties:
            return None
        res = [p for p in node.properties if p['key'] == property]
        if len(res) > 0:
            return res[0].get('metadata', None)
        return None

    def __init__(self, id=None, external_id=None, type=None,
                 tags=None, create_time=None, update_time=None,
                 properties=None, is_identity=None):
        self.id = id
        self.external_id = external_id
        self.type = type
        self.tags = tags
        self.create_time = create_time
        self.update_time = update_time
        self.properties = properties
        self.is_identity = is_identity


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
        if relationship.create_time:
            ik_relationship.create_time = timestamp_to_date(relationship.create_time)
        if relationship.update_time:
            ik_relationship.update_time = timestamp_to_date(relationship.update_time)
        property_map = {
            k: Property(arg_to_value(v))
            for k, v in relationship.properties.items()
        }
        ik_relationship.properties = property_map
        return ik_relationship

    def __init__(self, id=None, type=None, source=None, target=None, create_time=None, update_time=None,
                 properties=None):
        self.id = id
        self.type = type
        self.source = source
        self.target = target
        self.create_time = create_time
        self.update_time = update_time
        self.properties = properties


class Property:
    @classmethod
    def deserialize(cls, property):
        if property is None:
            return None
        return Property(
            property.type if property.type else None,
            grpc_to_value(property.value) if property.value else None,
            Metadata.deserialize(property.metadata) if property.metadata else None,
        )

    def __init__(self, type=None, value=None, metadata=None):
        self.type = type
        self.value = value
        self.metadata = metadata


class Metadata:
    @classmethod
    def deserialize(cls, metadata):
        if metadata is None:
            return None
        if (not metadata.assurance_level
            and not metadata.source
            and str(metadata.verification_time) == ""
            and not metadata.custom_metadata):
            return None
        custom = {}
        if hasattr(metadata, 'custom_metadata'):
            custom = {
                k: v
                for k, v in metadata.custom_metadata.items()
            }
        return Metadata(
            metadata.assurance_level if hasattr(metadata, 'assurance_level') else None,
            timestamp_to_date(metadata.verification_time) if hasattr(metadata, 'verification_time') else None,
            metadata.source if hasattr(metadata, 'source') else None,
            custom
        )

    def __init__(self, assurance_level=None, verification_time=None, source=None, custom_metadata={}):
        self.assurance_level = assurance_level
        self.verification_time = verification_time
        self.source = source
        self.custom_metadata = custom_metadata


class Return:
    @classmethod
    def deserialize(cls, returned):
        if returned is None:
            return None
        return Return(
            returned.variable or None,
            returned.properties or None,
        )

    def __init__(self, variable=None, properties=None):
        self.variable = variable
        self.properties = properties
