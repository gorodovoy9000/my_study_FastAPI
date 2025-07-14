


async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            'date_from': "2025-08-01",
            'date_to': "2025-08-10",
        }
    )
    assert response.is_success
    print(response.json())
