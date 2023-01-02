from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.json_format import MessageToDict


class EmailMessage:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        email_message = EmailMessage(list(Email(message.to)))
        if message.HasField("reply_to"):
            email_message.reply_to = Email(message.reply_to),
        if message.HasField("cc"):
            email_message.cc = list(Email(message.cc))
        if message.HasField("bcc"):
            email_message.bcc = list(Email(message.bcc))
        if message.HasField("subject"):
            email_message.subject = str(message.subject)
        if message.HasField("text_content"):
            email_message.text_content = str(message.text_content)
        if message.HasField("html_content"):
            email_message.html_content = str(message.html_content)
        if message.HasField("headers"):
            email_message.headers = MessageToDict(message.headers)
        if message.HasField("custom_args"):
            email_message.custom_args = MessageToDict(message.custom_args)
        if message.HasField("dynamic_template_values"):
            email_message.dynamic_template_values = MessageToDict(message.dynamic_template_values)
        if message.HasField("categories"):
            email_message.categories = list(str(message.categories))
        if message.HasField("attachments"):
            email_message.attachments = list(EmailAttachment(message.attachments))
        if message.HasField("event_payload"):
            email_message.event_payload = wrappers.StringValue(message.event_payload)

        return email_message

    def __init__(self, to):
        self.to = to,
        self.reply_to = None,
        self.cc = None,
        self.bcc = None,
        self.subject = None,
        self.text_content = None,
        self.html_content = None,
        self.headers = None,
        self.custom_args = None,
        self.dynamic_template_values = None,
        self.categories = None,
        self.attachments = None,
        self.event_payload = None


