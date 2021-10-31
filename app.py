from flask import Flask 
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.User import RegisterUser, UserLogin, RefreshLogin, UpdatePassword, ForgotPassword, Profile , UserLogout
from resources.UploadImage import UploadImage
import urllib.request
import time
from utils import blocklist
from datetime import timedelta
import sys
import os
import glob
import re
import numpy as np

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "somesecretcode"

ACCESS_EXPIRES= timedelta(hours=5)
MODEL_PATH='Deep_Learning_Model/gen_weight_final.h5'

app.config["JWT_ACCESS_TOKEN_EXPIRES"]=ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)

CORS(app)
api = Api(app)

# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header,jwt_payload):
#     jti = jwt_payload["jti"]
#     token_in_redis = blocklist.jwt_redis_blocklist.get(jti)
#     return token_in_redis is not None


api.add_resource(RegisterUser, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Profile,'/myprofile')
api.add_resource(RefreshLogin, '/reauth')
api.add_resource(UpdatePassword, '/password/change')
api.add_resource(ForgotPassword,'/password/get_new')
api.add_resource(UserLogout,'/logout')
api.add_resource(UploadImage,'/uploadimage/<string:fname>')

if __name__ == '__main__':
    
    model=load_model(MODEL_PATH)
    app.run(debug = False)