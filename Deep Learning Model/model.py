import sys
import os
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image

def generator_block(i,filters):
    input_layer=keras.Input(shape=i.shape[1:])
    o=keras.layers.Conv2D(filters,(3,3),padding='same',kernel_regularizer=keras.regularizers.l2)(input_layer)
    o=keras.layers.BatchNormalization()(o)
    o=keras.layers.LeakyReLU()(o)
    o=keras.layers.Conv2D(filters,(3,3),padding='same',kernel_regularizer=keras.regularizers.l2)(o)
    o=keras.layers.BatchNormalization()(o)
    o=keras.layers.add([input_layer,o])
    model_block=keras.Model(inputs=input_layer,outputs=o)
    return model_block

def generator_model():
  inputs=keras.Input(shape=(180,256,3))
  x=keras.layers.Conv2D(32,(5,5),padding='same')(inputs)
  x=keras.layers.LeakyReLU()(x)
  skip=x
  x=generator_block(x,32)(x)
  x=generator_block(x,32)(x)
  x=keras.layers.Conv2D(64,(5,5),padding='same')(x)
  x=keras.layers.LeakyReLU()(x)
  x=generator_block(x,64)(x)
  x=generator_block(x,64)(x)
  x=keras.layers.Conv2D(64,(5,5),padding='same')(x)
  x=keras.layers.LeakyReLU()(x)
  x=generator_block(x,64)(x)
  x=generator_block(x,64)(x)
  x=keras.layers.Conv2D(64,(5,5),padding='same')(x)
  x=keras.layers.LeakyReLU()(x)
  x=generator_block(x,64)(x)
  x=generator_block(x,64)(x)
  x=keras.layers.Conv2D(32,(3,3),padding='same')(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.add([x,skip])
  x=keras.layers.Conv2DTranspose(32,(2,2),strides=4)(x)
  x=keras.layers.Conv2D(32,(3,3),padding='same')(x)
  x=keras.layers.LeakyReLU()(x)
  x=generator_block(x,32)(x)
  x=keras.layers.Conv2D(3,(3,3),padding='same',activation=keras.activations.sigmoid)(x)
  generator=keras.Model(inputs=inputs,outputs=x)
  return generator

gen=generator_model()

gen.load_weights('gen_weight_final.h5')

def main():
    if len(sys.argv)==1:
        print("ERROR: Input image missing.")
        sys.exit(0)
    elif len(sys.argv)==2:
        path_to_img=sys.argv[1]
        if os.path.isfile(path_to_img):
            if len(path_to_img)>4 and (path_to_img[-4:]=='.jpg' or path_to_img =='.png' ):    
                img=Image.open(path_to_img)
                img = np.asarray( img, dtype="int32" )[0:180+0,0:256+0,:]
                gen_img=gen.predict(img.reshape(1,180,256,3)/255.)
                plt.imshow(gen_img[0])
            else:
                print('ERROR: Invalid input.')
        else:
            print("ERROR: Invalid path to image.")
            sys.exit(0)
    else:
        print('Only 1 arguments required. Given',len(sys.argv)-1)
        sys.exit(0)

if __name__ == '__main__':
    main()