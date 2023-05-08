<<<<<<< HEAD:codigos/ejemploi3.py
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
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              metrics=['acc'])

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
validation_dataset = tf.data.Dataset.from_generator(
        lambda: validation_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

validation_dataset1 = validation_dataset.repeat()
callb=[tf.keras.callbacks.ModelCheckpoint(filepath= 'modelo', verbose=1, save_freq="epoch", mode='auto', save_best_only=True)]

history = model.fit(
      train_generator,
      steps_per_epoch=len(train_generator), # número de lotes en un ciclo de entrenamiento
      epochs=100,
      validation_data=validation_dataset1,
      validation_steps=len(validation_generator),
      verbose=2,
      callbacks=callb
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
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              metrics=['acc'])

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
validation_dataset = tf.data.Dataset.from_generator(
        lambda: validation_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 150, 150, 3], [None]))

validation_dataset1 = validation_dataset.repeat()
callb=[tf.keras.callbacks.ModelCheckpoint(filepath= 'modelo', verbose=1, save_freq="epoch", mode='auto', save_best_only=True)]

history = model.fit(
      train_generator,
      steps_per_epoch=len(train_generator), # número de lotes en un ciclo de entrenamiento
      epochs=100,
      validation_data=validation_dataset1,
      validation_steps=len(validation_generator),
      verbose=2,
      callbacks=callb
>>>>>>> origin:ejemploi3.py
      )