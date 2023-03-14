from indykite_sdk.utils import duration_to_seconds
from indykite_sdk.model.conveyance_preference import ConveyancePreference
from indykite_sdk.model.authenticator_attachment import AuthenticatorAttachment
from indykite_sdk.model.user_verification_requirement import UserVerificationRequirement


class WebAuthnProviderConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        relying = {}
        for k, v in message_config.relying_parties.items():
            relying[k] = v
        webauthn_provider_config = WebAuthnProviderConfig(
            relying
        )
        if "attestation_preference" in fields:
            webauthn_provider_config.attestation_preference = ConveyancePreference(message_config.attestation_preference).name
        if "authenticator_attachment" in fields:
            webauthn_provider_config.authenticator_attachment = \
                AuthenticatorAttachment(message_config.authenticator_attachment).name
        if "require_resident_key" in fields:
            webauthn_provider_config.require_resident_key = bool(message_config.require_resident_key)
        if "user_verification" in fields:
            webauthn_provider_config.user_verification = UserVerificationRequirement(message_config.user_verification).name
        if "registration_timeout" in fields:
            webauthn_provider_config.registration_timeout = duration_to_seconds(message_config.registration_timeout)
        if "authentication_timeout" in fields:
            webauthn_provider_config.authentication_timeout = duration_to_seconds(message_config.authentication_timeout)
        return webauthn_provider_config

    def __init__(self, relying_parties, attestation_preference=None, authenticator_attachment=None, require_resident_key=None,
                 user_verification=None):
        self.relying_parties = relying_parties
        self.attestation_preference = attestation_preference
        self.authenticator_attachment = authenticator_attachment
        self.require_resident_key = require_resident_key
        self.user_verification = user_verification
        self.registration_timeout = None
        self.authentication_timeout = None
