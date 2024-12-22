import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

# Veriyi yükleme ve işleme
def load_data():
    data = pd.read_csv(r"C:\Users\mel\Desktop\bvaproject\data\creditcard.csv")
    X = data.drop('Class', axis=1).values  # Özellikler
    y = data['Class'].values  # Hedef değişken
    y = to_categorical(y)  # One-hot encoding
    X = np.expand_dims(X, axis=2)  # CNN için 3D şekline getirme (örnek sayısı, özellik sayısı, 1)
    return train_test_split(X, y, test_size=0.3, random_state=42)

# CNN modelini oluşturma ve eğitme
def create_cnn_model(input_shape):
    model = Sequential()
    model.add(Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(32, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(2, activation='softmax'))  # İki sınıf (0, 1) olduğu için
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# CNN modelini eğitme
def train_cnn():
    X_train, X_test, y_train, y_test = load_data()
    model = create_cnn_model(X_train.shape[1:])
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    model.save('../models/cnn_model.h5')  # Modeli kaydetme

    # Performansı ölçme
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)
    
    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    precision = precision_score(y_test_classes, y_pred_classes)
    recall = recall_score(y_test_classes, y_pred_classes)
    f1 = f1_score(y_test_classes, y_pred_classes)
    
    return accuracy, precision, recall, f1

if __name__ == "__main__":
    acc, prec, rec, f1 = train_cnn()
    print(f"Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")
