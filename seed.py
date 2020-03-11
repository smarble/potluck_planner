"""Utility file to seed potluck_planner database"""

import datetime
from sqlalchemy import func

from model import User, Potluck, Dish, Type, UserDish, UserPotluck, PotluckDish, connect_to_db, db
from server import app


def load_users():
    """Load users into users table."""

    print("Users")

    paul = User(fname="Paul",
                lname="Reubens",
                phone = 5555555,
                email = "paul@gmail.com",
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
    db.session.add_all([paul, serena, prince, michael, grace, ricardo, pauly, bootsy])


    # Once we're done, we should commit our work
    db.session.commit()


def load_potlucks():
    """Load potlucks into potlucks table."""

    print("Users")

    potluck1 = User(fname="Paul",
                lname="Reubens",
                phone = 5555555,
                email = "paul@gmail.com",
                password = "1",
                )

    potluck2 = User(fname="Serena",
                lname="Williams",
                phone = 5555555,
                email = "serena@gmail.com",
                password = "2",
                )
                                

    # We need to add to the session or it won't ever be stored
    db.session.add_all([paul, serena, prince, michael, grace, ricardo, pauly, bootsy])


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
   
    load_users()
    


    db.session.commit()