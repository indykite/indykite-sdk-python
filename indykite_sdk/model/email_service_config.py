from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailServiceConfig, Email, SendGridProviderConfig, EmailDefinition, MailJetProviderConfig, MailgunProviderConfig, AmazonSESProviderConfig
from indykite_sdk.model.email_template import EmailTemplate
from indykite_sdk.model.email_message import EmailMessage


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

        if message_config.HasField('mailjet'):
            email_service_config.mailjet = MailJetProviderConfig(api_key=message_config.mailjet.api_key,
                                                                 sandbox_mode=message_config.mailjet.sandbox_mode,
                                                                 url_tags=message_config.mailjet.url_tags,
                                                                 custom_campaign=message_config.mailjet.custom_campaign)

        if message_config.HasField('mailgun'):
            email_service_config.mailgun = MailgunProviderConfig(api_key=message_config.mailgun.api_key,
                                                                 default_from_address=Email.deserialize(
                                                                     message_config.mailgun.default_from_address))

        if message_config.HasField('amazon'):
            email_service_config.amazon = AmazonSESProviderConfig(access_key_id=message_config.amazon.access_key_id,
                                                                  secret_access_key=
                                                                  message_config.amazon.secret_access_key,
                                                                  region=message_config.amazon.region,
                                                                  configuration_set_name=
                                                                  message_config.amazon.configuration_set_name,
                                                                  default_from_address=Email.deserialize(
                                                                      message_config.amazon.default_from_address),
                                                                  feedback_forwarding_email_address=
                                                                  message_config.amazon.feedback_forwarding_email_address,
                                                                  reply_to_addresses=message_config.amazon.reply_to_addresses)

        if message_config.HasField('authentication_message'):
            email_service_config.authentication_message = EmailDefinition(
                template=EmailTemplate.deserialize(message_config.authentication_message.template),
                message=EmailMessage.deserialize(message_config.authentication_message.message))

        if message_config.HasField('invitation_message'):
            email_service_config.invitation_message = EmailDefinition(
                template=EmailTemplate.deserialize(message_config.invitation_message.template),
                message=EmailMessage.deserialize(message_config.invitation_message.message))

        if message_config.HasField('reset_password_message'):
            email_service_config.reset_password_message = EmailDefinition(
                template=EmailTemplate.deserialize(message_config.reset_password_message.template),
                message=EmailMessage.deserialize(message_config.reset_password_message.message))

        if message_config.HasField('verification_message'):
            email_service_config.verification_message = EmailDefinition(
                template=EmailTemplate.deserialize(message_config.verification_message.template),
                message=EmailMessage.deserialize(message_config.verification_message.message))

        if message_config.HasField('one_time_password_message'):
            email_service_config.one_time_password_message = EmailDefinition(
                template=EmailTemplate.deserialize(message_config.one_time_password_message.template),
                message=EmailMessage.deserialize(message_config.one_time_password_message.message))

        return email_service_config

    def __init__(self, default_from_address, default):

        self.default_from_address = default_from_address
        self.default = default
        self.sendgrid = None
        self.mailjet = None
        self.mailgun = None
        self.amazon = None
        self.authentication_message = None
        self.invitation_message = None
        self.reset_password_message = None
        self.verification_message = None
        self.one_time_password_message = None



