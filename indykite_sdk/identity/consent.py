from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as struct
from indykite_sdk.model.consent import CreateConsentResponse, CheckOAuth2ConsentChallengeResponse, CreateOAuth2ConsentVerifierResponse, ConsentRequestSessionData
import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.utils.message_to_value import arg_to_value


def create_consent(self, pii_processor_id, pii_principal_id, properties=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.CreateConsentRequest(
                pii_processor_id=pii_processor_id,
                pii_principal_id=pii_principal_id,
                properties=properties
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return CreateConsentResponse.deserialize(response)


def list_consents(self, pii_principal_id):
    sys.excepthook = logger.handle_excepthook
    try:
        streams = self.stub.ListConsents(
            pb2.ListConsentsRequest(
                pii_principal_id=pii_principal_id
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        return logger.logger_error(exception)

    return responses


def revoke_consent(self, pii_principal_id, consent_ids=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RevokeConsent(
            pb2.RevokeConsentRequest(
                pii_principal_id=pii_principal_id, consent_ids=consent_ids
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response


def check_oauth2_consent_challenge(self, challenge):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CheckOAuth2ConsentChallenge(
            pb2.CheckOAuth2ConsentChallengeRequest(
                challenge=challenge
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)
    if not response:
        return None

    return CheckOAuth2ConsentChallengeResponse.deserialize(response)


def create_oauth2_consent_verifier_approval(self, consent_challenge, grant_scopes=[], granted_audiences=[],
                                            access_token={}, id_token={}, userinfo={}, remember=False,
                                            remember_for=None):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateOAuth2ConsentVerifier(
            pb2.CreateOAuth2ConsentVerifierRequest(
                consent_challenge=consent_challenge,
                approval=pb2.ConsentApproval(
                    grant_scopes=grant_scopes,
                    granted_audiences=granted_audiences,
                    session=pb2.ConsentRequestSessionData(
                        access_token=arg_to_value(access_token) if access_token else {},
                        id_token=arg_to_value(id_token) if id_token else {},
                        userinfo=arg_to_value(userinfo) if userinfo else {}
                    ),
                    remember=remember,
                    remember_for=remember_for
                )
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)
    if not response:
        return None

    return response


def create_oauth2_consent_verifier_denial(self, consent_challenge, error=None,
                                          error_description=None,
                                          error_hint=None, status_code=None,):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateOAuth2ConsentVerifier(
            pb2.CreateOAuth2ConsentVerifierRequest(
                consent_challenge=consent_challenge,
                denial=pb2.DenialResponse(
                    error=error,
                    error_description=error_description,
                    error_hint=error_hint,
                    status_code=status_code
                )
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)
    if not response:
        return None

    return response
