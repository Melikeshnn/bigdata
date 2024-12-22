from random_forest import train_random_forest
from cnn_model import train_cnn
from kafka import KafkaProducer
import json
import time

def main():
    print("Random Forest Model Results:")
    acc, prec, rec, f1 = train_random_forest()
    print(f"Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")

    print("\nCNN Model Results:")
    acc, prec, rec, f1 = train_cnn()
    print(f"Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")
    ############################################################
    # Kafka Producer tanımlanıyor
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka'ya veri gönderme fonksiyonu
def send_data_to_kafka(data):
    producer.send('normal_data', value=data)  # Topic adı 'normal_data' olarak değiştirildi
    producer.flush()
############################################################
if __name__ == "__main__":
    sample_data = {"feature1": 1.5, "feature2": 2.3, "label": 0}
    while True:
        send_data_to_kafka(sample_data)
        time.sleep(1)
main()
