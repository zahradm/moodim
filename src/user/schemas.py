from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


class UserSerialiser(UserSchema):
    class Config:
        from_attributes = True


class UserSchemaUpdate(BaseModel):
    first_name: str
    last_name: str
    password: str
