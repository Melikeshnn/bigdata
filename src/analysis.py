import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from kafka import KafkaConsumer, KafkaProducer
import json

# Veri setini yükleyin
data = pd.read_csv('./data/creditcard.csv')

# İlk birkaç satıra göz atın
print(data.head())

# Veri seti hakkında özet bilgi alın
print(data.info())

# Eksik verileri kontrol edin
print(data.isnull().sum())

# Eksik veriler varsa, doldurma ya da çıkarma işlemleri
data = data.dropna()  # Eksik verileri çıkarma

# Özellikle sayısal sütunlar için (örneğin, 'Amount' sütununu normalize etme)
scaler = StandardScaler()
data['Normalized_Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))

# Gereksiz sütunu çıkarın
data = data.drop(['Amount'], axis=1)

# Kategorik değişken varsa:
data = pd.get_dummies(data, drop_first=True)

# Aykırı değerlerin tespiti için bir dağılım grafiği
sns.boxplot(data['Normalized_Amount'])
plt.show()

# Aykırı değerleri isterseniz çıkarabilirsiniz
Q1 = data['Normalized_Amount'].quantile(0.25)
Q3 = data['Normalized_Amount'].quantile(0.75)
IQR = Q3 - Q1

# IQR yöntemi ile aykırı değerleri filtreleme
data = data[~((data['Normalized_Amount'] < (Q1 - 1.5 * IQR)) | (data['Normalized_Amount'] > (Q3 + 1.5 * IQR)))]

# Histogram 
sns.histplot(data['Class'], bins=2)
plt.show()

# Korelasyon matrisi ve heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.show()

# # Kafka Consumer ve Producer Tanımları
# consumer = KafkaConsumer(
#     'data_stream',
#     bootstrap_servers=['localhost:9092'],
#     auto_offset_reset='earliest',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# def process_and_send(data):
#     # Veriyi modele gönder ve sonuçları analiz et
#     result = {"data": data, "is_anomaly": True}  # Model çıktısı burada belirlenir
#     if result["is_anomaly"]:
#         producer.send('anomalies', value=result)
#     else:
#         producer.send('normal_data', value=result)

# def consume_and_process_data():
#     for message in consumer:
#         process_and_send(message.value)

# # Eğer bu dosya çalıştırılırsa Kafka Consumer başlat
# if __name__ == "__main__":
#     # consume_and_process_data()
