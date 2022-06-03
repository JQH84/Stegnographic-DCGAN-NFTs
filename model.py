import tensorflow as tf
import matplotlib.pyplot as plt


model = tf.keras.models.load_model('my_model.h5')
model.compile(optimizer='Adam', loss=None)
img = model.predict(tf.random.normal([1, 5]))

plt.imshow(img[0, :, :, :])
plt.show()
