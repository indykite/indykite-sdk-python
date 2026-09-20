"""Make KBAC authorization decisions via the AuthZEN API.

Requires INDYKITE_APPLICATION_CREDENTIALS[_FILE] and an active KBAC policy.
"""

from indykite_sdk import AuthZENClient


def main() -> None:
    """Run the example."""
    with AuthZENClient() as client:
        result = client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
        print(f"ada CAN_DRIVE kitt: {result.decision}")

        batch = client.evaluations(
            [
                {"resource": {"type": "Car", "id": "kitt"}},
                {"resource": {"type": "Car", "id": "karr"}},
            ],
            subject=("Person", "ada"),
            action="CAN_DRIVE",
        )
        print(f"Batch decisions: {batch.decisions}")

        actions = client.search_action(("Person", "ada"), ("Car", "kitt"))
        print(f"ada may perform on kitt: {actions.action_names}")

        drivers = client.search_subject(("Car", "kitt"), "CAN_DRIVE", "Person")
        print(f"Who can drive kitt: {[subject.id for subject in drivers.results]}")

        # Needs the ReadAuthZConfigs API permission on the application agent.
        policies = client.policies(subject_type="Person")
        for policy in policies.results:
            print(f"Policy for {policy.subject_type} with tags {policy.tags}: {policy.policy.get('actions')}")


if __name__ == "__main__":
    main()
