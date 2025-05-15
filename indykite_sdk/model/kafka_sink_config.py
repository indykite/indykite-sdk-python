from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KafkaSinkConfig:
    brokers: List[str] = field(default_factory=list)
    topic: Optional[str] = None
    disable_tls: Optional[bool] = None
    tls_skip_verify: Optional[bool] = None
    username: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None


    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            'brokers': lambda val: [b for b in val],
            'topic': str,
            'disable_tls': bool,
            'tls_skip_verify': bool,
            'username': str,
            'password': str,
            'display_name': str
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
