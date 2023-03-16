from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.json_format import MessageToDict
from indykite_sdk.model.email import Email


class EmailTemplate:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        email_template = EmailTemplate(message.template_id)
        if "template_version" in fields:
            email_template.template_version = wrappers.StringValue(message.template_version)
        if "reply_to" in fields:
            email_template.reply_to = Email(message.reply_to)
        if "to" in fields:
            to = []
            for e in message.to:
                to.append(Email.deserialize(e))
            email_template.to = to
        if "cc" in fields:
            cc = []
            for e in message.cc:
                cc.append(Email.deserialize(e))
            email_template.cc = cc
        if "bcc" in fields:
            bcc = []
            for e in message.bcc:
                bcc.append(Email.deserialize(e))
            email_template.bcc = bcc
        if "subject" in fields:
            email_template.subject = str(message.subject)
        if "headers" in fields:
            email_template.headers = MessageToDict(message.headers)
        if "custom_args" in fields:
            email_template.custom_args = MessageToDict(message.custom_args)
        if "dynamic_template_values" in fields:
            email_template.dynamic_template_values = MessageToDict(message.dynamic_template_values)
        if "categories" in fields:
            categories = []
            for e in message.categories:
                categories.append(str(message.e))
            email_template.categories = categories
        if "attachments" in fields:
            attachments = []
            for e in message.attachments:
                attachments.append(EmailAttachment.deserialize(message.e))
            email_template.attachments = attachments
        if "event_payload" in fields:
            email_template.event_payload = wrappers.StringValue(message.event_payload)
        if "template_arn" in fields:
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


