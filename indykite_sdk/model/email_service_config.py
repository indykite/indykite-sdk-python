from indykite_sdk.indykite.config.v1beta1.model_pb2 import MailJetProviderConfig, MailgunProviderConfig, AmazonSESProviderConfig
from indykite_sdk.model.email import Email
from indykite_sdk.model.sendgrid_provider_config import SendGridProviderConfig
from indykite_sdk.model.email_definition import EmailDefinition


class EmailServiceConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]
        email_service_config = EmailServiceConfig(
            Email(message_config.default_from_address.address,message_config.default_from_address.name),
            bool(message_config.default),
        )

        if "sendgrid" in fields:
            email_service_config.sendgrid = SendGridProviderConfig.deserialize(message_config.sendgrid)

        if "mailjet" in fields:
            email_service_config.mailjet = MailJetProviderConfig(api_key=message_config.mailjet.api_key,
                                                                 sandbox_mode=message_config.mailjet.sandbox_mode,
                                                                 url_tags=message_config.mailjet.url_tags,
                                                                 custom_campaign=message_config.mailjet.custom_campaign)

        if "mailgun" in fields:
            email_service_config.mailgun = MailgunProviderConfig(api_key=message_config.mailgun.api_key,
                                                                 default_from_address=Email.deserialize(
                                                                     message_config.mailgun.default_from_address))

        if "amazon" in fields:
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

        if "invitation_message" in fields:
            email_service_config.invitation_message = EmailDefinition.deserialize(
                message_config.invitation_message)

        if "reset_password_message" in fields:
            email_service_config.reset_password_message = EmailDefinition.deserialize(
                message_config.reset_password_message)

        if "verification_message" in fields:
            email_service_config.verification_message = EmailDefinition.deserialize(
                message_config.verification_message.template)

        if "one_time_password_message" in fields:
            email_service_config.one_time_password_message = EmailDefinition.deserialize(
                message_config.one_time_password_message.template)

        return email_service_config

    def __init__(self, default_from_address, default):

        self.default_from_address = default_from_address
        self.default = default
        self.sendgrid = None
        self.mailjet = None
        self.mailgun = None
        self.amazon = None
        self.invitation_message = None
        self.reset_password_message = None
        self.verification_message = None
        self.one_time_password_message = None



