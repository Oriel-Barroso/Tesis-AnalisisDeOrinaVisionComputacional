import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
tf.data.experimental.enable_debug_mode()

# Definir las rutas de las imágenes
train_dir = r'/home/oriel/python/testIA/Images/Dataset/Entrenamiento'
validation_dir = r'/home/oriel/python/testIA/Images/Dataset/Validacion'

# Definir el generador de imágenes para el entrenamiento y validación
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')

# Crear el modelo de la CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compilar el modelo
model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-4),
              metrics=['accuracy'])

steps_per_epoch = len(train_dir)//32

validation_steps = len(validation_generator)//32

# Entrenar el modelo
history = model.fit(
      train_generator,
      steps_per_epoch=steps_per_epoch,
      epochs=50,
      validation_data=validation_generator,
      validation_steps=validation_steps,
      verbose=2)

# Evaluar el modelo con las imágenes de comparación
test_dir = r'C:\Users\Admin\Documents\Images\Dataset\Test'
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
    )
test_loss, test_acc = model.evaluate(test_generator, steps=50)
print('test acc:', test_acc)