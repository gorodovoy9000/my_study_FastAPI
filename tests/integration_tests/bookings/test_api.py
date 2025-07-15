async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_many_filtered(limit=1))[0].id
    data = {
        "room_id": room_id,
        "date_from": "2025-08-01",
        "date_to": "2025-08-10",
    }
    response = await authenticated_ac.post("/bookings", json=data)
    assert response.is_success
    response_payload = response.json()
    assert isinstance(response_payload, dict)
    assert "data" in response_payload
