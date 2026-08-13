from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class AddressSchema(BaseModel):
    street: str = Field(..., json_schema_extra={"example": "123 Main St"})
    city: str = Field(..., json_schema_extra={"example": "Anytown"})
    state: str = Field(..., json_schema_extra={"example": "CA"})
    zip_code: str = Field(..., json_schema_extra={"example": "12345"})

class CreateUserRequestSchema(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )
    last_name: str = Field(
        min_length=2,
        max_length=50
    )
    email: EmailStr = Field(..., json_schema_extra={"example": "john.doe@example.com"})
    age: int = Field(..., ge=18, le=70)
    phone: str = Field(..., json_schema_extra={"example": "123-456-7890"})
    gender: Literal["Male", "Female"]
    address: AddressSchema
    is_active: bool = Field(default=True)
    role: Literal[
        "Admin",
        "Manager",
        "User"
    ]