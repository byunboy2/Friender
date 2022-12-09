"""SQLAlchemy models for Friender2."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import requests
from flask import (jsonify)

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

    location = db.Column(
        db.Text,
        nullable=True,
    )

    # location = db.relationship("Location")

    hobbies = db.relationship(
        "Hobby",
        secondary="user_hobbies",
        backref="users",
    )
    
    matches = db.relationship(
        'User',
        secondary='matches',
        primaryjoin=(Match.username_matcher == username),
        secondaryjoin=(Match.username_matchee == username),
        backref='matcher'
    )

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

    def users_with_common_hobbies_descending(self):
        """
        Return a frequency counter of users that have a common hobby with
        current user in descending order.
        """
        counter = {}

        for hobby in self.hobbies:
            users = hobby.users
            for user in users:
                if user != self:
                    counter[user.username] = counter.get(user.username, 0)+1

        sorted_users_by_frequency = sorted(
            counter.items(), key=lambda x: x[1], reverse=True)
        converted_users = dict(sorted_users_by_frequency)

        potential_friends = list(converted_users.keys())
        print("potential_friends",potential_friends)
        details = []
        for friend in converted_users:
            friend_details = User.query.get(friend)
            test = friend_details.serialize_user()
            print("these are the test",test)
            test["hobbies"] = []
            for h in friend_details.hobbies:
                print("these are the hobby",h)
                test["hobbies"].append(h.code)
            details.append(test)

        return jsonify(details)

    @staticmethod
    def caculate_distance_between_zip(zip1, zip2):
        """
        Find the distance between two zip codes
        """
        zipcodekey = "34rLAdNVPatsZZeuUF595mtEVPz9sAB3UOSIhHHjjpvoB4kD9urQHZDyL0QKXJkp"
        url = f'https://www.zipcodeapi.com/rest/{zipcodekey}/distance.json/{zip1}/{zip2}/mile'
        response = requests.get(url)
        return response.text

    def serialize_user(self):
        """Serializes only column data."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

##############################################################################


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

    """
    
        - one to many
        - one user to many matches
        - join table UserMatches

    """ 

class Match(db.Model):
    """Connection of a user <-- Match --> users"""

    __tablename__ = 'matches'

    username_matcher = db.Column(
        db.Text,
        db.ForeignKey('user.username')
    )

    username_matchee = db.Column(
        db.Text,
        db.ForeignKey('user.username')
    )

##############################################################################

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
