from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    name: str
    products: list

    model_config = ConfigDict(from_attributes=True)
