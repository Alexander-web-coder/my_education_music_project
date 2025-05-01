from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

#client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_login = fake.first_name()
client.fake_title = " ".join(fake.words(2))
client.fake_author = f"{fake.first_name()} {fake.first_name()}"
client.fake_genre = fake.word(ext_word_list=("pop", "rock", "jazz", "classic"))
client.new_user_id = 0
client.auth_token = ""
client.new_track_id = 0


def test_create_user():
    response = client.post("/users/create_user",
                           json={"login": client.fake_login,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 201
    client.new_user_id = response.json()


def test_token():
    response = client.post("/users/token",
                           data={"username": client.fake_login,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 200
    client.auth_token = response.json()['access_token']

def test_create_track():
    response = client.post("/tracks/create_track",
                           json={"title": client.fake_title,
                                 "author": client.fake_author,
                                 "genre": client.fake_genre}
    )
    assert response.status_code == 201
    client.new_track_id = response.json()['id']

def test_set_rating():
    response = client.patch("/ratings/set_rating",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"track_id": client.new_track_id,
                                "estimate": 5})
    assert response.status_code == 201
    # assert response.json() == client.new_user_id

def test_create_track_fail():
    response = client.post("/tracks/create_track",
                           json={"title": client.fake_title,
                                 "author": client.fake_author,
                                 "genre": client.fake_genre}
    )
    assert response.status_code == 400


def test_get_full_list():
    response = client.get("/tracks/get_full_list")
    assert response.status_code == 200
    #client.new_track_id = response.json()['id']

def test_delete_track():
    response = client.delete("/tracks/delete_track",
                             params={"track_id": client.new_track_id})

    assert response.status_code == 204
    # client.new_track_id = response.json()['id']

def test_delete_track_fail():
    response = client.delete("/tracks/delete_track",
                             params={"track_id": client.new_track_id})

    assert response.status_code == 400

def test_get_main():
    response = client.get("/")
    assert response.status_code == 200


