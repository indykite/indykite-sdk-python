from dataclasses import dataclass, field

from indykite_sdk.model.trust_score_profile_dimension import TrustScoreDimension
from indykite_sdk.model.trust_score_profile_update_frequency import UpdateFrequency


@dataclass
class TrustScoreProfileConfig:
    node_classification: str | None = None
    dimensions: list[TrustScoreDimension] = field(default_factory=list)
    schedule: float | None = None

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            "node_classification": str,
            "dimensions": lambda val: [TrustScoreDimension.deserialize(d) for d in val],
            "schedule": cls._validate_frequency,
        }

        # Process optional fields
        kwargs = {}
        for field_name, processor in all_fields.items():
            if field_name in fields:
                try:
                    kwargs[field_name] = processor(getattr(message_config, field_name))
                except Exception as e:
                    raise ValueError(f"Error processing field '{field_name}': {e}")

        return cls(**kwargs)

    @staticmethod
    def _validate_frequency(value):
        try:
            return UpdateFrequency(value).name
        except ValueError:
            raise TypeError(f"'{value}' is not a valid UpdateFrequency name")
