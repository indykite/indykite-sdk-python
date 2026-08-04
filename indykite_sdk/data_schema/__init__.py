"""Data Schema API - read the IKG data model in JGF v2 format."""

from indykite_sdk.data_schema.aio import AsyncDataSchemaClient
from indykite_sdk.data_schema.client import DataSchemaClient
from indykite_sdk.data_schema.models import DataSchema

__all__ = ["AsyncDataSchemaClient", "DataSchema", "DataSchemaClient"]
