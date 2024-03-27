import sys
from indykite_sdk.indykite.trusted_data.access.v1beta1 import trusted_data_access_api_pb2 as pb2
from indykite_sdk.model.access_consented_data import (AccessConsentedDataResponse)
import indykite_sdk.utils.logger as logger


def grant_consent_by_id(self, user_id, consent_id, revoke_after_use=False):
    """
    create consent
    :param self:
    :param user_id: string GID id of identity node
    :param consent_id: string GID id of consent config node
    :param revoke_after_use: boolean
    :return: GrantConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.GrantConsentRequest(
                user_id=user_id,
                consent_id=consent_id,
                revoke_after_use=revoke_after_use
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def grant_consent_by_token(self, user_token, consent_id, revoke_after_use=False):
    """
    create consent
    :param self:
    :param user_token: user token as string
    :param consent_id: string GID id of consent config node
    :param revoke_after_use: boolean
    :return: GrantConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.GrantConsentRequest(
                user_token=user_token,
                consent_id=consent_id,
                revoke_after_use=revoke_after_use
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def revoke_consent_by_id(self, user_id, consent_id):
    """
    create consent
    :param self:
    :param user_id: string GID id of identity node
    :param consent_id: string GID id of consent config node
    :return: RevokeConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.GrantConsentRequest(
                user_id=user_id,
                consent_id=consent_id
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def revoke_consent_by_token(self, user_token, consent_id):
    """
    create consent
    :param self:
    :param user_token: user token as string
    :param consent_id: string GID id of consent config node
    :return: RevokeConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.GrantConsentRequest(
                user_token=user_token,
                consent_id=consent_id
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def access_consented_data(self, consent_id, user_id):
    """
    create consent
    :param self:
    :param consent_id: string GID id of consent config node
    :param user_id: string GID id of identity node
    :return: AccessConsentedDataResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConsent(
            pb2.AccessConsentedDataRequest(
                consent_id=consent_id,
                user_id=user_id
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return AccessConsentedDataResponse.deserialize(response)
