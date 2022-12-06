from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
  """User"""

  __tablename__ = 'users'

  username = db.Column(
      db.Text,
      primary_key=True,
      nullable=False,
  )

  email = db.Column(
      db.Text,
      nullable=False,
      unique=True,
  )

  location = db.Column(
      db.Text,
      nullable=False,
  )

  password = db.Column(
      db.Text,
      nullable=False,
  )

# class Hobby(db.Model):
#   """Hobby"""

#   __tablename__ = 'hobbies'

# class Interest(db.Model):
#   """Interest"""

#   __tablename__ = 'interests'

# class Location(db.Model):
#   """Interest"""

#   __tablename__ = 'locations'

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)