from dataclasses import dataclass, field
from typing import List, Optional

from indykite_sdk.model.knowledge_query_status import KnowledgeQueryStatus


@dataclass
class KnowledgeQueryConfig:
    query: Optional[str] = None
    status: Optional[float] = None
    policy_id: Optional[str] = None

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]
        print(fields)

        # Define processors for all fields
        all_fields = {
            'query': str,
            'status': cls._validate_status,
            'policy_id': str,
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
    def _validate_status(value):
        try:
            return KnowledgeQueryStatus(value).name
        except ValueError:
            raise TypeError(f"'{value}' is not a valid KnowledgeQueryStatus name")
