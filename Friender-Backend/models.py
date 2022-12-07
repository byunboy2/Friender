# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# bcrypt = Bcrypt()
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

  password = db.Column(
    db.Text,
    nullable=False,
  )

  image = db.Column(
    db.Text,
    nullable=True,
  )

  # location = db.Column(
  #   db.Integer,
  #   db.ForeignKey('locations.zip')
  # )

  # location = db.relationship("Location")

  hobbies = db.relationship(
    "Hobby",
    secondary="user_hobbies",
    backref="users",
  )

  @classmethod
  def get_all_users(cls):
    return User.query.all()


  def serialize_user(self):
    dict = self.__dict__
    del dict["_sa_instance_state"]
    return dict
##############################################################################

  """_summary_

    user -< userhobbies >- hobby
  """

class UserHobbies(db.Model):
  """Join table between users and hobbies"""

  __tablename__ = 'user_hobbies'

  username = db.Column(
    db.Text,
    db.ForeignKey('users.username'),
    nullable=False,
    primary_key=True,
  )

  hobby_code = db.Column(
    db.Text,
    db.ForeignKey('hobbies.code'),
    nullable=False,
    primary_key=True,
  )


class Hobby(db.Model):
  """Hobby
    backref: users -> User
  """

  __tablename__ = 'hobbies'

  code = db.Column(
    db.Text,
    nullable=True,
    primary_key=True,
  )


##############################################################################

#   """_summary_

#     user -> location >- users
#   """

# class Location(db.Model):
#   """Location"""

#   __tablename__ = 'locations'

#   zip = db.Column(
#     db.Integer,
#     nullable=True,
#     primary_key=True,
#   )


##############################################################################

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)