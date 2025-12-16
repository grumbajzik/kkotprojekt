from sqlalchemy.orm import Session

from Auth.crypt_context import hash_password
from Dtos.Requests.update_roles import UpdateRolesDto
from Dtos.Requests.user_update import UpdateUserDto
from Entities.user import User
from passlib.hash import bcrypt_sha256


def get_all(db: Session):
    return db.query(User).all()


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()


def update_user(db: Session, user: User, dto: UpdateUserDto) -> User:
    if dto.name is not None:
        user.name = dto.name

    if dto.password is not None:
        user.password = dto.password  # hashuje SERVICE, ne repo

    db.commit()
    db.refresh(user)
    return user

def change_user(db: Session, user: User, password : str) -> User:


    if password is not None:# hashuje SERVICE, ne repo
        hashed_new_password = hash_password(password)
        user.password = hashed_new_password

    db.commit()
    db.refresh(user)
    return user



def create(db: Session, login: str, password: str, name: str, is_admin=False, is_approver=False):
    hashed_password = hash_password(password)
    user = User(
        login=login,
        password=hashed_password,
        name=name,
        is_admin=is_admin,
        is_approver=is_approver
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User):
    db.delete(user)
    db.commit()


def update_roles(db: Session, user: User, dto: UpdateRolesDto) -> User:
    user.is_admin = dto.is_admin
    user.is_approver = dto.is_approver

    db.commit()
    db.refresh(user)
    return user
