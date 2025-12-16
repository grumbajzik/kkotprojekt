from pydantic import BaseModel, Field
from typing import Optional


class UpdateUserDto(BaseModel):
    name: Optional[str] = None
