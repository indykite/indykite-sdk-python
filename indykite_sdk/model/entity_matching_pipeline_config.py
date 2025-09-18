from dataclasses import dataclass
from datetime import datetime

from indykite_sdk.model.entity_matching_status import Status
from indykite_sdk.model.node_filter import NodeFilter
from indykite_sdk.model.property_mapping import PropertyMapping
from indykite_sdk.utils import timestamp_to_date


@dataclass
class EntityMatchingPipelineConfig:
    @classmethod
    def deserialize(cls, message_config):
        node_filter: NodeFilter | None = None
        similarity_score_cutoff: float | None = None
        property_mapping_status: str | None = None
        property_mapping_message: str | None = None
        entity_matching_status: str | None = None
        entity_matching_message: str | None = None
        property_mappings: list[PropertyMapping] = dataclass.field(default_factory=list)
        rerun_interval: str | None = None
        last_run_time: datetime | None = None
        report_url: str | None = None
        report_type: str | None = None

        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for optional fields
        optional_fields = {
            "node_filter": NodeFilter.deserialize(message_config.node_filter),
            "similarity_score_cutoff": float,
            "property_mapping_status": cls._validate_status,
            "property_mapping_message": str,
            "entity_matching_status": cls._validate_status,
            "entity_matching_message": str,
            "property_mappings": lambda val: [PropertyMapping.deserialize(p) for p in val],
            "rerun_interval": str,
            "last_run_time": timestamp_to_date,
            "report_url": str,
            "report_type": str,
        }

        # Process optional fields
        kwargs = {}
        for field_name, processor in optional_fields.items():
            if field_name in fields:
                try:
                    kwargs[field_name] = processor(fields[field_name])
                except Exception as e:
                    raise ValueError(f"Error processing field '{field_name}': {e}")

        return cls(**kwargs)

    @staticmethod
    def _validate_status(value):
        try:
            return Status(value).name
        except ValueError:
            raise TypeError(f"'{value}' is not a valid status")
