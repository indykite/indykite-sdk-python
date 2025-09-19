from dataclasses import dataclass


@dataclass
class KeyValuePair:
    key: str
    value: str


@dataclass
class KeysValues:
    key_value_pairs: KeyValuePair | None
    event_type: str


@dataclass
class Filter:
    keys_values: KeysValues | None = None

    def __post_init__(self):
        if self.keys_values is None:
            raise ValueError("Exactly one of 'event_type' or 'context_key_value' must be provided.")


@dataclass
class EventSinkRoute:
    provider_id: str | None = None
    stop_processing: bool | None = None
    filter: Filter | None = None
    display_name: str | None = None
    id: str | None = None

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {"provider_id": str, "stop_processing": bool, "filter": Filter, "display_name": str, "id": str}

        # Process optional fields
        kwargs = {}
        for field_name, processor in all_fields.items():
            if field_name in fields:
                try:
                    kwargs[field_name] = processor(getattr(message_config, field_name))
                except Exception as e:
                    raise ValueError(f"Error processing field '{field_name}': {e}")

        return cls(**kwargs)
