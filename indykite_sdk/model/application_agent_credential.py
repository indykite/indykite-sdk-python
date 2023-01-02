from indykite_sdk.utils import timestamp_to_date


class ApplicationAgentCredential:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        application_agent_credential = ApplicationAgentCredential(
            str(message.id),
            str(message.kid),
            str(message.display_name),
            str(message.customer_id),
            str(message.app_space_id),
            str(message.application_id),
            str(message.application_agent_id)
        )

        if message.HasField('create_time'):
            application_agent_credential.create_time = timestamp_to_date(message.create_time)

        if message.HasField('destroy_time'):
            application_agent_credential.destroy_time = timestamp_to_date(message.destroy_time)

        if message.HasField('delete_time'):
            application_agent_credential.delete_time = timestamp_to_date(message.delete_time)

        return application_agent_credential

    def __init__(self, id, kid, display_name, customer_id, app_space_id, application_id, application_agent_id):
        self.id = id
        self.kid = kid
        self.display_name = display_name
        self.customer_id = customer_id
        self.app_space_id = app_space_id
        self.application_id = application_id
        self.application_agent_id = application_agent_id
        self.create_time = None
        self.destroy_time = None
        self.delete_time = None


