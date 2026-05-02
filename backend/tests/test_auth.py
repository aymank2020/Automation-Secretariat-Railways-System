def _login(client, username: str, password: str):
    return client.post("/auth/login", json={"username": username, "password": password})


def test_login_success_with_initial_admin(client):
    r = _login(client, "testadmin", "test-admin-pw-strong")
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["username"] == "testadmin"
    assert body["user"]["seclevel"] == "admin"
    assert body["access_token"]


def test_login_wrong_password(client):
    r = _login(client, "testadmin", "wrong")
    assert r.status_code == 401


def test_register_requires_admin_token(client):
    """Public unauthenticated registration must be rejected."""
    r = client.post(
        "/auth/register",
        json={"username": "evil", "password": "evil-pw-1234", "seclevel": "admin"},
    )
    assert r.status_code in (401, 403)


def test_register_with_admin_can_create_user(client):
    login = _login(client, "testadmin", "test-admin-pw-strong").json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/auth/register",
        json={"username": "alice", "password": "alice-pw-1234", "seclevel": "user"},
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["username"] == "alice"
    assert r.json()["seclevel"] == "user"


def test_register_seclevel_is_sanitised(client):
    """An admin can elevate a user but values outside the allowed set fall back to 'user'."""
    login = _login(client, "testadmin", "test-admin-pw-strong").json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/auth/register",
        json={"username": "bob", "password": "bob-pw-12345", "seclevel": "superuser"},
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["seclevel"] == "user"
