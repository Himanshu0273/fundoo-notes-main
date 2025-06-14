# Test user registration
def test_register_user_success(client, user_payload):
    res = client.post("/signup", json=user_payload)
    assert res.status_code == 201
    assert res.json()["username"] == user_payload["username"]


# Test for duplicate emails
def test_user_duplicate_email(client, user_payload):
    res1 = client.post("/signup", json=user_payload)
    assert res1.status_code == 201

    res2 = client.post("/signup", json=user_payload)
    assert res2.status_code == 409


# Another way to check duplicate emails
# #Test for duplicate emails
# def test_user_duplicate_email(client, user_payload):
# assert user_payload["email"] == "test@gm.com"
