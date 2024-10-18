from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.property_mapping import PropertyMapping
from enum import Enum


class ReadSuggestedPropertyMappingResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        read_suggested_property_mapping = ReadSuggestedPropertyMappingResponse(
            id=message.id
        )
        if "property_mappings" in fields:
            read_suggested_property_mapping.property_mappings = [
                PropertyMapping.deserialize(p)
                for p in message.property_mappings
            ]
        if "property_mapping_status" in fields:
            statuses = [s.value for s in PipelineStatus]
            if message.property_mapping_status and message.property_mapping_status not in statuses:
                raise TypeError("property_mapping_status must be a member of PipelineStatus")
            read_suggested_property_mapping.property_mapping_status = (
                PipelineStatus(message.property_mapping_status).name)
        return read_suggested_property_mapping

    def __init__(self, id, property_mappings=None, property_mapping_status=None):
        self.id = id
        self.property_mappings = property_mappings
        self.property_mapping_status = property_mapping_status


class RunEntityMatchingPipelineResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        run_entity_matching_pipeline = RunEntityMatchingPipelineResponse(
            id=message.id
        )
        if "last_run_time" in fields:
            run_entity_matching_pipeline.last_run_time = timestamp_to_date(message.last_run_time)
        if "etag" in fields:
            run_entity_matching_pipeline.etag = str(message.etag)
        return run_entity_matching_pipeline

    def __init__(self, id, last_run_time=None, etag=None):
        self.id = id
        self.last_run_time = last_run_time
        self.etag = etag



class PipelineStatus(Enum):
	PIPELINE_STATUS_STATUS_INVALID = 0
	PIPELINE_STATUS_STATUS_PENDING = 1
	PIPELINE_STATUS_STATUS_IN_PROGRESS = 2
	PIPELINE_STATUS_STATUS_SUCCESS = 3
	PIPELINE_STATUS_STATUS_ERROR = 4
