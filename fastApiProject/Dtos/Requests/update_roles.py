from pydantic import BaseModel


class UpdateRolesDto(BaseModel):
    is_admin: bool
    is_approver: bool
