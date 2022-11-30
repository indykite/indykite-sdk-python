from jarvis_sdk.utils import timestamp_to_date
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import EmailServiceConfig, Email, SendGridProviderConfig, EmailDefinition
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from jarvis_sdk.model.email_template import EmailTemplate
from jarvis_sdk.model.email_message import EmailMessage


class EmailServiceConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        email_service_config = EmailServiceConfig(
            Email(address=message_config.default_from_address.address,name=message_config.default_from_address.name),
            str(message_config.default),
        )

        if message_config.HasField('sendgrid'):
            email_service_config.sendgrid = SendGridProviderConfig(api_key=message_config.sendgrid.api_key,
                                                                   sandbox_mode=message_config.sendgrid.sandbox_mode,
                                                                   ip_pool_name=message_config.sendgrid.ip_pool_name,
                                                                   host=message_config.sendgrid.host)

        if message_config.HasField('authentication_message'):
            email_service_config.authentication_message = EmailDefinition(template=EmailTemplate.deserialize(message_config.authentication_message.template),
                                                                          message=EmailMessage.deserialize(message_config.authentication_message.message))

        if message_config.HasField('invitation_message'):
            email_service_config.invitation_message = EmailDefinition(template=EmailTemplate.deserialize(message_config.invitation_message.template),
                                                                      message=EmailMessage.deserialize(message_config.invitation_message.message))

        if message_config.HasField('reset_password_message'):
            email_service_config.reset_password_message = EmailDefinition(template=EmailTemplate.deserialize(message_config.reset_password_message.template),
                                                                          message=EmailMessage.deserialize(message_config.reset_password_message.message))

        if message_config.HasField('verification_message'):
            email_service_config.verification_message = EmailDefinition(template=EmailTemplate.deserialize(message_config.verification_message.template),
                                                                        message=EmailMessage.deserialize(message_config.verification_message.message))

        if message_config.HasField('one_time_password_message'):
            email_service_config.one_time_password_message = EmailDefinition(template=EmailTemplate.deserialize(message_config.one_time_password_message.template),
                                                                             message=EmailMessage.deserialize(message_config.one_time_password_message.message))

        return email_service_config

    def __init__(self, default_from_address, default):

        self.default_from_address = default_from_address
        self.default = default
        self.sendgrid = None
        self.authentication_message = None
        self.invitation_message = None
        self.reset_password_message = None
        self.verification_message = None
        self.one_time_password_message = None



