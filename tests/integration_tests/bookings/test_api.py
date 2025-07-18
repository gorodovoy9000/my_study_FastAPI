import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-08-01", "2025-08-10", 200),
    (1, "2025-08-02", "2025-08-11", 200),
    (1, "2025-08-03", "2025-08-12", 200),
    (1, "2025-08-04", "2025-08-13", 200),
    (1, "2025-08-05", "2025-08-14", 200),
    (1, "2025-08-06", "2025-08-15", 404),
    (1, "2025-08-17", "2025-08-25", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
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
