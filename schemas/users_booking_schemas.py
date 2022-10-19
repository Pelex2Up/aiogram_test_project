from datetime import datetime
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    f_name: str
    l_name: str
    date: datetime = Field(default=datetime.now())
    time: str
    num_of_people: str


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)