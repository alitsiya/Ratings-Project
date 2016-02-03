"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    occupation = db.Column(db.String(50), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Show user's info"""
        return "<user's id=%s email=%s age=%s zipcode=%s>" % (self.user_id, self.email, 
                                                            self.age, self.zipcode)


# Put your Movie and Rating model classes here.
class Movie(db.Model):
    """User of ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(150), nullable=True)
    # unknown = db.Column(db.Boolean, nullable=True)
    # action = db.Column(db.Boolean, nullable=True)
    # adventure = db.Column(db.Boolean, nullable=True)
    # animation = db.Column(db.Boolean, nullable=True)
    # childrens = db.Column(db.Boolean, nullable=True)
    # comedy = db.Column(db.Boolean, nullable=True)
    # crime = db.Column(db.Boolean, nullable=True)
    # documentary = db.Column(db.Boolean, nullable=True)
    # drama = db.Column(db.Boolean, nullable=True)
    # fantacy = db.Column(db.Boolean, nullable=True)
    # film_noir = db.Column(db.Boolean, nullable=True)
    # horror = db.Column(db.Boolean, nullable=True)
    # musical = db.Column(db.Boolean, nullable=True)
    # mistery = db.Column(db.Boolean, nullable=True)
    # romance = db.Column(db.Boolean, nullable=True)
    # sci_fi = db.Column(db.Boolean, nullable=True)
    # thriller = db.Column(db.Boolean, nullable=True)
    # war = db.Column(db.Boolean, nullable=True)
    # western = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        """Show movie's info"""
        return "<movie id=%s movie title=%s release_date=%s >" % (self.movie_id, self.movie_title, 
                                                            self.release_date)

class Rating(db.Model):
    """Shows ratings of the movies."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=True)
    score = db.Column(db.Integer, nullable=True)


    user = db.relationship('User', backref=db.backref("ratings", order_by=rating_id))
    movie = db.relationship('Movie', backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Show user's info"""
        return "<user's id=%s movie_id=%s score=%s>" % (self.user_id, self.movie_id, 
                                                            self.score)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
