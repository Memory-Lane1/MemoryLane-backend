from flask import Flask , request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.User import RegisterUser, UserLogin, RefreshLogin, UpdatePassword, ForgotPassword, Profile , UserLogout
# from resources.UploadImage import UploadImage
import urllib.request
import time
from utils import blocklist
from datetime import timedelta
import sys
import os
import glob
import re
from werkzeug.utils import secure_filename
import werkzeug
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "somesecretcode"

ACCESS_EXPIRES= timedelta(hours=5)
MODEL_PATH='/home/jaskaran/Documents/MemoryLaneLocal/Deep_Learning_Model/gen_weight_final.h5'
UPLOAD_FOLDER = '/home/jaskaran/Documents/MemoryLaneLocal/img'


app.config["JWT_ACCESS_TOKEN_EXPIRES"]=ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)

CORS(app)
api = Api(app)

# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header,jwt_payload):
#     jti = jwt_payload["jti"]
#     token_in_redis = blocklist.jwt_redis_blocklist.get(jti)
#     return token_in_redis is not None




# class UploadImage(Resource):
#    def post(self):
#     f = request.files['file']
#     f.save(f.filename)
#     return {"message":"Successful upload"},200


class UploadImage(Resource):
   def post(self):
    f = request.files['file']
    # f.save(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return {"message":"Successful upload"},200

  

class Predict(Resource):
    def post(self):

        img_name=[i for i in os.listdir('/home/jaskaran/Documents/MemoryLaneLocal/img')]
        target_path=['/home/jaskaran/Documents/MemoryLaneLocal/img/'+i for i in img_name]
        img=Image.open(target_path)
        img=np.asarray(img)
        



api.add_resource(RegisterUser, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Profile,'/myprofile')
api.add_resource(RefreshLogin, '/reauth')
api.add_resource(UpdatePassword, '/password/change')
api.add_resource(ForgotPassword,'/password/get_new')
api.add_resource(UserLogout,'/logout')
api.add_resource(UploadImage,'/uploader')
api.add_resource(Predict,'/predict')


if __name__ == '__main__':
    
    model=keras.models.load_model(MODEL_PATH)
    app.run(debug = False)