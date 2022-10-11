"""Demo file showing off a model for SQLAlchemy."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
#run SQLAlchemy, whatever is returned will be stored in db var



def connect_db(app): #makes it so we can call this logic to connect to a db from app.py, 
    # """Connect to database.""" we don't want this tobe called every time we run app.py; just a best-practice 

    db.app = app #associate flask application w/ db variable
    db.init_app(app) #What does this method do?

#define models below... essentially schema
#create a special type of class, which inherits a sqlalchemy class 
class Pet(db.Model):
    """Pet."""
    #making a new pet that we would insert into the table

    __tablename__ = "pets" #specify name of table to be created in SQL db- PLURALIZE
    #define each indiv. column w/db.Column(db.NameOfType--UseSQLName)
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50), #can pass in max length for string
                     nullable=False, #opposite of not null, every val will be NULL unless we set this to false (meaning name can NOT be NULL)
                     unique=True)
    species = db.Column(db.String(30), nullable=True) #nullable defaults to True... this is unnecessary
    hunger = db.Column(db.Integer, nullable=False, default=20) # add default value
    #above doesn't just define schema for pets, but simultaneously creates pet class, which will make a pet object in Python

    def greet(self):
        """Greet using name."""

        return f"I'm {self.name} the {self.species or 'thing'}"

    def feed(self, units=10):
        """Nom nom nom."""

        self.hunger -= units
        self.hunger = max(self.hunger, 0)

    def __repr__(self):
        """Show info about pet."""

        p = self
        return f"<Pet {p.id} {p.name} {p.species} {p.hunger}>"

    @classmethod
    def get_by_species(cls, species):
        """Get all pets matching that species."""

        return cls.query.filter_by(species=species).all()
