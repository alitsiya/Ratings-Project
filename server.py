"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user's profile"""

    user = Rating.query.get(user_id)

    user_movie_list = Rating.query.filter_by(user_id = user_id).all()
    movies = []
    for user_movie in user_movie_list:
        movies.append((user_movie.movie.movie_title, user_movie.score))

    return render_template("user_profile.html", email=user.user.email,
                                                age=user.user.age,
                                                zipcode=user.user.zipcode,
                                                occupation=user.user.occupation,
                                                movies=movies,
                                                )


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by('movie_title').all()

    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>", methods=['GET'])
def show_movies(movie_id):
    """Show movies's details"""

    movie = Movie.query.get(movie_id)
    return render_template("movie_profile.html", movie=movie, score=None,
                                                )

@app.route("/movies/<int:movie_id>", methods=['POST'])
def update_movie_rating(movie_id):
    """Update movie rating """

    user_rating = request.form.get("rating")

    if user_rating:
        print '\n' + user_rating + '\n'
        email = session['email'] 
        user = User.query.filter_by(email=email).all()
        print user[0].user_id #user_id

        rating = Rating.query.filter_by(movie_id = movie_id, user_id = user[0].user_id).all()
        print rating[0].score
        #if user rated movie, then update rating, else create new value into Ratings table in db
        if rating:
            rating[0].score = user_rating
            print rating[0].score
        else:
            rating = Rating(score=user_rating,
                            movie_id=movie_id,
                            user_id=user[0].user_id,
                            )
            db.session.add(rating)
        print rating
        # rating.score = user_rating
        # ratings.update().\
        #     where(ratings.movie_id == movie_id, user_id == user.user_id).\
        #     values(score=user_rating)

        print "\nRating updated \n"

    db.session.commit()

    movie = Movie.query.get(movie_id)

    return render_template("movie_profile.html", movie=movie, score=rating[0].score)

@app.route('/sign-in', methods=['GET'])
def render_sign_in():
    """Render Sign In Page"""

    return render_template("sign_in.html")

@app.route('/sign-in', methods=['POST'])
def sign_in():
    """Dealing with Submit on Sign In Page"""

    email = request.form.get('email')
    password = request.form.get('password')
    print email
    print password
    # if user exist - log in and redirect to homepage
    existing_user = User.query.filter_by(email = email).all()

    print existing_user

    if not existing_user:
    # if user doesn't exist - add user to db  and redirect
        flash("You're not registered. Do you want to sign up?")
        return redirect('/sign-up')
    else:    
        if existing_user.password != password:
            print "\n Incorrect password\n\n"
            flash("Incorrect password")
            
            return redirect("/sign-in")
        
        else:
            print "\n Logged in - SUCCSESS!!!"
            session['email'] = email
            flash("Logged in as %s" % email)

    return redirect("/")

@app.route('/sign-up')
def sign_up_form():
    """Sign Up page"""

    return render_template("sign_up.html")

@app.route('/sign-up', methods=['POST'])
def sign_up():
    """Handles Sign Up page input"""
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    occupation = request.form.get('occupation')
    zipcode = request.form.get('zipcode')

    user = User(email=email,
                password=password,
                age=age,
                occupation=occupation,
                zipcode=zipcode,
                    )

    print "\nAdded to Database \n"

    db.session.add(user)
    db.session.commit()
    session['email'] = email
    flash("%s has been added" % email) 
    return redirect('/')

@app.route('/logout')
def sign_out():
    """Log out users"""

    if session: 
        del session['email']
        flash("The user has logged out")
    
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
