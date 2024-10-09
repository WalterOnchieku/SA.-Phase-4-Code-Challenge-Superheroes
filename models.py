# models.py
from app import db  # Import db from app.py
from sqlalchemy_serializer import SerializerMixin

#===========================================================================================

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    super_name = db.Column(db.String(64), nullable=False)

    # Specify serialization rules to limit recursion depth
    serialize_rules = ('-hero_powers.hero', '-powers.heroes')

    # Relationships
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan', passive_deletes=True)
    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }

    def __repr__(self):
        return f"<Hero {self.name}>"

#===========================================================================================

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)  # Increased length for description

    # Specify serialization rules to limit recursion depth
    serialize_rules = ('-hero_powers.power', '-heroes.powers')

    # Relationships
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan', passive_deletes=True)
    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers')

    def __repr__(self):
        return f"<Power {self.name}>"

    @db.validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present.")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

#===========================================================================================

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(64), nullable=False)

    # Specify serialization rules to limit recursion depth
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # Foreign keys with cascading deletes
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    VALID_STRENGTHS = ['Strong', 'Weak', 'Average']

    def __repr__(self):
        return f"<HeroPower strength={self.strength}>"

    @db.validates('strength')
    def validate_strength(self, key, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError(f"Invalid strength: {value}. Must be one of {', '.join(self.VALID_STRENGTHS)}.")
        return value
        
#===========================================================================================