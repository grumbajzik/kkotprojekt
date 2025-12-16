from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Auth.Dependencies import can_modify_user
from Auth.crypt_context import verify_password, hash_password
from Dtos.Requests.update_roles import UpdateRolesDto
from Dtos.Requests.user_update import UpdateUserDto
from Entities import User
from Repositories import user_repository
from Repositories.user_repository import get_by_login, create
from Auth.jwt import create_access_token


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def register(self, login: str, password: str, name: str):
        if get_by_login(self.db, login):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login již existuje")
        return create(self.db, login, password, name)

    def login(self, login: str, password: str):
        user = get_by_login(self.db, login)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Neplatné přihlašovací údaje")

        token = create_access_token({"user_id": user.id})
        return {"access_token": token, "token_type": "bearer", "user_id": user.id, "name": user.name}

    def update_user(self, user_id: int, dto: UpdateUserDto, current_user: User):
        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not current_user.is_admin and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user_repository.update_user(self.db, user, dto)

    def delete_user(self, user_id: int, current_user: User):
        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not current_user.is_admin and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        user_repository.delete(self.db, user)

    def update_roles(self, user_id: int, dto: UpdateRolesDto, current_user: User):
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admins only")

        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user_repository.update_roles(self.db, user, dto)

    def change_password(self, user_id: int, old_password: str, new_password: str, current_user: User):
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(old_password, user.password):
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        can_modify_user(current_user, user_id)



        return user


