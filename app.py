# for testing purpose we will use sqlite database.
#  for production we may shift to mysql database.

from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from user import UserRegister
from security import authenticate,identity
from item import  Item,ItemList

app=Flask(__name__)
app.secret_key='jose'
api=Api(app)

jwt=JWT(app,authenticate,identity) 


# api.add_resource(Item,'/item/<string:name>')
# api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
    app.run(port=5000,debug=True)