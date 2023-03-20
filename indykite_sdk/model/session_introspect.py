from indykite_sdk.model.token_info import TokenInfo


class SessionIntrospect:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        fields = [desc.name for desc, val in message.ListFields()]
        session_introspect = SessionIntrospect(
            bool(message.active)
        )

        if "token_info" in fields:
            session_introspect.token_info = TokenInfo.deserialize(message.token_info)

        if "provider_data" in fields:
            provider_data = []
            for e in message.provider_data:
                provider_data.append(str(e))
            session_introspect.provider_data = provider_data

        return session_introspect

    def __init__(self, active, token_info=None, provider_data=None):
        self.active = active
        self.token_info = token_info
        self.provider_data = provider_data
