from flask import Blueprint, jsonify, request
from models import Hero, HeroPower, Power  # Ensure all models are imported
from sqlalchemy.exc import IntegrityError  # Import IntegrityError for database-related errors

heroes_bp = Blueprint('heroes', __name__)

@heroes_bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [hero.to_dict() for hero in heroes]
    return jsonify(heroes_data), 200

@heroes_bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_powers = [
        {
            "id": hero_power.id,
            "hero_id": hero.id,
            "power_id": hero_power.power.id,
            "strength": hero_power.strength,
            "power": {
                "id": hero_power.power.id,
                "name": hero_power.power.name,
                "description": hero_power.power.description
            }
        }
        for hero_power in hero.hero_powers
    ]

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": hero_powers
    }
    
    return jsonify(hero_data), 200

@heroes_bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data), 200

@heroes_bp.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    
    return jsonify(power_data), 200

@heroes_bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()  # Get the JSON data from the request
    if not data or 'description' not in data:
        return jsonify({"errors": ["Invalid request body"]}), 400

    new_description = data['description']

    try:
        # Update the power's description
        power.description = new_description
        db.session.commit()  # Commit the changes to the database

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        
        return jsonify(power_data), 200

    except ValueError as e:
        # Catch validation errors raised in the model
        return jsonify({"errors": [str(e)]}), 422

# New route for creating a new HeroPower
@heroes_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()  # Get the JSON data from the request

    # Validate the required fields
    if not data or not all(k in data for k in ("strength", "power_id", "hero_id")):
        return jsonify({"errors": ["Invalid request body"]}), 400

    strength = data["strength"]
    power_id = data["power_id"]
    hero_id = data["hero_id"]

    # Validate that the Hero and Power exist
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        return jsonify({"errors": ["Hero or Power not found"]}), 404

    try:
        # Create a new HeroPower
        new_hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(new_hero_power)
        db.session.commit()  # Commit the new HeroPower to the database

        hero_power_data = {
            "id": new_hero_power.id,
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": new_hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }

        return jsonify(hero_power_data), 201  # 201 Created status

    except IntegrityError:
        db.session.rollback()  # Rollback if there is an integrity error
        return jsonify({"errors": ["validation errors"]}), 422
