import os
import Keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator

def create_model():
  model = Sequential()
  model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(256, 256, 3)))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(1, activation='softmax'))

  return model

train_generator = ImageDataGenerator(
  data_format="channels_last",
  rescale = 1. / 255
)

train_batches = train_generator.flow_from_directory(
    batch_size=32,
    directory='./dataset/train',
    target_size=(256, 256),
    class_mode='binary'
)

validation_generator = ImageDataGenerator(
  data_format="channels_last",
  rescale = 1. / 255
)

validation_batches = validation_generator.flow_from_directory(
    batch_size=32,
    directory='./dataset/validation',
    target_size=(256, 256),
    class_mode='binary'
)

model = create_model()

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Starts training the model
model.fit_generator(train_batches,
                    epochs=15,
                    verbose=1,
                    steps_per_epoch=len(train_batches),
                    validation_data=validation_batches,
                    initial_epoch=0,
                    validation_steps=len(validation_batches)
                    )

test_generator = ImageDataGenerator(
    data_format='channels_last',
    rescale=1./255
)

test_batches = test_generator.flow_from_directory(
    batch_size=1,
    directory='./dataset/test',
    target_size=[256, 256],
    class_mode='binary'
)

score = model.evaluate_generator(test_batches, verbose=1)

print(model.metrics_names)
print('test dataset: ' + str(score))
