import pathway as pw

class Txn(pw.Schema):
    txn_id: int = pw.column_definition(primary_key=True)
    amount: float
    country: str
    timestamp: float
    user_id: int

rdkafka = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "pathway-consumer",
    "auto.offset.reset": "earliest",
}

transactions = pw.io.kafka.read(
    rdkafka,
    topic="transactions",
    format="json",
    schema=Txn,
    autocommit_duration_ms=1000,
)

alerts = transactions.filter(pw.this.amount > 500)

pw.io.kafka.write(
    alerts,
    {"bootstrap.servers": "localhost:9092"},
    "alerts",
    format="json",
)

pw.run()