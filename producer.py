from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Sending simulated transactions to Kafka...")

while True:
    txn = {
        "txn_id": random.randint(10000, 99999),
        "user_id": random.randint(1, 50),
        "amount": round(random.uniform(10, 1000), 2),
        "country": random.choice(["US", "UK", "IN", "SG"]),
        "timestamp": time.time()
    }
    producer.send("transactions", txn)
    print("Sent:", txn)
    time.sleep(1)

