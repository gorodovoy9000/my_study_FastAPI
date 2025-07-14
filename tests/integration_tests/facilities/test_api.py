


async def test_post_facilities(ac):
    data = [
        {'title': "wi-fi"},
        {'title': "tv"},
        {'title': "minibar"},
    ]
    for obj in data:
        response = await ac.post("/facilities", json=obj)
        print(response.json())
        assert response.is_success


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    print(response.json())
    assert response.is_success
