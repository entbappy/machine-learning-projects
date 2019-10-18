# -*- coding: utf-8 -*-
"""bank_customer_satisfaction_prediction_using_CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yfJHE8g9yr1zfdKauZQjSVKC2yt72Fpb
"""

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, MaxPool1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold

!git clone https://github.com/laxmimerit/Data-Files-for-Feature-Selection.git

"""### Dataset: https://www.kaggle.com/c/bnp-paribas-cardif-claims-management/data"""

data = pd.read_csv('/content/Data-Files-for-Feature-Selection/santander-train.csv')
data.head()

data.shape

X = data.drop(labels=['ID', 'TARGET'], axis=1)
X.shape

y = data['TARGET']

# train_features, test_features, train_labels, test_labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y)

X_train.shape # training data shape

X_test.shape  # test data shape

# Remove constant, Quasi constant
filter = VarianceThreshold(0.01)
X_train = filter.fit_transform(X_train)
X_test = filter.transform(X_test)

# after removing features, now we have
X_train.shape, X_test.shape

# remove duplicate features
X_train_T = X_train.T
X_test_T = X_test.T

# Converting it to panda dataFrame, cause pandas has a feature called duplicated()
X_train_T = pd.DataFrame(X_train_T)
X_test_T = pd.DataFrame(X_test_T)

X_train_T.shape, X_test_T.shape

X_train_T.duplicated().sum()

duplicated_features = X_train_T.duplicated()
print(duplicated_features)

# invert values
features_to_keep = [not index for index in duplicated_features]
features_to_keep

X_train = X_train_T[features_to_keep].T
X_train.shape

X_test = X_test_T[features_to_keep].T
X_test.shape

scaler = StandardScaler() # transforms every data into same scale
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train.shape, X_test.shape

# reshape data for NN - CNN
X_train = X_train.reshape(60816, 256, 1)
X_test = X_test.reshape(15204, 256, 1)

X_train.shape, X_test.shape

# converting labels to numpy arrays
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

# CNN model

model = Sequential()
model.add(Conv1D(32, 3, activation='relu', input_shape = (256,1)))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.3))

model.add(Conv1D(64, 3, activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.5))

model.add(Conv1D(128, 3, activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer=Adam(lr=0.00005), loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), verbose=1)

history.history

# graph ploting 

def plot_learningCurve(history, epoch):
  # Plot training & validation accuracy values
  epoch_range = range(1, epoch+1)
  plt.plot(epoch_range, history.history['accuracy'])
  plt.plot(epoch_range, history.history['val_accuracy'])
  plt.title('Model accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Val'], loc='upper left')
  plt.show()

  # Plot training & validation loss values
  plt.plot(epoch_range, history.history['loss'])
  plt.plot(epoch_range, history.history['val_loss'])
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Val'], loc='upper left')
  plt.show()

plot_learningCurve(history, 10)