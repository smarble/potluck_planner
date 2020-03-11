"""Utility file to seed potluck_planner database"""

import datetime
from sqlalchemy import func

from model import User, Potluck, Dish, Type, UserDish, UserPotluck, PotluckDish, connect_to_db, db
from server import app


def load_users():
    """Load users into users table."""

    print("Users")

    lisa = User(fname="Lisa",
                lname="Kudrow",
                phone = 5555555,
                email = "lisa@gmail.com",
                password = "1",
                )

    serena = User(fname="Serena",
                lname="Williams",
                phone = 5555555,
                email = "serena@gmail.com",
                password = "2",
                )

    prince = User(fname="Prince",
                phone = 5555555,
                email = "prince@gmail.com",
                password = "3",
                )

    michael = User(fname="Michael",
                lname="Kohout",
                phone = 5555555,
                email = "michael@gmail.com",
                password = "4",
                )

    grace = User(fname="Grace",
                lname="Jones",
                phone = 5555555,
                email = "kim@gmail.com",
                password = "5",
                )

    ricardo = User(fname="Ricardo",
                lname="Montalban",
                phone = 5555555,
                email = "ricardo@gmail.com",
                password = "6",
                )

    pauly = User(fname="Pauly",
                lname="Shore",
                phone = 5555555,
                email = "pauly@gmail.com",
                password = "7",
                )

    bootsy = User(fname="Bootsey",
                lname="Collins",
                phone = 5555555,
                email = "bootsy@gmail.com",
                password = "8",
                )                                       

    # We need to add to the session or it won't ever be stored
    db.session.add_all([lisa, serena, prince, michael, grace, ricardo, pauly, bootsy])


    # Once we're done, we should commit our work
    db.session.commit()


def load_potlucks():
    """Load potlucks into potlucks table."""

    print("Potlucks")

    potluck1 = Potluck(potluck_name="Bootsy's Cosmic Cacophony Bash",
                # date= datetime(2020, 6, 5, 10, 20, 10, 10),
                address = "5678 Dark Matter Ln. Richmond Va, 88765",
                )

    potluck2 = Potluck(potluck_name="Serena's Summertime Soiree",
                # date= datetime(2020, 4, 11, 10, 20, 10, 10),
                address = "9422 Hard Green Ct. Pheonix AZ, 22098",
                )
                                

    # We need to add to the session or it won't ever be stored
    db.session.add_all([potluck1, potluck2])


    # Once we're done, we should commit our work
    db.session.commit()



def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
   
    # call your functions above
    load_users()
    load_potlucks()
    


    db.session.commit()