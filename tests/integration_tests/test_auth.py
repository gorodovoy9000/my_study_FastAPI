from src.service.auth import AuthService


def test_create_and_decode_access_token():
    # test data
    data = {"user_id": 1}
    # create token
    token = AuthService().create_access_token(data=data)
    # decode token
    payload = AuthService().decode_access_token(token)
    # test result is correct
    assert payload["user_id"] == 1
