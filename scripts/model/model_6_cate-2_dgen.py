import os
import re
import datetime
import numpy as np
from PIL import Image
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt

def prepae_data():
    x, t = [], []

    categorized_dir_paths = glob('/content/drive/My Drive/kikagaku/novelapp/data/images/categorized-2/*')

    for dir_path in categorized_dir_paths:
        category_id = os.path.basename(dir_path)
        image_paths = glob(os.path.join(dir_path, '*'))
        print(datetime.datetime.now().isoformat(), 'Category', category_id, ':', len(image_paths))

        for i, p in enumerate(image_paths):
            book_id = re.sub(r'(_.*$)', '', os.path.basename(p))

            if i % 30 == 0:
                print(datetime.datetime.now().isoformat(), 'Image:', i, book_id, category_id)

            try:
                img = Image.open(p)
                img_resize = img.resize((229, 229))
                img_np = np.array(img_resize) / 255.0
                img_reshape = img_np.reshape(1, 229, 229, 3)
                #print(datetime.datetime.now().isoformat(), img_np.shape, img_reshape.shape)

                x.append(img_np)
                t.append(category_id)

            except Exception as e:
                print(datetime.datetime.now().isoformat(), 'Error:', e)

    return x, t


x, t = prepae_data()

x = np.array(x).astype('f')
t = np.array(t).astype('f')


import tensorflow as tf
from tensorflow import keras

import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split


x_train, x_val, t_train, t_val = train_test_split(x, t, test_size=0.3, random_state=0)


import os
import random


def reset_seed(seed=0):
    os.environ['PYTHONHASHSEED'] = '0'
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


reset_seed(0)

category_count = len(np.unique(t))


from tensorflow.keras import models, layers
from tensorflow.keras.applications import Xception

from tensorflow.keras.preprocessing.image import ImageDataGenerator


datagen = ImageDataGenerator(
    rotation_range=180,     # randomly rotate images in the range
    zoom_range=0.1,         # randomly zoom image
    width_shift_range=0.1,  # randomly shift images horizontally
    height_shift_range=0.1, # randomly shift images vertically
    horizontal_flip=True,   # randomly flip images horizontally
    vertical_flip=True      # randomly flip images vertically
)

datagen.fit(x_train)

model_fine = Xception(include_top=False, weights='imagenet', input_shape=x_train.shape[1:])

for layer in model_fine.layers[:100]:
    layer.trainable = False


model = models.Sequential()
model.add(model_fine)

model.add(layers.Flatten())

model.add(layers.BatchNormalization())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(category_count, activation='softmax'))

optimizer = keras.optimizers.Adagrad(lr=0.005)

model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

model.summary()

#history = model.fit(x_train, t_train,
#                    batch_size=30,
#                    epochs=400,
#                    verbose=0,
#                    validation_data=(x_val, t_val))
history = model.fit_generator(
    datagen.flow(x_train, t_train, batch_size=32),
    epochs=400,
    verbose=0,
    validation_data=(x_val, t_val),
    #steps_per_epoch=x_train.shape[0]
)

