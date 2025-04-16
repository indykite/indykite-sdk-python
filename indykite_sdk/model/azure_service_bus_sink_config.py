from dataclasses import dataclass
from typing import Optional


@dataclass
class AzureServiceBusSinkConfig:
    connection_string: Optional[str] = None
    queue_or_topic_name: Optional[str] = None


    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            'connection_string': str,
            'queue_or_topic_name': str
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
