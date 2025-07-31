from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchemas(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int | str
    password_hash: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchemas(BaseModel):
    """"""

class UserReadSchemas(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchemas(BaseModel):
    id: int


