"""SQLAlchemy models for Friender2."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

##############################################################################

class User(db.Model):
  """Users in system"""

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

  # hobbies = db.relationship(
  #   "Hobby",
  #   secondary="user_hobbies",
  #   backref="users",
  # )

  @classmethod
  def signup(cls, username, email, password, image_url=DEFAULT_IMAGE_URL):
    """Sign up user.

    Hashes password and adds user to system.
    """

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
      username=username,
      password=hashed_pwd,
      email=email,
      image_url=image_url,
      )

    db.session.add(user)
    return user

  @classmethod
  def authenticate(cls, username, password):
    """Find user with `username` and `password`.

    This is a class method. It searches for a user whose password hash matches
    this password and, if it finds such a user, returns that user object.

    If this can't find matching user (or if password is wrong), returns
    False.
    """
    user = cls.query.filter_by(username=username).first()

    if user:
      is_auth = bcrypt.check_password_hash(user.password, password)
      if is_auth:
          return user

    return False


    # if duplicate_user or duplicate_email or duplicate_image:
    #   return True

    # return False

  # def serialize_user(self):
  #   dict = self.__dict__
  #   del dict["_sa_instance_state"]
  #   return dict
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