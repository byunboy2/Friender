import os
from dotenv import load_dotenv
import boto3
s3_client = boto3.client('s3')


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


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['S3_BUCKET'] = os.getenv("bucket_name")
app.config['S3_KEY_ID'] = os.getenv("aws_access_key_id")
app.config['S3_SECRET_KEY'] = os.getenv("aws_secret_access_key")


connect_db(app)


################################################################# AWS IMPORTS

# S3_BASE_URL = f'https://{S3_BUCKET}.s3.amazonaws.com/'

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=os.environ['aws_access_key_id'],
  aws_secret_access_key=os.environ["aws_secret_access_key"],
)

# upload_file(file_name, bucket, object_name)






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
@app.post('/newuser', methods=["GET", "POST"])
def create_newuser():
    """Create a new user, test..."""
    
    if request.method == 'GET':
        return render_template('newuser.html')

    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    file = request.files['file']

    s3.upload_fileobj(file, os.environ["bucket_name"], file.filename,{"ContentDisposition":"inline",
        "ContentType":"*"})
    image = f"https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/{file.filename}"

    user = User(username=username, email=email, password=password, image=image)
    db.session.add(user)
    db.session.commit()

    return f"{username} was successfully created."


##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]

    return jsonify(results)