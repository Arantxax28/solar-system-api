from crypt import methods
from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, number_of_moons):
        self.id = id
        self.name = name
        self.description = description
        self.number_of_moons = number_of_moons

planets = [
    Planet(1, "Mercury", "hot rocky planet", 0),
    Planet(2, "Venus", "planet without moons", 0),
    Planet(3, "Earth", "planet with human life", 1),
    Planet(4, "Mars", "red planet", 2),
    Planet(5, "Jupiter", "huge planet with red spot", 79),
    Planet(6, "Saturn", "planet with rings", 82),
    Planet(7, "Uranus", "ice giant planet", 27),
    Planet(8, "Neptune", "supersonic wind planet", 14)
]

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"error message":f"Planet {planet_id} invalid"},400))
    for planet in planets:
        if planet.id == planet_id:
            return planet
    abort(make_response({"error message":f"Could not find planet with id: {planet_id}."},404))

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

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)


    response = {
        "id" : planet.id,
        "name" : planet.name,
        "description" : planet.description,
        "number_of_moons" : planet.number_of_moons
    }
    return jsonify(response),200


        
