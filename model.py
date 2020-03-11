"""Models and database functions for Potluck Planner."""
from flask_sqlalchemy import SQLAlchemy
# not using correlation?
# import correlation
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """users table in potluck_planner database."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(), nullable=False)
    lname = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    password = db.Column(db.String(), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} fname={self.fname}>"


class Potluck(db.Model):
    """potlucks table in potluck_planner database."""

    __tablename__ = "potlucks"

    potluck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    potluck_name = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Potluck potluck_id={self.potluck_id} potluck_name={self.potluck_name}>"


class Dish(db.Model):
    """dishes table in potluck_planner database."""

    __tablename__ = "dishes"

    dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dish_name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey('types.type_id'))
    servings = db.Column(db.Integer, nullable=True)

    something = db.relationship("Type", backref="dishes")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Dish dish_id={self.dish_id} dish_name={self.dish_name}>"


class Type(db.Model):
    """types table in potluck_planner database."""

    __tablename__ = "types"

    type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Type type_id={self.type_id} type_name={self.type_name}>"        


class UserDish(db.Model):
    """users_dishes table in potluck_planner database."""

    __tablename__ = "users_dishes"

    user_dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.dish_id'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserDish user_dish_id={self.user_dish_id} user_id={self.user_id} dish_id={self.dish_id}>"


class UserPotluck(db.Model):
    """Users_potlucks table in potluck_planner database."""

    __tablename__ = "users_potlucks"

    user_potluck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    potluck_id = db.Column(db.Integer, db.ForeignKey('potlucks.potluck_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserPotluck user_potluck_id={self.user_potluck_id} user_id={self.user_id} potluck_id={self.potluck_id}>"


class PotluckDish(db.Model):
    """potlucks_dishes table in potluck_planner database."""

    __tablename__ = "potlucks_dishes"

    potluck_dish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    potluck_id = db.Column(db.Integer, db.ForeignKey('potlucks.potluck_id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.dish_id'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<PotluckDish potluck_dish_id={self.potluck_dish_id} potluck_id={self.potluck_id} dish_id={self.dish_id}>"



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # database name goes below: 'postgresql:///database_name'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///potluck_planner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    db.create_all()
    #db.drop()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    
   
    from server import app

    connect_to_db(app)
    print("Connected to DB.")

