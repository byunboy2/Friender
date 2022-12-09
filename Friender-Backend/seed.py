from app import app
from models import db, User, UserHobbies, Hobby

db.drop_all()
db.create_all()

user1 = User(
    username= "john",
    email= "test@test.com",
    password= "test",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code2.png",
    location = "33470"
)

user2 = User(
    username= "james",
    email= "test1@test.com",
    password= "test1",
    image= "https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code3.png",
    location = "55318"
)

user3 = User(
    username= "jonathon",
    email= "test2@test.com",
    password= "test2",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code4.png",
    location = "19380"
)


user4 = User(
    username= "chris",
    email= "test3@test.com",
    password= "test3",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code5.png",
    location = "16506"
)



user5 = User(
    username= "daniel",
    email= "test4@test.com",
    password= "test4",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code6.png",
    location = "11377"
)




user6 = User(
    username= "henry",
    email= "test5@test.com",
    password= "test2",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code7.png",
    location = "11354"
)



user7 = User(
    username= "jesse",
    email= "test6@test.com",
    password= "test2",
    image="https://danielchrisrithmprojectfriender.s3.us-west-1.amazonaws.com/code8.png",
    location = "50310"
)



db.session.add_all([user1,user2,user3,user4,user5,user6,user7])
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

user_hobby4 =  UserHobbies(
    username = "jonathon",
    hobby_code = "soccer"
)

user_hobby5 =  UserHobbies(
    username = "jonathon",
    hobby_code = "basketball"
)

user_hobby6 =  UserHobbies(
    username = "john",
    hobby_code = "frisbee"
)

user_hobby7 =  UserHobbies(
    username = "james",
    hobby_code = "tennis"
)

user_hobby7 =  UserHobbies(
    username = "james",
    hobby_code = "singing"
)





db.session.add_all([user_hobby1 ,user_hobby2,user_hobby3,user_hobby4,user_hobby5,user_hobby6,user_hobby7])
db.session.commit()




