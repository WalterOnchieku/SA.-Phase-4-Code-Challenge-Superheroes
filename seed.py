# seed.py
from random import choice as rc
from app import create_app, db  
from models import Hero, Power, HeroPower  

def seed_database():
    app = create_app()

    with app.app_context():
        print("Clearing db...")
        HeroPower.query.delete()
        Power.query.delete()
        Hero.query.delete()

        print("Seeding powers...")
        powers = [
            Power(name="Super Strength", description="Grants the wielder super-human physical strength."),
            Power(name="Flight", description="Allows the wielder to fly through the skies at supersonic speed."),
            Power(name="Super Senses", description="Enables the wielder to use their senses at a super-human level."),
            Power(name="Elasticity", description="Allows the wielder to stretch their body to extreme lengths."),
        ]
        db.session.add_all(powers)

        print("Seeding heroes...")
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)

        print("Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []
        for hero in heroes:
            power = rc(powers)
            hero_powers.append(
                HeroPower(hero=hero, power=power, strength=rc(strengths))
            )
        db.session.add_all(hero_powers)
        db.session.commit()

        print("Done seeding!")

if __name__ == '__main__':
    seed_database()
