"""Demo app using SQLAlchemy."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pet #need to import db functionality from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db' #specifies that you are using postgres, and name of db
#specify which db to use
#run this line before the db code on line 13!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #takes up more time, but will be deprecated so we set it 
#to false to avoid the warning
app.config['SQLALCHEMY_ECHO'] = True #helpful for debugging, shows underlying SQL statements that are run.

connect_db(app) #call the fn from models.py

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route("/")
def list_pets():
    """List pets and show add form."""

    pets = Pet.query.all()
    return render_template("list.html", pets=pets)


@app.route("/", methods=["POST"])
def add_pet():
    """Add pet and redirect to list."""

    name = request.form['name']
    species = request.form['species']
    hunger = request.form['hunger']
    hunger = int(hunger) if hunger else None

    pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(pet)
    db.session.commit()

    return redirect(f"/{pet.id}")


@app.route("/<int:pet_id>")
def show_pet(pet_id):
    """Show info on a single pet."""

    pet = Pet.query.get_or_404(pet_id)
    return render_template("detail.html", pet=pet)
