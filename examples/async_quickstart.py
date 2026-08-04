"""Async clients: concurrent authorization checks and a graph read.

Requires INDYKITE_APPLICATION_CREDENTIALS[_FILE].
"""

import asyncio

from indykite_sdk import AsyncAuthZENClient, AsyncDataSchemaClient


async def main() -> None:
    """Run the example."""
    async with AsyncAuthZENClient() as authzen, AsyncDataSchemaClient() as data_schema:
        decision, schema = await asyncio.gather(
            authzen.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt")),
            data_schema.read(),
        )
        print(f"Decision: {decision.decision}")
        print(f"Node types in the IKG: {schema.node_types}")


if __name__ == "__main__":
    asyncio.run(main())
