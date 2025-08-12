async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.is_success
    assert isinstance(response.json(), list)


async def test_facility_crud(ac):
    # create facility
    post_data = {"title": "wi-fi"}
    response = await ac.post("/facilities", json=post_data)
    assert response.is_success
    response_data = response.json()
    assert isinstance(response_data, dict)
    created_data = response_data["data"]
    assert created_data["title"] == post_data["title"]

    # get facility
    response = await ac.get(f"/facilities/{created_data['id']}")
    assert response.is_success

    # put facility
    put_data = {"title": "fi-wi"}
    response = await ac.put(f"/facilities/{created_data['id']}", json=put_data)
    assert response.is_success

    # patch facility
    patch_data = {"title": "wf-ii"}
    response = await ac.patch(f"/facilities/{created_data['id']}", json=patch_data)
    assert response.is_success

    # delete facility
    response = await ac.delete(f"/facilities/{created_data['id']}")
    assert response.is_success
