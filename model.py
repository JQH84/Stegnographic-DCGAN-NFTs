import tensorflow as tf
from PIL import Image
import numpy as np



def makePunk():
    model = tf.keras.models.load_model('my_model.h5')
    model.compile(optimizer='Adam', loss=None)
    image = model.predict(tf.random.normal([1, 5]))
    image = image.reshape(48, 48,3)
    image = tf.keras.preprocessing.image.array_to_img(image)
    return image
