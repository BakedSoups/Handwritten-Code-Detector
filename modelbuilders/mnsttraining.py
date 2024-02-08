import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

import random

def ModelStats(accuracy, loss, epochs, batchNum, randomnum_classes, modelnum):
    with open('modelstats.txt', 'a') as f:
        f.write(f'{modelnum}:\n')
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Loss: {loss}\n')
        f.write(f'Epochs: {epochs}\n')
        f.write(f'Batch Size: {batchNum}\n')
        f.write(f'Number of Classes: {randomnum_classes}\n')
        f.write('\n')
print("ModelStats function defined")


def train(modelnum):
    batchNum = random.randint(128, 400)
    randomnum_classes = random.randint(10, 100)
    epoochRandnum = random.randint(40, 120)

    batch_size = batchNum
    num_classes = randomnum_classes
    epochs = epoochRandnum

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    print(x_train.shape, y_train.shape)

    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    input_shape = (28, 28, 1)

    # convert class vectors to binary class matrices

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])

    hist = model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(x_test, y_test))
    print("The model has successfully trained")

    model.save(f'models/mnist{modelnum}.h5')
    print("Saving the model as mnist.h5")

    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    ModelStats(score[1], score[0],epochs,batchNum, randomnum_classes,  f'model {modelnum}')



def trainModel(modelnum):
    for i in range(modelnum):
        print("Training model " + str(i))
        train(i)

if __name__ == "__main__":
    trainModel(60)

