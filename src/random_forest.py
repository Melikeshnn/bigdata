import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Veriyi yükleme ve işleme
def load_data():
    data = pd.read_csv(r'C:\Users\mel\Desktop\bvaproject\data\creditcard.csv')
    X = data.drop('Class', axis=1)  # Özellikler
    y = data['Class']              # Hedef değişken
    return train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest modelini eğitme
def train_random_forest():
    X_train, X_test, y_train, y_test = load_data()
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, '../models/random_forest_model.pkl')  # Modeli kaydetme

    # Tahmin yapma ve performansı ölçme
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    return accuracy, precision, recall, f1

if __name__ == "__main__":
    acc, prec, rec, f1 = train_random_forest()
    print(f"Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")
