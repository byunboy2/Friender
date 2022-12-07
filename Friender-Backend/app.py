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
        response = s3.upload_fileobj(f, os.environ["bucket_name"], f)
        os.remove(f.filename)
        return 'file uploaded successfully'
        # except ClientError as e:
        #     logging.error(e)
        # return False

@app.get('/get')
def read_file():
    s3.

# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]

    return jsonify(results)