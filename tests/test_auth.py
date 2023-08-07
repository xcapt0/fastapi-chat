from conftest import client


def test_register():
    response = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False,
        "username": "test"
    })

    response_data = response.json()

    assert response.status_code == 201
    assert "id" in response_data
    assert "test@gmail.com" == response_data["email"]
    assert False is response_data["is_superuser"] # Test if a non-superuser user is always registered
    assert "test" == response_data["username"]


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 200


def test_wrong_login_credentials():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "1234"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 400


def test_logout():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    logout_response = client.post("/auth/logout", headers={"Cookie": response.headers.get("set-cookie")})
    assert logout_response.status_code == 200
