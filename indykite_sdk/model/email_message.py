from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.json_format import MessageToDict
from indykite_sdk.model.email import Email


class EmailMessage:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        email_message = EmailMessage()
        if "to" in fields:
            to = []
            for e in message.to:
                to.append(Email.deserialize(e))
            email_message.to = to
        if "reply_to" in fields:
            email_message.reply_to = Email.deserialize(message.reply_to)
        if "cc" in fields:
            cc = []
            for e in message.cc:
                cc.append(Email.deserialize(e))
            email_message.cc = cc
        if "bcc" in fields:
            bcc = []
            for e in message.bcc:
                bcc.append(Email.deserialize(e))
            email_message.bcc = bcc
        if "subject" in fields:
            email_message.subject = str(message.subject)
        if "text_content" in fields:
            email_message.text_content = str(message.text_content)
        if "html_content" in fields:
            email_message.html_content = str(message.html_content)
        if "headers" in fields:
            email_message.headers = MessageToDict(message.headers)
        if "custom_args" in fields:
            email_message.custom_args = MessageToDict(message.custom_args)
        if "dynamic_template_values" in fields:
            email_message.dynamic_template_values = MessageToDict(message.dynamic_template_values)
        if "categories" in fields:
            categories = []
            for e in message.categories:
                categories.append(str(message.e))
            email_message.categories = categories
        if "attachments" in fields:
            attachments = []
            for e in message.attachments:
                attachments.append(EmailAttachment.deserialize(message.e))
            email_message.attachments = attachments
        if "event_payload" in fields:
            email_message.event_payload = wrappers.StringValue(message.event_payload)

        return email_message

    def __init__(self, to=None):
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


