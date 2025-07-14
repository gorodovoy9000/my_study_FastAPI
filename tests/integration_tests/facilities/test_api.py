


async def test_post_facilities(ac):
    create_data = {'title': "wi-fi"}
    response = await ac.post("/facilities", json=create_data)
    assert response.is_success
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "data" in response_data
    assert response_data['data']['title'] == create_data['title']


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.is_success
    assert isinstance(response.json(), list)
