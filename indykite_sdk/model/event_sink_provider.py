from dataclasses import dataclass

from indykite_sdk.model.azure_event_grid_sink_config import AzureEventGridSinkConfig
from indykite_sdk.model.azure_service_bus_sink_config import AzureServiceBusSinkConfig
from indykite_sdk.model.kafka_sink_config import KafkaSinkConfig


@dataclass
class EventSinkProvider:
    kafka: KafkaSinkConfig
    azure_event_grid: AzureEventGridSinkConfig
    azure_service_bus: AzureServiceBusSinkConfig

    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        fields = [desc.name for desc, val in message_config.ListFields()]

        # Define processors for all fields
        all_fields = {
            "kafka": KafkaSinkConfig,
            "azure_event_grid": AzureEventGridSinkConfig,
            "azure_service_bus": AzureServiceBusSinkConfig,
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
