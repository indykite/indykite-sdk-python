from pydantic import BaseModel, Field


class AppSpaceById(BaseModel):
    id: str = Field(..., description="gid")


class AppSpaceCreate(BaseModel):
    customer_id: str = Field(..., description="Customer gid id")
    display_name: str = Field(..., description="AppSpace display name")
    description: str = Field(..., description="AppSpace description")
