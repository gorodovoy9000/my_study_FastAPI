async def test_get_facilities(ac):
    response = await ac.get("/api/v1/facilities")
    assert response.is_success
    data = response.json()["data"]
    assert isinstance(data, list)


async def test_facility_crud(ac):
    # create facility
    post_data = {"title": "wi-fi"}
    response = await ac.post("/api/v1/facilities", json=post_data)
    assert response.is_success
    response_data = response.json()
    assert isinstance(response_data, dict)
    created_data = response_data["data"][0]
    assert created_data["title"] == post_data["title"]

    # get facility
    response = await ac.get(f"/api/v1/facilities/{created_data['id']}")
    assert response.is_success

    # put facility
    put_data = {"title": "fi-wi"}
    response = await ac.put(f"/api/v1/facilities/{created_data['id']}", json=put_data)
    assert response.is_success

    # patch facility
    patch_data = {"title": "wf-ii"}
    response = await ac.patch(
        f"/api/v1/facilities/{created_data['id']}", json=patch_data
    )
    assert response.is_success

    # delete facility
    response = await ac.delete(f"/api/v1/facilities/{created_data['id']}")
    assert response.is_success
