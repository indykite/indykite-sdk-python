from indykite_sdk.utils import timestamp_to_date


class RegisterApplicationAgentCredential:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        register_application_agent_credential = RegisterApplicationAgentCredential(
            str(message.id),
            str(message.application_agent_id),
            str(message.kid),
            bytes(message.agent_config),
            timestamp_to_date(message.create_time),
            timestamp_to_date(message.expire_time),
            str(message.bookmark),
        )

        return register_application_agent_credential

    def __init__(self, id, application_agent_id, kid, agent_config, create_time, expire_time, bookmark):
        self.id = id
        self.application_agent_id = application_agent_id
        self.kid = kid
        self.agent_config = agent_config
        self.create_time = create_time
        self.expire_time = expire_time
        self.bookmark = bookmark



