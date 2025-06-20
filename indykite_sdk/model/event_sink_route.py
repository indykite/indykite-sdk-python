from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KeyValuePair:
    key: str
    value: str

@dataclass
class KeysValues:
    key_value_pairs: Optional[KeyValuePair]
    event_type: str

@dataclass
class Filter:
    keys_values: Optional[KeysValues] = None

    def __post_init__(self):
        if self.keys_values is None:
            raise ValueError("Exactly one of 'event_type' or 'context_key_value' must be provided.")

@dataclass
class EventSinkRoute:
    provider_id: Optional[str] = None
    stop_processing: Optional[bool] = None
    filter: Optional[Filter] = None
    display_name: Optional[str] = None
    id: Optional[str] = None

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            'provider_id': str,
            'stop_processing': bool,
            'filter': Filter,
            'display_name': str,
            'id': str
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
