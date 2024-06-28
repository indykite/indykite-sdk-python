class TokenIntrospectConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        claims_mapping = {}
        for k, v in message_config.claims_mapping.items():
            claims_mapping[k] = v.selector

        token_introspect_config = TokenIntrospectConfig(
            claims_mapping=claims_mapping,
            ikg_node_type=str(message_config.ikg_node_type),
            perform_upsert=message_config.perform_upsert
        )
        if "jwt" in fields:
            token_introspect_config.jwt = message_config.jwt
        elif "opaque" in fields:
            token_introspect_config.opaque = message_config.opaque

        if "offline" in fields:
            token_introspect_config.offline = message_config.offline
        elif "online" in fields:
            token_introspect_config.online = message_config.online
        return token_introspect_config

    def __init__(self,
                 claims_mapping,
                 ikg_node_type,
                 perform_upsert=False,
                 jwt=None,
                 opaque=None,
                 offline=None,
                 online= None):

        self.jwt = jwt
        self.opaque = opaque
        self.offline = offline
        self.online = online
        self.claims_mapping = claims_mapping
        self.ikg_node_type = ikg_node_type
        self.perform_upsert = perform_upsert
