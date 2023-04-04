import tensorflow as tf

modelo = tf.keras.models.load_model("modelo")

"""Traer imagen"""
img = "imagen"
img= img/255.
img=tf.reshape(img, shape=(150,150,3))
img = tf.expand_dims(img, axis=0)
modelo.predict(img)
"""Para redondear tf.round()"""
