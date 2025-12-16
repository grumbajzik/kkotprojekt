from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Entities import Reservation, User
from Repositories import reservation_repository
from Dtos.Requests.reservation_create_dto import CreateReservationDto
from Dtos.Requests.reject_reservation import RejectReservationDto
from Dtos.Requests.return_reservation_dto import ReturnReservationDto
from datetime import datetime, date
from Auth.Dependencies import approver_only, enable_only

class ReservationService:

    def __init__(self, db: Session):
        self.db = db

    def create(self, dto: CreateReservationDto, current_user: User):
        reservation = Reservation(
            customer_id=current_user.id,
            reservation_date_from=dto.reservation_date,
            created_date=datetime.utcnow()
        )

        reservation = reservation_repository.create_reservation(self.db, reservation)
        reservation_repository.add_items(
            self.db,
            reservation.id,
            dto.equipment_item_ids
        )
        return reservation

    def approve(self, reservation_id: int, current_user: User):
        if not current_user.is_approver:
            raise HTTPException(status_code=403, detail="Approver only")

        reservation = reservation_repository.get_by_id(self.db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        return reservation_repository.approve(
            self.db,
            reservation,
            current_user.id
        )

    def reject(
        self,
        reservation_id: int,
        dto: RejectReservationDto,
        current_user: User
    ):
        if not current_user.is_approver:
            raise HTTPException(status_code=403, detail="Approver only")

        reservation = reservation_repository.get_by_id(self.db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        reservation_repository.cancel(self.db, reservation)
        reservation_repository.add_comment(
            self.db,
            text=dto.reason,
            user_id=current_user.id,
            reservation_id=reservation_id
        )

    def return_reservation(
        self,
        reservation_id: int,
        dto: ReturnReservationDto,
        current_user: User
    ):
        if not current_user.is_approver:
            raise HTTPException(status_code=403, detail="Approver only")

        reservation = reservation_repository.get_by_id(self.db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        reservation_repository.mark_returned(self.db, reservation)
        reservation_repository.add_comment(
            self.db,
            text=dto.comment,
            user_id=current_user.id,
            reservation_id=reservation_id
        )

    def get_by_view(self, view: str, user: User):
        match view:
            case "mine":
                return reservation_repository.mine(self.db, user.id)

            case "pending":
                approver_only(user)
                return reservation_repository.pending(self.db)

            case "upcoming":
                return reservation_repository.upcoming(self.db, user.id)

            case "past":
                return reservation_repository.past(self.db, user.id)

            case "active":
                approver_only(user)
                return reservation_repository.active(self.db)

            case "cancelled":
                return reservation_repository.cancelled(self.db)

            case "all":
                enable_only(user)
                return reservation_repository.all_reservations(self.db)

            case _:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid view"
                )
