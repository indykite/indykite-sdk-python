from dataclasses import dataclass, field, fields
from typing import Dict, List, Optional

from google.protobuf.json_format import MessageToDict

from indykite_sdk.model.event_sink_provider import EventSinkProvider
from indykite_sdk.model.event_sink_route import EventSinkRoute


@dataclass
class EventSinkConfig:
    providers: Dict[str, EventSinkProvider] = field(default_factory=dict)
    routes: List[EventSinkRoute] = field(default_factory=list)

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        message_dict = MessageToDict(message_config, preserving_proto_field_name=True)
        # Define processors for all fields

        all_fields = {
            'providers': lambda x: message_dict["providers"].copy(),
            'routes': lambda x: [route for route in message_dict["routes"]]
        }

        # Process optional fields
        kwargs = {}
        for field_name, processor in all_fields.items():
            if field_name in {f.name for f in fields(cls)}:
                try:
                    kwargs[field_name] = processor(getattr(message_config, field_name))
                except Exception as e:
                    raise ValueError(f"Error processing field '{field_name}': {e}")

        return cls(**kwargs)
