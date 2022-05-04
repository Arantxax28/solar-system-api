import json
import re
from app import db
from app.models.planets import Planet
from flask import Blueprint, jsonify, abort, make_response, request

# class Planet:
#     def __init__(self, id, name, description, number_of_moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.number_of_moons = number_of_moons

# planets = [
#     Planet(1, "Mercury", "hot rocky planet", 0),
#     Planet(2, "Venus", "planet without moons", 0),
#     Planet(3, "Earth", "planet with human life", 1),
#     Planet(4, "Mars", "red planet", 2),
#     Planet(5, "Jupiter", "huge planet with red spot", 79),
#     Planet(6, "Saturn", "planet with rings", 82),
#     Planet(7, "Uranus", "ice giant planet", 27),
#     Planet(8, "Neptune", "supersonic wind planet", 14)
# ]
# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"error message":f"Planet {planet_id} invalid"},400))
#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
#     abort(make_response({"error message":f"Could not find planet with id: {planet_id}."},404))


planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

@planets_bp.route("", methods=["POST"])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"],
        number_of_moons=request_body["number_of_moons"]
    )
    db.session.add(new_planet)
    db.session.commit()

    return {"id": new_planet.id,
            "message": f"Succesfully created planet with id {new_planet.id}"
    } , 201


@planets_bp.route("", methods=["GET"])
def get_all_planets():
    params = request.args
    if "name" in params:
        name_name = params["name"]
        planets = Planet.query.filter_by(name=name_name)
    elif "description" in params:
        description_name = params["description"]
        #planets = Planet.query.filter(Planet.description.contains("planet"))
        planets = Planet.query.filter_by(description=description_name)
    elif "number_of_moons" in params:
        moons_value = params["number_of_moons"]
        planets = Planet.query.filter_by(number_of_moons=moons_value)
    else:
        planets = Planet.query.all()

    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "number_of_moons": planet.number_of_moons

            }
        )
    return jsonify(planets_response)

def get_planet_or_abort(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        response = {"message":f"Invalid id:{planet_id}"}
        abort(make_response(jsonify(response),400))
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        response = {"message":f"Could not find planet with id {planet_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_planet

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    # try: 
    #     planet_id = int(planet_id)
    # except ValueError:
    #     response = {
    #         "message" : f"Invalid id: {planet_id}"}
    #     return jsonify(response), 400
    # chosen_planet = Planet.query.get(planet_id)
    chosen_planet = get_planet_or_abort(planet_id)

    # if chosen_planet is None:
    #     response = {"message": f" Could not find a planet with id {planet_id}"}
    #     return jsonify(response), 404
    
    response = { "id" : chosen_planet.id,
                    "name": chosen_planet.name,
                    "description": chosen_planet.description,
                    "number_of_moons": chosen_planet.number_of_moons}
    return jsonify(response), 200

@planets_bp.route("/<planet_id>", methods = ["PUT"])
def replace_planet(planet_id):
    # try: 
    #     planet_id = int(planet_id)
    # except ValueError:
    #     response = {"message":f"Invalid id {planet_id}"}
    #     return jsonify(response), 400
    
    # chosen_planet = Planet.query.get(planet_id)

    # if chosen_planet is None:
    #     response = {"message": f"Could not find planet with id {planet_id}"}
    #     return jsonify(response), 404
    chosen_planet = get_planet_or_abort(planet_id)
    request_body = request.get_json()

    try:
        chosen_planet.name = request_body["name"]
        chosen_planet.description = request_body["description"]
        chosen_planet.number_of_moons = request_body["number_of_moons"]
    
    except KeyError:
        return {
            "message": "name, description, and number_of_moons are required"
        } , 400

    db.session.commit()

    return {
        "message": f"planet #{chosen_planet.id} successfully replaced"
    }, 200

@planets_bp.route("/<planet_id>", methods = ["DELETE"])
def delete_planet(planet_id):
    # try: 
    #     planet_id = int(planet_id)
    # except ValueError:
    #     response = {"message":f"Invalid id {planet_id}"}
    #     return jsonify(response), 400
    
    # chosen_planet = Planet.query.get(planet_id)

    # if chosen_planet is None:
    #     response = {"message": f"Could not find planet with id {planet_id}"}
    #     return jsonify(response), 404

    chosen_planet = get_planet_or_abort(planet_id)
    db.session.delete(chosen_planet)
    db.session.commit()

    return {
        "message": f"planet #{chosen_planet.id} successfully removed"
    }, 200



# @planets_bp.route("", methods = ["GET"])
# def get_all_planets():
#     planet_response = []
#     for planet in planets:
#         planet_response.append({
#             "id" : planet.id,
#             "name" : planet.name,
#             "description" : planet.description,
#             "number_of_moons" : planet.number_of_moons
#         })
#     return jsonify(planet_response)


        
