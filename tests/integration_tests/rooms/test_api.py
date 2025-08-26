async def test_get_rooms(ac):
    response = await ac.get(
        "/api/rooms",
        params={
            "hotel_id": 1,
            "date_from": "2025-08-01",
            "date_to": "2025-08-10",
        },
    )
    print(response.json())
    assert response.is_success


async def test_room_crud(ac):
    # create room
    post_data = {
        "hotel_id": 1,
        "title": "Supermax",
        "description": "Maximum comfort, just like in prison",
        "price": 500,
        "quantity": 4,
        "facilities_ids": [1, 2],
    }
    response = await ac.post("/api/rooms", json=post_data)
    assert response.is_success
    response_data = response.json()
    assert isinstance(response_data, dict)
    created_data = response_data["data"]
    assert created_data["title"] == post_data["title"]

    # get room
    response = await ac.get(f"/api/rooms/{created_data['id']}")
    assert response.is_success

    # put room
    put_data = {
        "hotel_id": 1,
        "title": "Maximum Lux",
        "description": "Maximum luxury and comfort",
        "price": 600,
        "quantity": 4,
        "facilities_ids": [1, 2, 3],
    }
    response = await ac.put(f"/api/rooms/{created_data['id']}", json=put_data)
    assert response.is_success

    # patch room
    patch_data = {
        "quantity": 5,
        "facilities_ids": [1, 2],
    }
    response = await ac.patch(
        f"/api/rooms/{created_data['id']}", json=patch_data
    )
    assert response.is_success

    # patch only facilities
    patch_data = {"facilities_ids": [1, 3]}
    response = await ac.patch(
        f"/api/rooms/{created_data['id']}", json=patch_data
    )
    assert response.is_success

    # delete room
    response = await ac.delete(f"/api/rooms/{created_data['id']}")
    assert response.is_success
