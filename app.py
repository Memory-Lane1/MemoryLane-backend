from flask import Flask 
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from utils.security import authenticate, identity
from resources.User import RegisterUser, UserLogin

app=Flask(__name__)
app.secret_key='memorylane'
api=Api(app)

api.add_resource(RegisterUser,'/register')

jwt=JWT(app,authenticate,identity) # creates new end point... /auth



if __name__=='__main__':
    app.run(port=5000,debug=True)