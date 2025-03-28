from dataclasses import dataclass
from typing import List, Optional

from indykite_sdk.model.kafka_sink_config import KafkaSinkConfig

@dataclass
class EventSinkProvider:
    kafka: KafkaSinkConfig

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            'kafka': KafkaSinkConfig,
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


