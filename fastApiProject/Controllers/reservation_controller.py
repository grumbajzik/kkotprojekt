from typing import Literal

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Auth.Dependencies import get_current_user
from Dtos.Response.reservation_dto import ReservationDto
from Servicies.reservation_service import ReservationService
from database import get_db
from Entities import User
from Dtos.Requests.reservation_create_dto import CreateReservationDto
from Dtos.Requests.reject_reservation import RejectReservationDto
from Dtos.Requests.return_reservation_dto import ReturnReservationDto

router = APIRouter(
    prefix="/reservations",
    tags=["Rezervace"]
)


def get_service(db: Session = Depends(get_db)):
    return ReservationService(db)


@router.post("/", status_code=201)
def create_reservation(
    dto: CreateReservationDto,
    service: ReservationService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(dto, current_user)


@router.post("/{reservation_id}/approve")
def approve_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.approve(reservation_id, current_user)


@router.post("/{reservation_id}/reject")
def reject_reservation(
    reservation_id: int,
    dto: RejectReservationDto,
    service: ReservationService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    service.reject(reservation_id, dto, current_user)


@router.post("/{reservation_id}/return")
def return_reservation(
    reservation_id: int,
    dto: ReturnReservationDto,
    service: ReservationService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    service.return_reservation(reservation_id, dto, current_user)


@router.get("", response_model=list[ReservationDto])
def get_reservations(
    view: Literal[
        "mine",
        "pending",
        "upcoming",
        "past",
        "active",
        "cancelled",
        "all"
    ] = "mine",
    user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_service)
):
    return service.get_by_view(view, user)
