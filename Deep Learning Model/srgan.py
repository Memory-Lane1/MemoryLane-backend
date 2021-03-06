# -*- coding: utf-8 -*-
"""SRGAN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hgeIxtJ0HbI7h4miibYwofcQ5usaJ6L3

**Import Libraries**
"""

import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
print(tf.__version__)

"""**Creating Architecture**"""

def discriminator_model():
  input_layer=keras.Input(shape=(720,1024,3))
  x=keras.layers.Conv2D(32,(11,11),strides=2)(input_layer)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(64,(7,7),strides=2,kernel_regularizer=keras.regularizers.l2)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(64,(5,5),kernel_regularizer=keras.regularizers.l2,strides=2)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(128,(3,3),kernel_regularizer=keras.regularizers.l2,strides=2)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(128,(3,3),kernel_regularizer=keras.regularizers.l2,strides=2)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(128,(3,3),kernel_regularizer=keras.regularizers.l2,strides=2)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Conv2D(128,(3,3),kernel_regularizer=keras.regularizers.l2,strides=1)(x)
  x=keras.layers.BatchNormalization()(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Flatten()(x)
  x=keras.layers.Dense(1024,kernel_regularizer=keras.regularizers.l2,)(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Dense(256,kernel_regularizer=keras.regularizers.l2,)(x)
  x=keras.layers.LeakyReLU()(x)
  x=keras.layers.Dense(1,activation='sigmoid',kernel_regularizer=keras.regularizers.l2)(x)
  model=keras.Model(inputs=input_layer,outputs=x)
  return model

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

"""**Images example**"""

img=Image.open('/content/drive/MyDrive/MemoryLane/Dataset_Human_Blur1/1 (1).jpg')
img = np.asarray( img, dtype="int32" )
img.reshape(1,720,1024,3)

plt.figure(figsize=(20, 20))
plt.title('Blurred')
plt.axis('off')
plt.imshow(img[::4,::4,:])

img=Image.open('/content/drive/MyDrive/MemoryLane/Dataset_Human_Sharp1/1 (1).jpg')
img = np.asarray( img, dtype="int32" )
img.reshape(1,720,1024,3)
plt.figure(figsize=(20, 20))
plt.title('High Resolution')
plt.axis('off')
plt.imshow(img)

"""**Importing Images** """

img_names=[i for i in os.listdir('/content/drive/MyDrive/MemoryLane/Dataset_Human_Sharp1')]
target_paths=['/content/drive/MyDrive/MemoryLane/Dataset_Human_Sharp1/'+i for i in img_names]
input_paths=['/content/drive/MyDrive/MemoryLane/Dataset_Human_Blur1/'+i for i in img_names]

def getNumpyImages(paths,number):
  image = tf.keras.preprocessing.image.load_img(paths[0])
  input_arr = keras.preprocessing.image.img_to_array(image)
  input_arr=input_arr.reshape(1,720,1024,3)
  count=0
  for i in range(1,number):
    count+=1
    if(count%10==0):
      print('\b\b\b'+str(count),end='')
    image = tf.keras.preprocessing.image.load_img(paths[i])
    input_arr2 = keras.preprocessing.image.img_to_array(image)
    input_arr2=input_arr2.reshape(1,720,1024,3)
    input_arr=np.concatenate([input_arr,input_arr2],axis=0)
  return input_arr

target_images_np=getNumpyImages(target_paths,300)

input_images_np=target_images_np[:,::4,::4,:]

# target=np.load('/content/drive/MyDrive/SRGAN/target.npy')

"""Perceptual Loss for Generator using VGG19 (https://arxiv.org/pdf/1609.04802.pdf)"""

from tensorflow.keras.applications.vgg19 import VGG19
vgg=VGG19(input_shape=(720,1024,3),include_top=False,weights='imagenet')
vgg_model_1=tf.keras.Model(inputs=vgg.inputs,outputs=vgg.get_layer(name='block3_conv4').output)

img=Image.open('/content/drive/MyDrive/MemoryLane/Dataset_Human_Blur1/1 (1).jpg')
img = np.asarray( img, dtype="int32" )
img=img.reshape(1,720,1024,3)
out=vgg_model_1(img)[0]
plt.title('Intermediate Result 1')
plt.imshow(out[:,:,0:3]/255.)

vgg_model_2=tf.keras.Model(inputs=vgg.inputs,outputs=vgg.get_layer(name='block4_conv4').output)

for layer in vgg_model_1.layers:
  layer.trainable=False

for layer in vgg_model_2.layers:
  layer.trainable=False

vgg_model_2.summary()

img=Image.open('/content/drive/MyDrive/MemoryLane/Dataset_Human_Blur1/1 (1).jpg')
img = np.asarray( img, dtype="int32" )
img=img.reshape(1,720,1024,3)
out=vgg_model_2(img)[0]
plt.title('Intermediate Result 2')
plt.imshow(out[:,:,0:3]/255.)

"""**Creating Model**"""

class SRGAN(keras.Model):
  def __init__(self,discriminator,generator):
    super(SRGAN, self).__init__()
    self.discriminator=discriminator
    self.generator=generator
  def compile(self, loss_fn,discriminator_op,generator_op):
    super(SRGAN, self).compile()
    self.loss_fn=loss_fn
    self.discriminator_op=discriminator_op
    self.generator_op=generator_op
  def train_step(self,data):
    input_images=data[0]
    target_images=data[1]
    batch_size=1
    print(input_images.shape)
    for k in range(1):
      ind=np.random.randint(low=0,high=16,size=batch_size)
      batch_real=tf.gather(target_images,ind)
      batch_fake=self.generator(tf.gather(input_images,ind))
      y_batch_real=np.ones((batch_size,1),dtype=np.float32)
      y_batch_fake=np.zeros((batch_size,1),dtype=np.float32)
      xtrain=tf.concat([batch_real,batch_fake],axis=0)
      ytrain=tf.concat([y_batch_real,y_batch_fake],axis=0)
      with tf.GradientTape() as tape:
        predictions=self.discriminator(xtrain)
        d_loss=self.loss_fn(ytrain,predictions)
      
      grads=tape.gradient(d_loss,self.discriminator.trainable_weights)
      self.discriminator_op.apply_gradients(
          zip(grads,self.discriminator.trainable_weights)
      )
    for k in range(5):
      misleading_labels=np.ones((batch_size,1),dtype=np.float32)
      ind=np.random.randint(low=0,high=16,size=batch_size)
      batch_fake=tf.gather(input_images,ind)
      target_sample=tf.gather(target_images,ind)
      with tf.GradientTape() as tape:
        generated_image=self.generator(batch_fake)
        vgg_1_real=vgg_model_1(target_sample)
        vgg_1_fake=vgg_model_1(generated_image)
        vgg_2_real=vgg_model_2(target_sample)
        vgg_2_fake=vgg_model_2(generated_image)
        predictions=self.discriminator(generated_image)
        g_loss=0.001*self.loss_fn(misleading_labels,predictions) 
        g_loss+=0.1*tf.keras.losses.MeanSquaredError()(vgg_2_real,vgg_2_fake)
        g_loss+=tf.keras.losses.MeanSquaredError()(vgg_1_real,vgg_1_fake)
        g_loss+=tf.keras.losses.MeanSquaredError()(self.generator(batch_fake),target_sample)
      grads=tape.gradient(g_loss,self.generator.trainable_weights)
      self.generator_op.apply_gradients(
          zip(grads,self.generator.trainable_weights)
      )

    return {'d_loss':d_loss,'g_loss':g_loss}


  def get_config(self):
    config = super(Linear, self).get_config()
    config.update({"units": self.units})
    return config

dis=discriminator_model()
gen=generator_model()

gan=SRGAN(dis,gen)
gan.compile(
    discriminator_op=keras.optimizers.Adam(learning_rate=0.0003),
    generator_op=keras.optimizers.Adam(learning_rate=0.0003),
    loss_fn=keras.losses.BinaryCrossentropy()
)

"""**Fine Tuning of trained model**"""

# dis.load_weights('/content/drive/MyDrive/SRGAN/dis_weight_final.h5')
# gen.load_weights('/content/drive/MyDrive/SRGAN/gen_weight_final.h5')
# for layer in list(gen.layers)[:-4]:
#   layer.trainable=False

# for layer in list(dis.layers)[:-4]:
#   layer.trainable=False

"""**Start Training**"""

gan.fit(input_images_np/255.,target_images_np/255.,epochs=7,batch_size=10)

"""**Testing**"""

u=77
print(target_images_np[u].max())
print(target_images_np[u].min())
plt.figure(figsize=(14,14))
plt.imshow(target_images_np[u]/255)

out=gen.predict(target_images_np[u:u+1,:180,:256]/255)
plt.figure(figsize=(14,14))
plt.imshow((out[0]))

dis.predict(target_images_np[u:u+1])

out=target_images_np[u:u+1,:180,0:256+0]/255
plt.figure(figsize=(14,14))
plt.imshow((out[0]))

"""**Random Picture**"""

path_to_img='/content/drive/MyDrive/MemoryLane/Dataset_Human_Sharp1/1 (1).jpg'
img=Image.open(path_to_img)
img = np.asarray( img, dtype="int32" )[:180:1,:256:1,:]
plt.figure(figsize=(14, 14))
plt.title('Test Image')
plt.axis('off')
plt.imshow(img)

out=gen(img.reshape(1,180,256,3)/255.)
plt.figure(figsize=(14, 14))
plt.title('Output')
plt.axis('off')
plt.imshow(out[0])

plt.figure(figsize=(20, 20))

plt.title('Output')
plt.axis('off')
plt.imshow(out[0])

img=Image.open('/content/drive/MyDrive/MemoryLane/Dataset_Human_Blur1/1 (1).jpg')
img = np.asarray( img, dtype="int32" )[::4,::4,:]
plt.figure(figsize=(14, 14))
plt.title('Test Image')
plt.axis('off')
plt.imshow(img)

out=gen(img.reshape(1,180,256,3)/255.)
plt.figure(figsize=(14, 14))
plt.title('Output')
plt.axis('off')
plt.imshow(out[0])

"""**Saving Model**"""

gen.save_weights('/content/drive/MyDrive/SRGAN/gen_weight_final.h5')

dis.save_weights('/content/drive/MyDrive/SRGAN/dis_weight_final.h5')

