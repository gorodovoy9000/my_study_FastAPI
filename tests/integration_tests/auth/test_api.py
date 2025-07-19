import pytest


@pytest.mark.parametrize("username, email, password", [
    # standard users
    ("darth_vader", "best@syth.com", "red_saber"),
    ("obi_van", "the-best@bright.com", "blue_saber"),
    ("yoda", "old-timer@aol.com", "pass_insert_here"),
    # test email already taken
])
async def test_auth_flow(
        username, email, password,
        ac
):
    # register user
    response = await ac.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
    })
    assert response.is_success

    # login user
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.is_success
    assert response.cookies['access_token']

    # check auth/me return the user
    response = await ac.get("auth/me")
    assert response.is_success
    response_payload = response.json()
    assert response_payload['username'] == username
    assert "id" in response_payload
    assert "password" not in response_payload
    assert "hashed_password" not in response_payload

    # logout user
    response = await ac.post("auth/logout")
    assert response.is_success
    assert not response.cookies.get('access_token')

    # check auth error after logout and get auth/me
    response = await ac.get("auth/me")
    assert response.status_code == 401


async def test_already_registered(ac):
    response = await ac.post("/auth/register", json={
        "username": "emperor",
        "email": "best@syth.com",
        "password": "red_saber",
    })
    assert response.status_code == 422


async def test_invalid_password(ac):
    response = await ac.post("/auth/login", json={
        "email": "the-best@bright.com",
        "password": "green_saber",
    })
    assert response.status_code == 401
