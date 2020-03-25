"""Functions for potluck_planner."""
from model import User, Potluck, Dish, PotluckDish, UserPotluck, connect_to_db, db
from random import choice
from flask import Flask, render_template, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import update, func, distinct
from jinja2 import StrictUndefined

# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def start_here():
    """Home Page not in use."""

    return "Hi! This is the home page."


@app.route('/welcome')
def say_hello():
    """Welcome user and get first and last name."""

    return render_template("welcome.html")


@app.route('/greet')
def greet_person():
    """Greet user by first and last name. Query database to populate potluck names for choice buttons"""

    userFname = request.args.get("fname")
    userLname = request.args.get("lname")

    new_user = User(fname=userFname, lname=userLname)
    db.session.add(new_user)
    db.session.commit()

    potlucks = Potluck.query.all()
    


    return render_template("choosePotluck.html",
                           personFname=userFname,
                           personLname=userLname,
                           potlucks=potlucks
                           )


@app.route('/choosePotluck')
def choose_potluck_form():
    """Have user choose a potluck."""
    #getting the data from the html form from the "name=" attribute
    #the data from the "name=" attribute is the number of the potluck chosen
    potluck_id = request.args.get("potluck")

    #using the number from the html form to query a specific potluck
    potluck = Potluck.query.get(potluck_id)

    #make an instance of UserPotluck to add this user to the users_potlucks association table
    # new_user_potluck = UserPotluck(user_id= , potluck_id=potluck_id)
    # db.session.add(new_user_potluck)
    # db.session.commit()

    
    return render_template("choice_made.html", potluck=potluck)
    


#gets potluck.potluck_id (an int), passed from a form in choice_made.html
@app.route('/user_brings/<int:potluck_id>')
def add_dish(potluck_id):
    """Ask user what dish they will bring."""

    #using potluck_id that was passed into @app.route
    potluck = Potluck.query.get(potluck_id)

    dish_name = request.args.get("dish")
    dish_servings = request.args.get("servings")
    type_id = request.args.get("type")

    #use data from html form to make a new Dish instance, add and commit it
    new_dish = Dish(dish_name=dish_name, servings=dish_servings, type_id=type_id)
    db.session.add(new_dish)
    db.session.commit()

    #make an instance of PotluckDish to add this user to the potlucks_dishes association table
    # dish_id = Dish.query.filter(Dish.dish_name==dish_name).one()
    new_dish_id = new_dish.dish_id
    new_potluck_dish = PotluckDish(potluck_id=potluck_id, dish_id=new_dish_id)
    db.session.add(new_potluck_dish)
    db.session.commit()
    
    #use table relationships to get the type_name from the new_dish object
    type_name = new_dish.types.type_name

    
    return render_template("user_brings.html",
                           dish=dish_name,
                           servings=dish_servings,
                           potluck=potluck
                           )


if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")