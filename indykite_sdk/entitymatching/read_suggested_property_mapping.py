import sys

from indykite_sdk.indykite.entitymatching.v1beta1 import entity_matching_api_pb2 as pb2
from indykite_sdk.model.entity_matching import ReadSuggestedPropertyMappingResponse
import indykite_sdk.utils.logger as logger


def read_suggested_property_mapping(self, id):
    """
    read suggested property mapping
    :param self:
    :param id: confg node GID id
    :return: deserialized ReadSuggestedPropertyMappingResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadSuggestedPropertyMapping(
            pb2.ReadSuggestedPropertyMappingRequest(
                id=id
            )
        )
        if not response:
            return None
        return ReadSuggestedPropertyMappingResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)
