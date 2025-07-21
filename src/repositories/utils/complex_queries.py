from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def query_vacant_rooms(
    date_from: date,
    date_to: date,
    hotel_id: int = None,
):
    cte_rooms_booked_result = (
        # FROM Bookings select rooms ids with counter
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        # filter bookings that intercepts with our date interval
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        # necessary grouping
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_booked_result")
    )

    cte_rooms_remaining_result = (
        # FROM Rooms select rooms ids with computed remaining rooms counter
        select(
            RoomsOrm.id.label("room_id"),
            (
                RoomsOrm.quantity
                - func.coalesce(cte_rooms_booked_result.c.rooms_booked, 0)
            ).label("rooms_remaining"),
        )
        .select_from(RoomsOrm)
        # join rooms with some bookings and totally free rooms
        .outerjoin(
            cte_rooms_booked_result, RoomsOrm.id == cte_rooms_booked_result.c.room_id
        )
        .cte("rooms_remaining_result")
    )

    # rooms filter subquery
    query_rooms_ids = select(RoomsOrm.id).select_from(RoomsOrm)
    # filter by hotel id if presented
    if hotel_id:
        query_rooms_ids = query_rooms_ids.filter_by(hotel_id=hotel_id)
    # label as subquery
    query_rooms_ids = query_rooms_ids.subquery(name="rooms_ids_of_hotel")

    # resulting rooms query
    vacant_rooms_ids = (
        # select from remaining rooms cte
        select(cte_rooms_remaining_result.c.room_id)
        .select_from(cte_rooms_remaining_result)
        # exclude fully booked rooms and filter ids by additional subquery
        .filter(
            cte_rooms_remaining_result.c.rooms_remaining > 0,
            cte_rooms_remaining_result.c.room_id.in_(query_rooms_ids),
        )
    )

    # print(vacant_rooms_ids.compile(compile_kwargs={'literal_binds': True}))

    return vacant_rooms_ids
