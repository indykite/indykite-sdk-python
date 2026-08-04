"""Bootstrap a project -> application -> agent -> credential via the Config API.

Requires INDYKITE_SERVICE_ACCOUNT_CREDENTIALS[_FILE].
"""

from indykite_sdk import ConfigClient


def main() -> None:
    """Run the example."""
    with ConfigClient() as config:
        organization = config.read_current_organization()
        print(f"Organization: {organization.name} ({organization.id})")

        projects = config.list_projects(organization.id)
        print(f"Projects: {[project.name for project in projects]}")
        if not projects:
            print("Create a project in the IndyKite Hub first.")
            return
        project = projects[0]

        app = config.create_application("sdk-example-app", project.id, description="SDK v2 example")
        agent = config.create_application_agent(
            "sdk-example-agent", app.id, api_permissions=["Authorization", "Capture", "ContXIQ"]
        )
        credential = config.create_application_agent_credential(agent.id)
        # The credential JSON is returned exactly once - store it securely.
        agent_credentials = credential.as_credentials()
        print(f"Agent credential created (token starts with {agent_credentials.token[:8]}...)")

        # Etag-guarded update: read to get a fresh etag, then update.
        app_read = config.read_application(app.id)
        config.update_application(app.id, etag=app_read.etag, display_name="SDK Example App")

        # Clean up (delete also requires the current etag).
        credential_meta = config.read_application_agent_credential(credential.id)
        config.delete_application_agent_credential(credential.id, etag=credential_meta.etag)
        agent_read = config.read_application_agent(agent.id)
        config.delete_application_agent(agent.id, etag=agent_read.etag)
        app_read = config.read_application(app.id)
        config.delete_application(app.id, etag=app_read.etag)
        print("Cleaned up example resources")


if __name__ == "__main__":
    main()
