from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

##############################################################################

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

  picture = db.Column(
    db.Text,
    nullable=True
  )

  hobbies = db.relationship(
        "Hobby"
    )

  users_with_same_hobbies = db.relationship(
        "User",
        secondary="user_hobbies",
        backref="following",
    )

##############################################################################

  """_summary_

    user -< userhobbies >- hobby
  """

class UserHobbies(db.Model):
  """Join table between users and hohbbies"""

  __tablename__ = 'user_hobbies'

  user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
      primary_key=True,
  )

  hobby_code = db.Column(
      db.Integer,
      db.ForeignKey('hobbies.code'),
      nullable=False,
      primary_key=True,
  )


class Hobby(db.Model):
  """Hobby"""

  __tablename__ = 'hobbies'

  code = db.Column(
    db.Text,
    nullable=True,
    primary_key=True,
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

##############################################################################

"""_summary_

    user -< userInterests >- interests
  """

class UserInterests(db.Model):
  """Join table between users and hohbbies"""

  __tablename__ = 'user_interests'

  user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
      primary_key=True,
  )

  interest_code = db.Column(
      db.Integer,
      db.ForeignKey('interests.code'),
      nullable=False,
      primary_key=True,
  )

class Interest(db.Model):
  """Interest"""

  __tablename__ = 'interests'

  code = db.Column(
    db.Text,
    nullable=True
    primary_key=True,
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

##############################################################################

"""_summary_

    user -< userLocation >- location
  """

class UserLocation(db.Model):
  """Join table between users and hohbbies"""

  __tablename__ = 'user_locations'

  user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
      primary_key=True,
  )

  location_code = db.Column(
      db.Integer,
      db.ForeignKey('locations.code'),
      nullable=False,
      primary_key=True,
  )

class Location(db.Model):
  """Interest"""

  __tablename__ = 'locations'

  code = db.Column(
    db.Text,
    nullable=True
    primary_key=True,
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

##############################################################################

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)