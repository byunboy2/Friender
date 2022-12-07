import os
from dotenv import load_dotenv
import boto3
s3_client = boto3.client('s3')

from flask import (
    Flask, request, redirect, session, g, jsonify
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

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['S3_BUCKET'] = os.environ["AWS_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]



connect_db(app)
db.create_all()

################################################################# AWS IMPORTS


BUCKET_NAME=os.environ["AWS_BUCKET_NAME"]
S3_BASE_URL = f'https://{BUCKET_NAME}.s3.amazonaws.com/'


s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=["aws_access_key_id"],
  aws_secret_access_key=["aws_secret_access_key"],
)




##############################################################################

##############################################################################

##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]

    return jsonify(results)