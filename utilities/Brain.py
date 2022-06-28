import numpy as np
import tensorflow as tf
import math
from tensorflow import keras
from tensorflow.keras import layers
from .MP3Handler import MP3Handler


class Brain:

    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        x = inputs = keras.Input(shape=(40,))

        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)
        # x = layers.Conv1D(filters=16, kernel_size=(3,), strides=(2,), activation="relu", data_format="channels_first")(x)
        # # x = layers.SpatialDropout1D(0.1)(x)
        # x = layers.GaussianNoise(0.01)(x)

        x = layers.Flatten()(x)

        x = layers.Dense(128, activation="relu")(x)

        x = layers.Dense(64, activation="relu")(x)

        x = layers.Dense(32, activation="relu")(x)

        num_classes = 10
        outputs = layers.Dense(num_classes, activation="softmax")(x)

        model = keras.Model(inputs=inputs, outputs=outputs)

        model.summary()

        model.compile(optimizer=keras.optimizers.Adam(0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    def train_model(self, data):
        
        def training_data():
            while True:
                chunk = q.get()
                yield (
                    chunk['inputs'],
                    chunk['outputs']
                )

        self.model.fit(np.array(data[0]), np.array(data[1]), batch_size=32, epochs=100, validation_split=0.15)