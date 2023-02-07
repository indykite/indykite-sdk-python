from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.model.consent import CreateConsentResponse


def create_consent(self, pii_processor_id, pii_principal_id, properties=[]):

    try:
        response = self.stub.CreateConsent(
            pb2.CreateConsentRequest(
                pii_processor_id=pii_processor_id,
                pii_principal_id=pii_principal_id,
                properties=properties
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return CreateConsentResponse.deserialize(response)


def list_consents(self, pii_principal_id):

    try:
        streams = self.stub.ListConsents(
            pb2.ListConsentsRequest(
                pii_principal_id=pii_principal_id
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        print(exception)
        return None

    return responses


def revoke_consent(self, pii_principal_id, consent_ids=[]):

    try:
        response = self.stub.RevokeConsent(
            pb2.RevokeConsentRequest(
                pii_principal_id=pii_principal_id, consent_ids=consent_ids
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response

