from sqlalchemy import delete
import pytest

from src.models.bookings import BookingsOrm
from tests.conftest import get_db_null_pool


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        stmt = delete(BookingsOrm)
        await _db.session.execute(stmt)
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-02", "2025-08-11", 200),
        (1, "2025-08-03", "2025-08-12", 200),
        (1, "2025-08-04", "2025-08-13", 200),
        (1, "2025-08-05", "2025-08-14", 200),
        (1, "2025-08-06", "2025-08-15", 409),
        (1, "2025-08-17", "2025-08-25", 200),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):
    data = {
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    }
    response = await authenticated_ac.post("/bookings", json=data)
    if response.is_success:
        response_payload = response.json()
        assert isinstance(response_payload, dict)
        assert "data" in response_payload
    else:
        assert response.status_code == status_code


@pytest.mark.parametrize(
    "room_id, date_from, date_to, my_bookings_count",
    [
        (1, "2025-08-01", "2025-08-10", 1),
        (1, "2025-08-02", "2025-08-11", 2),
        (1, "2025-08-03", "2025-08-12", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    my_bookings_count,
    db,
    authenticated_ac,
    delete_all_bookings,
):
    # create booking
    data = {
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    }
    # test response data
    response = await authenticated_ac.post("/bookings", json=data)
    assert response.is_success
    response_payload = response.json()
    assert isinstance(response_payload, dict)
    assert "data" in response_payload
    # check my bookings
    response = await authenticated_ac.get("/bookings/me")
    assert response.is_success
    response_payload = response.json()
    assert isinstance(response_payload, list)
    assert len(response_payload) == my_bookings_count
