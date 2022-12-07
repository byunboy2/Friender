import os
from dotenv import load_dotenv

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



connect_db(app)

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
      f.save(f.filename) 
      return 'file uploaded successfully'


##############################################################################

##############################################################################

##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]

    return jsonify(results)