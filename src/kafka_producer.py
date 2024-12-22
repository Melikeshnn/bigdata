from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Örnek veri üretimi
data = [{"id": i, "value": i * 2, "anomaly": i % 10 == 0} for i in range(1, 101)]

for record in data:
    topic = 'anomalies' if record['anomaly'] else 'normal-data'
    producer.send(topic, record)
    print(f"Sent to {topic}: {record}")
    time.sleep(1)
