from flask_restful import Resource,reqparse

from models.User import User


# Resource is basically where CRUD operation takes place...
class RegisterUser(Resource):
    # reqparse is basically request parsing.
    # basically things that client ( for testing postman) will pass will be considered in this order.
    parser=reqparse.RequestParser()
    parser.add_argument('email', type=str,required=True)
    parser.add_argument('password',type=str,required=True)
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('age',type=int,required=True)
    parser.add_argument('country',type=str,required=True)
    parser.add_argument('PhoneNo',type=str,required=True)

    # class method functions argument has self in it.
    # 200--> successful
    # 400 --> bad request.
    # 500 --> server fault
    def post(self):
        data=self.parser.parse_args()
        email=data['email']
        password=data['password']
        name=data['name']
        age=data['age']
        country=data['country']
        phoneNo=data['PhoneNo']

        _user, _id=User.find_by_email(email)
        if _user==None:
            user=User(email,password,name,age,country,phoneNo)
            if user.insert():
                return {"message":"registered successfully"},200
            else:
                return {"message":"an error occured"},500
        else:
            return {"message":"Email ID is already registered"},400
    


class UserLogin(Resource):