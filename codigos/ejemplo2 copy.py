<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:e3cc5feac3b47042f39df88675afc9e9c2b057005ce23095888334e09425fe2d
size 5450
=======
<<<<<<< HEAD:codigos/ejemplo2 copy.py
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.metrics as metrics
import scipy


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)), #Hacer un reshape a las imagenes a probar
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              metrics=['acc',]) #metrics.Mean('val_loss')])

train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        r'C:\Users\Admin\Documents\Images\Dataset\Entrenamiento',
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
        r'C:\Users\Admin\Documents\Images\Dataset\Validacion',
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

train_dataset = tf.data.Dataset.from_generator(
        lambda: train_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

train_dataset1 = train_dataset.repeat()
validation_dataset = tf.data.Dataset.from_generator(
        lambda: validation_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

validation_dataset1 = validation_dataset.repeat()
callb=[tf.keras.callbacks.ModelCheckpoint(filepath= 'modelo', verbose=1, save_freq="epoch", mode='auto',monitor='val_loss', save_best_only=True)]

history = model.fit(
      train_dataset1,
      steps_per_epoch=100,
      epochs=100,
      validation_data=validation_dataset1,
      validation_steps=50,
      verbose=2,
      callbacks=callb
      )



# model_json = model.to_json()
# with open("model.json", "w") as json_f:
#     json_f.write(model_json)

# model.save_weights("model.h5")
# print("Modelo guardado!")
=======
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.metrics as metrics
import scipy


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)), #Hacer un reshape a las imagenes a probar
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              metrics=['acc',]) #metrics.Mean('val_loss')])

train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        r'C:\Users\Admin\Documents\Images\Dataset\Entrenamiento',
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
        r'C:\Users\Admin\Documents\Images\Dataset\Validacion',
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

train_dataset = tf.data.Dataset.from_generator(
        lambda: train_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

train_dataset1 = train_dataset.repeat()
validation_dataset = tf.data.Dataset.from_generator(
        lambda: validation_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

validation_dataset1 = validation_dataset.repeat()
callb=[tf.keras.callbacks.ModelCheckpoint(filepath= 'modelo', verbose=1, save_freq="epoch", mode='auto',monitor='val_loss', save_best_only=True)]

history = model.fit(
      train_dataset1,
      steps_per_epoch=100,
      epochs=100,
      validation_data=validation_dataset1,
      validation_steps=50,
      verbose=2,
      callbacks=callb
      )



# model_json = model.to_json()
# with open("model.json", "w") as json_f:
#     json_f.write(model_json)

# model.save_weights("model.h5")
# print("Modelo guardado!")
>>>>>>> origin:ejemplo2 copy.py
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
