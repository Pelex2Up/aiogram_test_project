from datetime import datetime, date
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    f_name: str
    l_name: str
    date: str #datetime = Field(default=datetime.now())
    time: str
    num_of_people: int


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)