from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.model.provider_info import ProviderInfo
from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToDict


class TokenInfo:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        token_info = TokenInfo(
            str(message.customer_id),
            str(message.app_space_id),
            str(message.application_id),
            list(map(ProviderInfo.deserialize, message.provider_info))
        )

        if "subject" in fields:
            token_info.subject = DigitalTwinCore.deserialize(message.subject)

        if "impersonated" in fields:
            token_info.impersonated = DigitalTwinCore.deserialize(
                message.impersonated)

        if "issue_time" in fields:
            token_info.issueTime = timestamp_to_date(message.issue_time)

        if "expire_time" in fields:
            token_info.expireTime = timestamp_to_date(message.expire_time)

        if "authentication_time" in fields:
            token_info.authenticationTime = timestamp_to_date(
                message.authentication_time)

        if "session_claims" in fields:
            token_info.session_claims = MessageToDict(message.session_claims)

        if "token_claims" in fields:
            token_info.token_claims = MessageToDict(message.token_claims)

        return token_info

    def __init__(self, customer_id, app_space_id, application_id, provider_info):
        self.customerId = customer_id
        self.appSpaceId = app_space_id
        self.applicationId = application_id
        self.providerInfo = provider_info
        self.subject = None
        self.impersonated = None
        self.issueTime = None
        self.expireTime = None
        self.authenticationTime = None
        self.session_claims = None
        self.token_claims = None

    def __str__(self):
        string = (
            "Customer ID: " + self.customerId + "\n"
            "Application Space ID: " + self.appSpaceId + "\n"
            "Application ID: " + self.applicationId
        )

        if hasattr(self, "subject"):
            string = (
                string + "\n"
                "Subject ID: " + self.subject.id + "\n"
                "Subject tenant ID: " + self.subject.tenantId
            )

        if hasattr(self, "issueTime"):
            string = (
                string + "\n"
                "Issue time: " + str(self.issueTime)
            )

        if hasattr(self, "expireTime"):
            string = (
                string + "\n"
                "Expire time: " + str(self.expireTime)
            )

        if hasattr(self, "authenticationTime"):
            string = (
                string + "\n"
                "Authentication time: " + str(self.authenticationTime)
            )

        providers_string = ""
        for provider in self.providerInfo:
            providers_string = providers_string + str(provider) + "\n"

        string = (
            string + "\n"
            "Provider info:\n" + providers_string.strip()
        )

        return string
