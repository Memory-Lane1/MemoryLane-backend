from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import predict
import uuid
from fastapi.responses import FileResponse
import os


app = FastAPI() # Instantiating FastApi App Object.

# Enabling CORS options.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Defining Api end-points

@app.get('/')
def get_root():
    return {"greetings": "Welcome to Memory Lane Image Resolution model"}


# @app.get('/predict')
# def get_SrImage(file_hash: str):
    
#     # model = load_model('/home/jaskaran/Desktop/Astronomical resolution/super-resolution-on-astronomical-images/Model/gen_weight_final.h5', compile=False)

#     SrImage = predict("https://ipfs.io/ipfs/"+str(file_hash))

#     return {"SrImage": SrImage}




@app.get('/predict', responses={200:{"desc":"a jpg file found"}})
def get_SrIMage( file_hash: str):
    # print("1")
    SrImage = predict("https://ipfs.io/ipfs/"+str(file_hash))

    if os.path.exists(SrImage[0]+SrImage[1]):
        # print("4"+FileName)
        return FileResponse(SrImage[0]+SrImage[1], media_type="image/jpg", filename=SrImage[1])
    else:
        # print("5"+FileName)
        return {"result":"no file found"}