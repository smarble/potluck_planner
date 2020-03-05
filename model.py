"""Models and database functions for Potluck Planner."""
from flask_sqlalchemy import SQLAlchemy
import correlation
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User table in potluck_planner database."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} fname={self.fname}>"


class Potluck(db.Model):
    """Potluck table in potluck_planner database."""

    __tablename__ = "potlucks"

    potluck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Potluck user_id={self.potluck_id} date={self.date} address={self.address}>"


class Dish(db.Model):
    """Dish table in potluck_planner database."""

    __tablename__ = "dishes"

    dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dish_name = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Dish dish_id={self.dish_id} dish_name={self.dish_name}>"


class UserDish(db.Model):
    """Users dishes table in potluck_planner database."""

    __tablename__ = "users_dishes"

    user_dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.dish_id'))
    


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserDish user_dish_id={self.user_dish_id} user_id={self.user_id} dish_id={self.dish_id}>"


class UserPotluck(db.Model):
    """Users dishes table in potluck_planner database."""

    __tablename__ = "users_potlucks"

    user_potluck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    potluck_id = db.Column(db.Integer, db.ForeignKey('potlucks.potluck_id'))
    


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserPotluck user_potluck_id={self.user_potluck_id} user_id={self.user_id} potluck_id={self.potluck_id}>"

class PotluckDishes(db.Model):
    """Users dishes table in potluck_planner database."""

    __tablename__ = "potlucks_dishes"

    potluck_dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    potluck_id = db.Column(db.Integer, db.ForeignKey('potlucks.potluck_id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.dish_id'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<PotluckDishes potluck_dish_id={self.potluck_dish_id} potluck_id={self.potluck_id} dish_id={self.dish_id}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # database name goes here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///potluck_planner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")

