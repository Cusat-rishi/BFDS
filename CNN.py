import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, BatchNormalization, Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization, AveragePooling2D, \
    GlobalAveragePooling2D, Activation
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from matplotlib import pyplot as plt

data_dir = 'Data'

Bone = []
for file in os.listdir(data_dir):
    Bone += [file]
print(Bone)
print(len(Bone))
num_classes=len(Bone)

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), padding='Same', activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(filters=96, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(filters=96, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(num_classes, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.3)

train_data = datagen.flow_from_directory(data_dir, target_size=(224, 224), batch_size=15, class_mode='categorical',
                                         subset='training')

val_data = datagen.flow_from_directory(data_dir, target_size=(224, 224), batch_size=15, class_mode='categorical',
                                       subset='validation')

print("\n Testing the data.....\n")

history = model.fit_generator(train_data,  epochs=50, validation_data=val_data, verbose=1)

model.save(r"model/cnn.h5")

plt.style.use("ggplot")
plt.figure()
plt.plot(history.history['accuracy'], 'r', label='training accuracy', color='green')
plt.plot(history.history['val_accuracy'], label='validation accuracy')
plt.xlabel('# epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig(r"model/cnn_acc.png")
plt.show()

plt.style.use("ggplot")
plt.figure()
plt.plot(history.history['loss'], 'r', label='training accuracy', color='green')
plt.plot(history.history['val_loss'], label='validation accuracy')
plt.xlabel('# epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig(r"model/cnn_loss.png")
plt.show()

