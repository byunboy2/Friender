from models import (
    connect_db,
    db,
    User
)
from forms import LoginForm, RegisterForm
from flask import (
    Flask, request, redirect, session, g, jsonify, render_template
)
from werkzeug.exceptions import Unauthorized
import sys
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import boto3
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required)
from datetime import timedelta

s3_client = boto3.client('s3')


# from werkzeug import secure_filename


# from flask_debugtoolbar import DebugToolbarExtension

# from forms import (
#     UserAddForm, UserEditForm, LoginForm, MessageForm, CSRFProtection,
# )

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)

jwt = JWTManager(app)
blacklist = set()


connect_db(app)


# AWS IMPORTS

s3 = boto3.client(
    "s3",
    "us-west-1",
    aws_access_key_id=os.environ['aws_access_key_id'],
    aws_secret_access_key=os.environ["aws_secret_access_key"],
)

##############################################################################
# login/register/logout


@app.post('/register')
def register():
    """Register the user"""

    form = RegisterForm()

    # if form.validate_on_submit():

    # get the user data off the form
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    # get the image file
    image = request.files['image']
    image_url= f"https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/{username}"
    try:
        # try adding the user
        User.signup(username=username, email=email,
                    password=password, image=image_url)
        db.session.commit()
        # add to AWS
        s3.upload_fileobj(image, os.environ["bucket_name"], username, {"ContentDisposition": "inline",
                                                                       "ContentType": "*"})
        # create a token
        token = create_access_token(identity=username)

        # return the token
        return jsonify({"token": token})
    except IntegrityError:
        return jsonify({"error": "Username or email already exists in database!"})


@app.post("/login")
def login():
    """Login the user"""

    form = LoginForm()

    if form.validate_on_submit():

        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.authenticate(username=username, password=password)
            if user:
                token = create_access_token(identity=username)
                return jsonify({"token": token})
        except Unauthorized:
            raise Unauthorized("Invalid credentials.")


##############################################################################

@app.get("/user/<username>")
# @jwt_required
def load_homepage(username):
    """
    List all the users with common hobbies with current user.
    """
    user = User.query.get(username)
    return user.users_with_common_hobbies_descending()


# Returns users in different ranking of distance


@app.get("/user/<username>/location")
# @jwt_required
def location(username):
    """
    Takes current user and returns users in the vicinity ordered by distance
    ascending.
    """

    current_user = User.query.get(username)
    all_users = User.query.all()
    details = []

    for user in all_users:
        if (user != current_user):
            friend_details = User.query.get(user.username)
            test = friend_details.serialize_user()
            distance_between_user = user.caculate_distance_between_zip(
                current_user.location, user.location)
            test["distance"] = []
            test["distance"].append(distance_between_user)
            details.append(test)
    return jsonify(details)


##############################################################################
# chatting features

@app.route('/chat')
def chat():
    return render_template('chat.html')