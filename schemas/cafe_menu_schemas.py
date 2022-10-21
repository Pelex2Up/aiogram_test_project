from pydantic import BaseModel, Field


class MenuSchema(BaseModel):
    food_photo: str
    food_name: str
    food_price: str
    food_compound: str


class MenuInDBSchema(MenuSchema):
    id: int = Field(ge=1)
