from sqlalchemy.orm import Session
from Entities import Reservation, EquipmentItemReservation, Comment
from datetime import datetime,date


def create_reservation(db: Session, reservation: Reservation):
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def add_items(db: Session, reservation_id: int, item_ids: list[int]):
    for item_id in item_ids:
        db.add(
            EquipmentItemReservation(
                reservation_id=reservation_id,
                equipment_item_id=item_id
            )
        )
    db.commit()


def get_by_id(db: Session, reservation_id: int) -> Reservation | None:
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


def approve(db: Session, reservation: Reservation, approver_id: int):
    reservation.approved = True
    reservation.approver_id = approver_id
    reservation.approved_date = datetime.utcnow()
    db.commit()
    db.refresh(reservation)
    return reservation


def cancel(db: Session, reservation: Reservation):
    reservation.cancelled = True
    db.commit()


def mark_returned(db: Session, reservation: Reservation):
    reservation.returned_date = datetime.utcnow()
    db.commit()


def add_comment(
    db: Session,
    text: str,
    user_id: int,
    reservation_id: int
):
    comment = Comment(
        text=text,
        user_id=user_id,
        reservation_id=reservation_id
    )
    db.add(comment)
    db.commit()


def mine(db: Session, user_id: int):
    return (
        db.query(Reservation)
        .filter(Reservation.customer_id == user_id)
        .order_by(Reservation.reservation_date.desc())
        .all()
    )


def pending(db: Session):
    return (
        db.query(Reservation)
        .filter(
            Reservation.approved == False,
            Reservation.cancelled == False
        )
        .order_by(Reservation.created_date.desc())
        .all()
    )


def upcoming(db: Session, user_id: int):
    today = date.today().isoformat()
    return (
        db.query(Reservation)
        .filter(
            Reservation.customer_id == user_id,
            Reservation.reservation_date >= today
        )
        .order_by(Reservation.reservation_date)
        .all()
    )


def past(db: Session, user_id: int):
    today = date.today().isoformat()
    return (
        db.query(Reservation)
        .filter(
            Reservation.customer_id == user_id,
            Reservation.reservation_date < today
        )
        .order_by(Reservation.reservation_date.desc())
        .all()
    )


def active(db: Session):
    return (
        db.query(Reservation)
        .filter(
            Reservation.approved == True,
            Reservation.returned_date == None
        )
        .order_by(Reservation.reservation_date)
        .all()
    )


def cancelled(db: Session):
    return (
        db.query(Reservation)
        .filter(Reservation.cancelled == True)
        .order_by(Reservation.reservation_date.desc())
        .all()
    )


def all_reservations(db: Session):
    return (
        db.query(Reservation)
        .order_by(Reservation.reservation_date.desc())
        .all()
    )


def add_comment(db: Session, text: str, user_id: int, reservation_id: int):
    comment = Comment(
        text=text,
        user_id=user_id,
        reservation_id=reservation_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment