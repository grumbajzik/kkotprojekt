from pydantic import BaseModel, Field


class LoginDto(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=6)