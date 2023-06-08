from pydantic import BaseModel, Field


class ApplicationWithAgentCredentialsCreate(BaseModel):
    app_space_id: str = Field(..., description="AppSpace gid id")
    tenant_id: str = Field(..., description="Tenant gid id")
    application_name: str = Field(..., description="Application display name")
    application_agent_name: str = Field(..., description="Application Agent name")
    application_agent_credentials_name: str = Field(..., description="Application Agent Credentials name")
