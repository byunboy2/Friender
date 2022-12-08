import os
from dotenv import load_dotenv
import boto3
from flask_jwt_extended import (JWTManager, create_access_token,
create_refresh_token
,get_raw_jwt)
from datetime import timedelta

s3_client = boto3.client('s3')

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc
import sys

# from werkzeug import secure_filename

from flask import (
    Flask, request, redirect, session, g, jsonify, render_template
)

# from flask_debugtoolbar import DebugToolbarExtension

# from forms import (
#     UserAddForm, UserEditForm, LoginForm, MessageForm, CSRFProtection,
# )
from models import (
    connect_db,
    db,
    User
)

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


################################################################# AWS IMPORTS

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=os.environ['aws_access_key_id'],
  aws_secret_access_key=os.environ["aws_secret_access_key"],
)

##############################################################################
# TEST ROUTE FOR UPLOADING
@app.get('/upload')
def upload_file_form():
   return render_template('upload.html')

@app.post('/uploader')
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        #   saves file to root directory
        # overwrites if have same name
        # f.save(f.filename)
        # try:

        print("this is what f is",f.filename)
        s3.upload_fileobj(f, os.environ["bucket_name"], f.filename,{"ContentDisposition":"inline",
        "ContentType":"*"})
        # os.remove(f.filename)
        image = f"https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/{f.filename}"
        print(image)
        return 'file uploaded successfully'
        # except ClientError as e:
        #     logging.error(e)
        # return False

# test route for creating a user
@app.route('/newuser', methods=["GET", "POST"])
def create_newuser():
    """Create a new user.

    Create new user and add detail to DB and image to Amazon. Redirect to hompage.
    If username or picture exists is DB or AWS, return error.

    """

    if request.method == 'GET':
        return render_template('newuser.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    file = request.files['file']
    file.filename=username

    image = f"https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/{file.filename}"
    try:
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password), image=image)
        db.session.add(user)
        db.session.commit() # this is where the error is happening
        print("this shouldn't be printed")
        s3.upload_fileobj(file, os.environ["bucket_name"], file.filename,{"ContentDisposition":"inline",
        "ContentType":"*"})
        return f"{username} was successfully created."
    except exc.IntegrityError:
        print("This should be printed")
        sys.exit(1)

##############################################################################

##############################################################################
# login/register/logout


@app.post('/register')
def register():
    """Register the user"""

    # get the user data off the form
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    # get the image file
    image = request.files['image']

    try:
        # try adding the user
        User.signup(username=username, email=email, password=password, image=image)
        db.session.commit()
        # add to AWS
        s3.upload_fileobj(image, os.environ["bucket_name"], username,{"ContentDisposition":"inline",
        "ContentType":"*"})
        # create a token
        token = create_access_token(identity=username)

        # return the token
        return jsonify({"token": token})
    except IntegrityError:
        # TODO:
        raise IntegrityError("Username or email already exists in database!")


@app.post("/login")
def login():
    """Login the user"""

    try:
        # get the user info
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.authenticate(username=username, password=password)
        # check that user exists
        # user = User.query.filter_by(username=username).first()
        # compare the password against the hashed password
        # is_auth = bcrypt.check_password_hash(user.password, password)
        # return the token
        if not user:
            token = create_access_token(identity=username)
            return jsonify({"token": token})

        # TODO:
        return "Username and/or password is not a match"
    except Exception:
        # TODO:
        raise Exception("Invalid credentials.")


##############################################################################
# all other routes / protected routes
# all other routes need @jwt_required


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]
    User.filter
    return jsonify(results)