"""Functions for potluck_planner."""
from model import User, Potluck, Dish, PotluckDish, connect_to_db, db
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
    """Display homepage."""

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
    
    #returns an object with potluck_id#1
    potluck1 = Potluck.query.filter(Potluck.potluck_id=='1').one()
    #returns the name of potluck #1
    potluck1_name = potluck1.potluck_name
    potluck1_address = potluck1.address

    #returns the users attribute of potluck1
    potluck1_users = potluck1.users

    # as a list comprehension: names = [(i.fname + i.lname + "...") for i in potluck1_users]
    
    names = []
    for i in potluck1_users:
        names.append(i.fname)
        names.append(i.lname)
        names.append("...")

    # potluck1_users_names = names
    potluck1_users_names = " ".join(names) + "."

    #returns an object with potluck_id#2
    potluck2 = Potluck.query.filter(Potluck.potluck_id=='2').one()
    #returns the name of potluck #2
    potluck2_name = potluck2.potluck_name
    potluck2_address = potluck2.address

    #returns the users attribute of potluck2
    potluck2_users = potluck2.users
    
    # as a list comprehension: names = [(i.fname + " " + i.lname) for i in potluck2_users]
    names = []
    for i in potluck2_users:
        names.append(i.fname)
        names.append(i.lname)
        names.append("...")
    

    # potluck2_users_names = names
    potluck2_users_names = " ".join(names) + "."





    return render_template("choosePotluck.html",
                           personFname=userFname,
                           personLname=userLname,
                           potluck1_name = potluck1_name,
                           potluck2_name = potluck2_name,
                           potluck1_address = potluck1_address,
                           potluck2_address = potluck2_address,
                           potluck1_users_names = potluck1_users_names,
                           potluck2_users_names = potluck2_users_names
                           )


@app.route('/choosePotluck')
def choose_potluck_form():
    """Have user choose a potluck."""

    play_game = request.args.get("play")
    

    if play_game == "1":
       
        #returns an object with potluck_id#1
        potluck1 = Potluck.query.filter(Potluck.potluck_id=='1').one()

        #returns the name of potluck #1
        potluck1_name = potluck1.potluck_name

        #returns a list of objects: dishes associated with potluck1
        potluck1Dishes = potluck1.dishes

        #as a list comprehension: names = [i.dish_name for i in potluck1Dishes]
        names = []
        for i in potluck1Dishes:
           names.append(i.dish_name)

        dish_names = ", ".join(names) + "."
           
        return render_template("firstChoice.html", potluck1_name = potluck1_name, potluck1Dishes=potluck1Dishes, dish_names=dish_names)

    elif play_game == "2":
        
        potluck2 = Potluck.query.filter(Potluck.potluck_id=='2').one()

        potluck2_name = potluck2.potluck_name

        potluck2Dishes = potluck2.dishes

        #as a list comprehension: names = [i.dish_name for i in potluck1Dishes]
        names = []
        for i in potluck2Dishes:
           names.append(i.dish_name)

        dish_names = ", ".join(names) + "."

        return render_template("secondChoice.html", potluck2_name = potluck2_name, potluck2Dishes=potluck2Dishes, dish_names=dish_names)



if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")