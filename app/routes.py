from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, number_of_moons):
        self.id = id
        self.name = name
        self.description = description
        self.number_of_moons = number_of_moons

planets = [
    Planet(1, "Venus", "planet without moons", 0),
    Planet(2, "Mercury", "hot rocky planet", 0),
    Planet(3, "Mars", "red planet", 2)
]

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

@planets_bp.route("", methods = ["GET"])
def get_all_planets():
    planet_response = []
    for planet in planets:
        planet_response.append({
            "id" : planet.id,
            "name" : planet.name,
            "description" : planet.description,
            "number_of_moons" : planet.number_of_moons
        })
    return jsonify(planet_response)