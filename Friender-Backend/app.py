import os
from dotenv import load_dotenv

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

connect_db(app)
db.create_all()

##############################################################################

##############################################################################

##############################################################################

##############################################################################

@app.get('/')
def test():

    results = [u.serialize_user() for u in User.get_all_users()]

    return jsonify(results)