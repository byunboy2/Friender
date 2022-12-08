# noinspection PyUnresolvedReferences
from app import app
from models import db, User, UserHobbies, Hobby

db.drop_all()
db.create_all()

user1 = User(
    username= "john",
    email= "test@test.com",
    password= "test",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code2.png"
)

user2 = User(
    username= "james",
    email= "test1@test.com",
    password= "test1",
    image= "https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code3.png"
)

user3 = User(
    username= "jonathon",
    email= "test2@test.com",
    password= "test2",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code4.png"
)


db.session.add_all([user1,user2,user3])
db.session.commit()

hobby1 = Hobby(
    code = "basketball"
)

hobby2 = Hobby(
    code = "soccer"
)

hobby3 = Hobby(
    code = "golf"
)

db.session.add_all([hobby1, hobby2, hobby3])
db.session.commit()


user_hobby1 =  UserHobbies(
    username = "john",
    hobby_code = "basketball"
)

user_hobby2 =  UserHobbies(
    username = "james",
    hobby_code = "soccer"
)


user_hobby3 =  UserHobbies(
    username = "jonathon",
    hobby_code = "golf"
)


db.session.add_all([user_hobby1 ,user_hobby2,user_hobby3])
db.session.commit()





