"""Execute a ContX IQ knowledge query (graph read/write under a CIQ policy).

Requires INDYKITE_APPLICATION_CREDENTIALS[_FILE] and an ACTIVE knowledge query
(create one with ConfigClient.create_knowledge_query or in the IndyKite Hub).
Set END_USER_TOKEN to also resolve that end-user token to its graph node.
"""

import os
import sys

from indykite_sdk import CIQClient


def main(query_id: str) -> None:
    """Run the example against the given knowledge query."""
    with CIQClient() as client:
        response = client.execute(query_id, page_size=10)
        print(f"First page: {len(response.data)} records")
        for record in response.data:
            print(record.nodes or record.aggregate_values)

        total = sum(1 for _ in client.execute_iter(query_id, page_size=100))
        print(f"Total records across all pages: {total}")

        if user_token := os.environ.get("END_USER_TOKEN"):
            me = client.whoami(user_token)
            print(f"The token belongs to {me.type} {me.id}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gid:my-knowledge-query-id")
