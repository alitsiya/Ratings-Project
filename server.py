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

    print user_id
    user = Rating.query.get(user_id)
    print user
    return "Test"
    # return render_template("user_profile.html", age=user.age,
    #                                             zipcode=user.zipcode,
    #                                             occupation=user.occupation,
    #                                             movies="",
    #                                             )

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
    existing_user = User.query.filter_by(email = email).first()

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
