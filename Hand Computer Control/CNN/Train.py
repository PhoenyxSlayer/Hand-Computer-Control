from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
from numpy import asarray
import cv2
import os

data = tf.keras.utils.image_dataset_from_directory("C:/Users/Phoenyx/Source/Repos/Hand Computer Control/CNN/Pictures/Training", image_size=(100,100))
print(data.class_names)
print(data)

data = data.map(lambda x,y: (((x/255)-.5)*2,tf.one_hot(y, depth=7)))
scaled_iterator = data.as_numpy_iterator()
batch = scaled_iterator.next()
print(batch[0].min())
print(batch[0].max())
print(len(data))
print("label:", batch[1])

train_size = int(len(data)*.7)
val_size = int(len(data)*.2)+2
test_size = int(len(data)*.1)
train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)

print(str(len(train)) + "\n" + str(len(val)) + "\n" + str(len(test)))

model = Sequential()

model.add(Conv2D(filters=32, kernel_size=4, activation="relu", input_shape=(100,100,3)))
model.add(Conv2D(filters=32, kernel_size=4, activation="relu"))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=64, kernel_size=4, activation="relu"))
model.add(Conv2D(filters=64, kernel_size=4, activation="relu"))
model.add(MaxPooling2D(pool_size=2))

model.add(Flatten())
model.add(Dense(512, activation="relu"))
model.add(Dense(7, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train, validation_data=val, epochs=10, batch_size=32)
model.summary()
model.save(os.path.join('CNN', 'Models', 'CNNModel.h5'))