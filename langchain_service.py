from kafka import KafkaConsumer, KafkaProducer
from langchain_openai import ChatOpenAI
import json, os

# --- Load your OpenAI key ---
os.environ["OPENAI_API_KEY"] = "sk-proj---->

# --- Initialize the model ---
llm = ChatOpenAI(model="gpt-4o-mini")

# --- Connect to Kafka ---
consumer = KafkaConsumer(
    "alerts",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="langchain-service"
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 LangChain service started. Waiting for alerts...")

# --- Main processing loop ---
for msg in consumer:
    alert = msg.value
    txn_str = json.dumps(alert, indent=2)

    # Generate AI explanation
    prompt = f"Explain briefly why this transaction might be suspicious:\n{txn_str}"
    explanation = llm.invoke(prompt)

    # Add explanation to message
    alert["ai_explanation"] = explanation.content
    print("💡 AI explanation added:", alert["ai_explanation"])

    # Send back into Kafka (topic ai_alerts)
    producer.send("ai_alerts", alert)
    producer.flush()
