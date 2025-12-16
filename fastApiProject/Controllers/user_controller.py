from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from Auth.Dependencies import get_current_user, can_modify_user, is_admin
from Dtos.Requests.login_dto import LoginDto
from Dtos.Requests.register_dto import RegisterDto
from Dtos.Requests.update_roles import UpdateRolesDto
from Dtos.Requests.user_update import UpdateUserDto
from Dtos.Response.user_dto import UserDto
from Entities import User
from Servicies.user_service import UserService
from database import get_db
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/users",
    tags=["Uživatelé"]
)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.get("/register")
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_form(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    service: UserService = Depends(get_user_service)
):
    service.register(login, password, name)
    return RedirectResponse(url="/users/login", status_code=302)


@router.get("/login")
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_form(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    service: UserService = Depends(get_user_service)
):
    try:
        service.login(login, password)
        return RedirectResponse(url="/", status_code=302)
    except Exception:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Neplatné přihlašovací údaje."}
        )


from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Entities import User
from Servicies.user_service import UserService
from Auth.Dependencies import get_current_user
from Dtos.Requests.user_update import UpdateUserDto

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/users",
    tags=["Uživatelé"]
)

def get_user_service(db=Depends(get_db)):
    return UserService(db)

@router.get("/me/profile")
def show_profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("me.html", {"request": request, "user": current_user})

@router.get("/me/update")
def show_update_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("me_update.html", {"request": request, "user": current_user})

@router.post("/me/update")
def update_profile(
    request: Request,
    name: str = Form(...),
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    dto = UpdateUserDto(name=name)
    service.update_user(current_user.id, dto, current_user)
    return RedirectResponse(url="/users/me/profile", status_code=302)

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Entities import User
from Servicies.user_service import UserService
from Auth.Dependencies import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/users",
    tags=["Uživatelé"]
)

def get_user_service(db=Depends(get_db)):
    return UserService(db)

# ... ostatní endpointy ...

@router.get("/me/change-password")
def show_change_password_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("me_change_password.html", {"request": request, "user": current_user})

@router.post("/me/change-password")
def change_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    try:
        service.change_password(current_user.id, old_password, new_password)
        return RedirectResponse(url="/users/me/profile", status_code=302)
    except Exception as e:
        return templates.TemplateResponse(
            "me_change_password.html",
            {"request": request, "user": current_user, "error": str(e)}
        )

@router.post("/me/delete")
def delete_profile(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    service.delete_user(current_user.id, current_user)
    return RedirectResponse(url="/users/logout", status_code=302)


@router.put("/{user_id}/roles", response_model=UserDto)
def update_roles(
    user_id: int,
    dto: UpdateRolesDto,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
    ):
    is_admin(current_user)
    return service.update_roles(user_id, dto, current_user)
