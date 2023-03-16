from indykite_sdk.model.email_template import EmailTemplate
from indykite_sdk.model.email_message import EmailMessage


class EmailDefinition:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        email_definition = EmailDefinition()

        if "template" in fields:
            email_definition.template = EmailTemplate.deserialize(message_config.template)
        if "message" in fields:
            email_definition.message = EmailMessage.deserialize(message_config.message)
        return email_definition

    def __init__(self, template=None, message=None):
        self.template = template
        self.message = message
