from dataclasses import dataclass


@dataclass
class AzureEventGridSinkConfig:
    topic_endpoint: str | None = None
    access_key: str | None = None
    display_name: str | None = None

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {"topic_endpoint": str, "access_key": str, "display_name": str}

        # Process optional fields
        kwargs = {}
        for field_name, processor in all_fields.items():
            if field_name in fields:
                try:
                    kwargs[field_name] = processor(getattr(message_config, field_name))
                except Exception as e:
                    raise ValueError(f"Error processing field '{field_name}': {e}")

        return cls(**kwargs)
