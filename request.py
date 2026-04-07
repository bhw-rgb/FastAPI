from pydantic import BaseModel, Field

class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    job: str = Field(..., min_length=2, max_length=10)