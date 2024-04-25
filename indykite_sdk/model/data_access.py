from indykite_sdk.model.identity_knowledge import Node


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
                nodes.append(Node.deserialize(node))
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
