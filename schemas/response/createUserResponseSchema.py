from pydantic import BaseModel
from pydantic import EmailStr
from datetime import datetime
from typing import Literal




class AddressSchema(BaseModel):

    street: str

    city: str

    state: str

    zip_code: str

class CreateUserResponseSchema(BaseModel):

    id: int

    first_name: str

    last_name: str

    email: EmailStr

    age: int

    phone: str

    gender: Literal[
        "Male",
        "Female"
    ]

    address: AddressSchema

    is_active: bool

    role: Literal[
        "Admin",
        "Manager",
        "User"
    ]