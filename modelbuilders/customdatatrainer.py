import keras
import random
import numpy as np
import pandas as pd
import os

currentdir = "C:\\Users\\peczo\\OneDrive\\Desktop\\Projects\\Desktop-Apps\\Git\\AwfulIDE\Data\\"
def ModelStats(accuracy, loss, epochs, batchNum, randomnum_classes, modelnum):
    with open('modelstats.txt', 'a') as f:
        f.write(f'{modelnum}:\n')
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Loss: {loss}\n')
        f.write(f'Epochs: {epochs}\n')
        f.write(f'Batch Size: {batchNum}\n')
        f.write(f'Number of Classes: {randomnum_classes}\n')
        f.write('\n')

def train(modelnum):
    batchNum = 2000
    randomnum_classes = 2000
    epoochRandnum = 200
    batch_size = batchNum
    num_classes = randomnum_classes
    epochs = epoochRandnum

    # Load your Kaggle dataset
    train_df = pd.read_csv(f"{currentdir}\\alpha_gym\\train.csv")
    test_df = pd.read_csv(f"{currentdir}\\alpha_gym\\test.csv")
    x_train = train_df.drop('label', axis=1).values.reshape(-1, 28, 28, 1)
    y_train = keras.utils.to_categorical(train_df['label'].values, num_classes)

    
    if 'label' in test_df.columns:
        x_test = test_df.drop('label', axis=1).values.reshape(-1, 28, 28, 1)
        y_test = keras.utils.to_categorical(test_df['label'].values, num_classes)
    else:
        x_test = test_df.values.reshape(-1, 28, 28, 1)
        y_test = None

    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0] if x_test is not None else 0, 'test samples')

    model = keras.Sequential()
    model.add(keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(256, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    hist = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test) if y_test is not None else None)
    print("The model has successfully trained")

    model.save(f'models/handwritten_text_recognition_model_{modelnum}.h5')
    print(f"Saving the model as handwritten_text_recognition_model{modelnum}.h5")

    if y_test is not None:
        score = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        ModelStats(score[1], score[0], epochs, batchNum, randomnum_classes, f'model {modelnum}')
    else:
        print("No test labels provided.")

def trainModel(modelnum):
    for i in range(modelnum):
        print("Training model " + str(i))
        train(i)
        

if __name__ == "__main__":
    trainModel(3)

