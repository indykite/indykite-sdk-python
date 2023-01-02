from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers


class EmailAttachment:
    @classmethod
    def deserialize(cls, message):
        return EmailAttachment(message.content_type, wrappers.StringValue(value=message.content_id), message.inline,
                               message.file_name, message.content)

    def __init__(self, content_type, content_id, inline, file_name, content):
        self.content_type = content_type
        self.content_id = content_id,
        self.inline = inline,
        self.file_name = file_name,
        self.content = content

    def __str__(self):
        return (
            f"Content type: {self.content_type} \n"
            f"Content id: {self.content_id} \n"
            f"Inline: {self.inline} \n"
            f"FileName: {self.file_name} \n"
            f"Content: {self.content} \n"
        )
