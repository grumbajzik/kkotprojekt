from pydantic import BaseModel

class UserDto(BaseModel):
    id: int
    login: str
    name: str
    is_admin: bool
    is_approver: bool

    class Config:
        from_attributes = True