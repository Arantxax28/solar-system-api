from app.models.planets import Planet


def test_get_all_planets_with_empty_list(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_planets_with_populated_list(client, two_planets):
# Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

def test_get_one_planet_with_populated_list(client, two_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "planet y",
        "number_of_moons": 0
    }


def test_create_one_planet(client):
# Act
    response = client.post("/planets", json={
        "name": "Earth",
        "description": "planet z",
        "number_of_moons": 1
    })
    response_body = response.get_json()

    # Assert
    assert "id" in response_body 
    assert response.status_code == 201
    assert "message" in response_body
    planets = Planet.query.all()
    assert len(planets) == 1
    assert planets[0].name == "Earth"



def test_get_one_planet_with_empty_db_returns_404(client):
    response = client.get("/planets/1")
    assert response.status_code == 404

def test_get_non_existing_planet_with_populated_db_returns_404(client, two_planets):
    response = client.get("/planets/100")
    assert response.status_code == 404