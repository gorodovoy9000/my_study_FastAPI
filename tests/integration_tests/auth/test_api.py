import pytest


@pytest.mark.parametrize(
    "email, password",
    [
        # standard users
        ("best@syth.com", "red_saber"),
        ("the-best@bright.com", "blue_saber"),
        ("old-timer@aol.com", "pass_insert_here"),
        # test email already taken
    ],
)
async def test_auth_flow(email, password, ac):
    # register user
    response = await ac.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.is_success

    # login user
    response = await ac.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.is_success
    assert response.cookies["access_token"]

    # check auth/me return the user
    response = await ac.get("/api/auth/me")
    assert response.is_success
    response_payload = response.json()
    assert "id" in response_payload
    assert "password" not in response_payload
    assert "hashed_password" not in response_payload

    # logout user
    response = await ac.post("/api/auth/logout")
    assert response.is_success
    assert "access_token" not in response.cookies

    # check auth error after logout and get auth/me
    response = await ac.get("/api/auth/me")
    assert response.status_code == 401


async def test_already_registered(ac):
    response = await ac.post(
        "/api/auth/register",
        json={
            "email": "best@syth.com",
            "password": "red_saber",
        },
    )
    assert response.status_code == 409


async def test_invalid_password(ac):
    response = await ac.post(
        "/api/auth/login",
        json={
            "email": "the-best@bright.com",
            "password": "green_saber",
        },
    )
    assert response.status_code == 401
