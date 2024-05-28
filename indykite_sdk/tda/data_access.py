import sys
from indykite_sdk.indykite.tda.v1beta1 import trusted_data_access_api_pb2 as pb2
from indykite_sdk.model.data_access import DataAccessResponse, ListConsentsResponse
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2 as objects
from indykite_sdk.utils.message_to_value import arg_to_value
import indykite_sdk.utils.logger as logger


def grant_consent(self, user, consent_id, validity_period):
    """
    create consent
    :param self:
    :param user: dictionary
    :param consent_id: string GID id of consent config node
    :param validity_period: int seconds between 1 day and 2 years
    :return: GrantConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        user_obj = user_validation(user)
        response = self.stub.GrantConsent(
            pb2.GrantConsentRequest(
                user=user_obj,
                consent_id=consent_id,
                validity_period=int(validity_period)
            )
        )
        if not response:
            return None
        return response
    except Exception as exception:
        return logger.logger_error(exception)


def revoke_consent(self, user, consent_id):
    """
    create consent
    :param self:
    :param user: dictionary
    :param consent_id: string GID id of consent config node
    :return: RevokeConsentResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        user_obj = user_validation(user)
        response = self.stub.RevokeConsent(
            pb2.RevokeConsentRequest(
                user=user_obj,
                consent_id=consent_id
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def data_access(self, consent_id, application_id, user=None):
    """
    data access
    :param self:
    :param consent_id: string GID id of consent config node
    :param application_id: string GID id of application
    :param user: User object from knowledge objects
    :return: DataAccessResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        user_obj = user_validation(user)
        response = self.stub.DataAccess(
            pb2.DataAccessRequest(
                consent_id=consent_id,
                application_id=application_id,
                user=user_obj if user_obj else None
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return DataAccessResponse.deserialize(response)


def list_consents(self, user, application_id):
    """
    data access
    :param self:
    :param user: User object from knowledge objects
    :param application_id: string GID id of application
    :return: ListConsentsResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        user_obj = user_validation(user)
        response = self.stub.ListConsents(
            pb2.ListConsentsRequest(
                user=user_obj,
                application_id=application_id,
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ListConsentsResponse.deserialize(response)


def user_validation(user=None):
    """
    user_validation
    :param user: dictionary
    :return: User object from knowledge objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        user_obj = None
        if isinstance(user, dict):
            key = next(iter(user))
            match key:
                case "user_id":
                    user_obj = objects.User(user_id=user[key])
                case "property":
                    if isinstance(user[key], dict):
                        user_obj = objects.User(
                            property=objects.User.Property(
                                type=user[key]["type"],
                                value=arg_to_value(user[key]["value"])
                            )
                        )
                    else:
                        raise Exception('ExternalID should be a dictionary')
                case "external_id":
                    if isinstance(user[key], dict):
                        user_obj = objects.User(
                            external_id=objects.User.ExternalID(
                                type=user[key]["type"],
                                external_id=user[key]["external_id"]
                            )
                        )
                    else:
                        raise Exception('ExternalID should be a dictionary')
                case _:
                    raise Exception('Key should be user_id, property or external_id')

        return user_obj
    except Exception as exception:
        return logger.logger_error(exception)
