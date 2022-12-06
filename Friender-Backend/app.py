import os
from dotenv import load_dotenv

from flask import (
    Flask, render_template, request, flash, redirect, session, g, abort
)
# from flask_debugtoolbar import DebugToolbarExtension

# from forms import (
#     UserAddForm, UserEditForm, LoginForm, MessageForm, CSRFProtection,
# )
from models import (
    db, connect_db, User)

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

##############################################################################

##############################################################################

##############################################################################

##############################################################################

@app.get('/')
def test():
  return "hello"