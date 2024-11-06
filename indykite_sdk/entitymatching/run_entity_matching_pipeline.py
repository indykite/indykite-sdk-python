import sys

from indykite_sdk.indykite.entitymatching.v1beta1 import entity_matching_api_pb2 as pb2
from indykite_sdk.model.entity_matching import RunEntityMatchingPipelineResponse
import indykite_sdk.utils.logger as logger


def run_entity_matching_pipeline(self, id, similarity_score_cutoff, custom_property_mappings=None):
    """
    run entitymatching pipeline
    :param self:
    :param id: confg node GID id
    :param custom_property_mappings array of CustomPropertyMappings
    :param similarity_score_cutoff float required threshold (in range [0,1])
    :return: deserialized RunEntityMatchingPipelineResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RunEntityMatchingPipeline(
            pb2.RunEntityMatchingPipelineRequest(
                id=id,
                custom_property_mappings=custom_property_mappings,
                similarity_score_cutoff=similarity_score_cutoff
            )
        )
        if not response:
            return None
        return RunEntityMatchingPipelineResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)
