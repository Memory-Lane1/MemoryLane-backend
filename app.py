from flask import Flask , request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.User import RegisterUser, UserLogin, RefreshLogin, UpdatePassword, ForgotPassword, Profile , UserLogout
from models.User import User
# from resources.UploadImage import UploadImage
import urllib.request
import time
#from utils import blocklist
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
from models.Image import Image
from models.model import predict


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "somesecretcode"

ACCESS_EXPIRES= timedelta(hours=5)
# MODEL_PATH='/home/jaskaran/Documents/MemoryLaneLocal/Deep_Learning_Model/gen_weight_final.h5'

# change path
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
    parser = reqparse.RequestParser()
    parser.add_argument('_id',
                        type = str,
                        required = True
                        )
    print('qwer')

    @jwt_required()
    def post(self):
        # print('abcd')
        data = self.parser.parse_args()
        user, user_id = User.find_by_id(data['_id'])
        # print(user_id)
        f = request.files['file']
        # print('1234')
    # f.save(f.filename)
        # st=str(_id)

        #change path
        path='/home/jaskaran/Documents/MemoryLaneLocal/img'
        
        print('')
        # print('5678')
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        f.save(os.path.join(path, f.filename))
        # print('91011')
        image_path = path + '/'+ str(f.filename)
        # print('121314')
        print(image_path)
        # if _ == None:
        # return {"message":"Successful upload"},200
        img = Image(user_id,image_path)
        # print('151617')
        if img.insert():
            # print('181920')
            image_id=Image.find_by_path(image_path)
            # print('212223')
            print(user_id)
            print(' ')
            print(image_id)
            print(' ')
            return {"message": "Successful upload",
                "user_id":user_id,
                "image_id":image_id}, 200
        else:
                return {"message": "an error occurred"}, 500
        
  

class Predict(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('image_id',
                        type = str,
                        required = True
                        )
    parser.add_argument('user_id',
                        type = str,
                        required = True
                        )

    def post(self):
        data = self.parser.parse_args()
        image_id = data['image_id']
        user_id = data['user_id']   

        image = Image.find_by_id(image_id)

        if image is None:
            return {'message':'bad request'}, 400
        else:
            predicted_path = predict(image.path_to_img)
            predicted_img = Image(user_id, image.path_to_img)
            predicted_img.insert()
            return {
                'message':'successful',
                'path':predicted_path
            }, 200



        



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
    
    # with tf.device('/CPU:0'):
      # model=keras.models.load_weights(MODEL_PATH)
    app.run(debug = False)