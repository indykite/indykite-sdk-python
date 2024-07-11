from indykite_sdk.model.identity_knowledge import Property
from indykite_sdk.utils import timestamp_to_date


class DataAccessResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        data_access = DataAccessResponse()

        nodes = []
        if "nodes" in fields:
            for node in message.nodes:
                nodes.append(TrustedDataNode.deserialize(node))
        data_access.nodes = nodes
        return data_access

    def __init__(self, nodes=None):
        self.nodes = nodes


class ListConsentsResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        list_consents = ListConsentsResponse()

        consents = []
        if "consents" in fields:
            for consent in message.consents:
                consents.append(Consent.deserialize(consent))
        list_consents.consents = consents
        return list_consents

    def __init__(self, consents=None):
        self.consents = consents


class Consent:
    @classmethod
    def deserialize(cls, consent):
        if consent is None:
            return None
        return_consent = Consent(
            consent.id if consent.id else None,
            consent.properties if consent.properties else []
        )

    def __init__(self, id=None, properties=None):
        self.id = id
        self.properties = properties


class TrustedDataNode:
    @classmethod
    def deserialize(cls, node):
        if node is None:
            return None
        ik_node = TrustedDataNode(
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
        if node.nodes:
            nodes = [TrustedDataNode.deserialize(n) for n in node.nodes]
            ik_node.nodes = nodes
        return ik_node

    def __init__(self, id=None, external_id=None, type=None,
                 tags=None, create_time=None, update_time=None,
                 properties=None, is_identity=None, nodes=None):
        self.id = id
        self.external_id = external_id
        self.type = type
        self.tags = tags
        self.create_time = create_time
        self.update_time = update_time
        self.properties = properties
        self.is_identity = is_identity
        self.nodes = nodes
