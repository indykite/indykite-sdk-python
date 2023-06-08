from pydantic import BaseModel, Field


class TenantById(BaseModel):
    id: str = Field(..., description="gid")


class TenantCreate(BaseModel):
    issuer_id: str = Field(..., description="Issuer id")
    display_name: str = Field(..., description="Tenant display name")
    description: str = Field(..., description="Tenant description")
