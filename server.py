"""Functions for Potluck Planner."""
from model import User, Potluck, Dish, PotluckDish, connect_to_db, db
from random import choice
from flask import Flask, render_template, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import update, func
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

AWESOMENESS = [
    'awesome', 'terrific', 'fantastic', 'neato', 'fantabulous', 'wowza',
    'oh-so-not-meh', 'brilliant', 'ducky', 'coolio', 'incredible', 'wonderful',
    'smashing', 'lovely'
]


@app.route('/')
def start_here():
    """Display homepage."""

    return "Hi! This is the home page."


@app.route('/hello')
def say_hello():
    """Say hello to user."""

    return render_template("welcome.html")


@app.route('/greet')
def greet_person():
    """Greet user."""

    userFname = request.args.get("fname")
    userLname = request.args.get("lname")

    new_user = User(fname=userFname, lname=userLname)
    db.session.add(new_user)
    db.session.commit()


    return render_template("choosePotluck.html",
                           personFname=userFname,
                           personLname=userLname)


@app.route('/choosePotluck')
def show_madlib_form():
    """Show form to play madlibs or say goodbye."""

    play_game = request.args.get("play")
    

    if play_game == "yes":
        #select * from dishes where (potlucks.potluck_id = 1)
        potluck1Dishes = Dish.query.filter(Dish.potlucks.any(potluck_id=1)).all()

        # Same as below, but literal: dish_names = [item.dish_name for item in potluck1Dishes]
        dish_names = []
        for item in potluck1Dishes:
            dish_names.append(item.dish_name)

        return render_template("game.html", potluck1Dishes=potluck1Dishes, dish_names=dish_names)
    else:

        # potlucks table query get one instance with id #2. 
        # That instance has an attribute named dishes(defined in your model). 
        # returns every dish associated with potluck #2 in the potlucks_dishes association table.
        # potluck2Dishes2 = Potluck.query.get(2).dishes
        
        potluck2Dishes = Dish.query.filter(Dish.potlucks.any(potluck_id=2)).all()
        # Same as below, but literal: dish_names = [item.dish_name for item in potluck1Dishes]
        dish_names = []
        for item in potluck2Dishes:
            dish_names.append(item.dish_name)

        potluck2Dishes = PotluckDish.query.filter(PotluckDish.potluck_id == 2).all()
        return render_template("secondChoice.html", potluck2Dishes=potluck2Dishes, dish_names=dish_names)


@app.route('/madlib')
def show_madlib():
    """Show resulting mablib."""

    name = request.args.get("person")
    color = request.args.get("color")
    noun = request.args.get("noun")
    adjective = request.args.get("adjective")

    return render_template("madlib.html",
                           person=name,
                           color=color,
                           noun=noun,
                           adjective=adjective,
                           )


if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")