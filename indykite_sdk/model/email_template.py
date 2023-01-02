from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.json_format import MessageToDict


class EmailTemplate:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        email_template = EmailTemplate(message.template_id)
        if message.HasField("template_version"):
            email_template.template_version = wrappers.StringValue(message.template_version)
        if message.HasField("reply_to"):
            email_template.reply_to = Email(message.reply_to)
        if message.HasField("to"):
            email_template.to = list(Email(message.to))
        if message.HasField("cc"):
            email_template.cc = list(Email(message.cc))
        if message.HasField("bcc"):
            email_template.bcc = list(Email(message.bcc))
        if message.HasField("subject"):
            email_template.subject = str(message.subject)
        if message.HasField("headers"):
            email_template.headers = MessageToDict(message.headers)
        if message.HasField("custom_args"):
            email_template.custom_args = MessageToDict(message.custom_args)
        if message.HasField("dynamic_template_values"):
            email_template.dynamic_template_values = MessageToDict(message.dynamic_template_values)
        if message.HasField("categories"):
            email_template.categories = list(str(message.categories))
        if message.HasField("attachments"):
            email_template.attachments = list(EmailAttachment(message.attachments))
        if message.HasField("event_payload"):
            email_template.event_payload = wrappers.StringValue(message.event_payload)
        if message.HasField("template_arn"):
            email_template.template_arn = str(message.template_arn)

        return email_template

    def __init__(self, template_id):
        self.template_id = template_id,
        self.template_version = None,
        self.reply_to = None,
        self.to = None,
        self.cc = None,
        self.bcc = None,
        self.subject = None,
        self.headers = None,
        self.custom_args = None,
        self.dynamic_template_values = None,
        self.categories = None,
        self.attachments = None,
        self.event_payload = None,
        self.template_arn = None


