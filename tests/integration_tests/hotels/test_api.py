async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-08-01",
            "date_to": "2025-08-10",
        },
    )
    print(response.json())
    assert response.is_success


async def test_hotel_crud(ac):
    # create hotel
    post_data = {
        "title": "Ukhovertka",
        "location": "Somewhere in jungle"
    }
    response = await ac.post("/hotels", json=post_data)
    assert response.is_success
    response_data = response.json()
    assert isinstance(response_data, dict)
    created_data = response_data["data"]
    assert created_data["title"] == post_data["title"]

    # get hotel
    response = await ac.get(f"/hotels/{created_data['id']}")
    assert response.is_success

    # put hotel
    put_data = {
        "title": "Nautilus",
        "location": "Submarine somewhere in ocean"
    }
    response = await ac.put(f"/hotels/{created_data['id']}", json=put_data)
    assert response.is_success

    # patch hotel
    patch_data = {
        "location": "Somewhere in pacific"
    }
    response = await ac.patch(f"/hotels/{created_data['id']}", json=patch_data)
    assert response.is_success

    # delete hotel
    response = await ac.delete(f"/hotels/{created_data['id']}")
    assert response.is_success

