# AI-Driven Real-Time Transaction Anomaly Detection  
### Powered by Apache Kafka, Pathway, LangChain, and OpenAI GPT-4o-mini

---

## Overview
This project demonstrates a **real-time AI streaming pipeline** where:
- 🧾 A **Python producer** streams synthetic transactions into **Kafka**
- ⚡ **Pathway** consumes and filters suspicious transactions live
- 🧠 **LangChain + GPT-4o-mini** analyze each suspicious case to generate AI explanations
- 📡 Results are sent back to Kafka for further visualization or action

Designed to run seamlessly across:
- **Windows Docker (Kafka)**
- **Ubuntu 24.04 via WSL2 (Pathway + LangChain)**

---

## Architecture
[Producer] → (transactions)
↓
[Kafka Broker] ← Docker (Windows)
↓
[Pathway Consumer] → filters & outputs → topic: alerts
↓
[LangChain Service] → adds GPT explanations → topic: ai_alerts


---

## Components

|    Component      |     Technology            |                Description                       |
|-------------------|---------------------------|--------------------------------------------------|
| **Producer**      | Python                    | Streams random transactions to Kafka             |
| **Consumer**      | Pathway                   | Detects suspicious events in real time           |
| **AI Service**    | LangChain + GPT-4o-mini   | Adds natural-language insights                   |
| **Broker**        | Apache Kafka              | Handles live data streaming                      |


---

## Setup Instructions

1️⃣ Kafka on Windows (Docker)
Create a file named docker-compose.yml:

Run: 
  ```bash docker compose up -d```

Check: 
  ```docker ps```


2️⃣ WSL2 (Ubuntu) — Python Environment

Create a virtual environment:

  ```python3 -m venv pathway-env```
  ```source pathway-env/bin/activate```

Install dependencies:

  ```pip install -r requirements.txt```

Set your OpenAI key:

  export OPENAI_API_KEY="sk-xxxx"

3️⃣ Run Components

🧾 Producer

  ```python3 producer.py```

⚡ Pathway Consumer

  ```python3 pathway_consumer1.py```

🧠 LangChain AI Service

  ```python3 langchain_service.py```


4️⃣ Verify in Kafka

Check topics:

  ```docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092```

Consume messages:

  ```docker exec -it kafka kafka-console-consumer --topic ai_alerts --bootstrap-server localhost:9092 --from-beginning```


You’ll see AI-enriched transaction logs such as:

  {
    "txn_id": 91823,
    "amount": 987.3,
    "country": "IN",
    "ai_explanation": "Transaction amount unusually high; may indicate suspicious behavior."
  }
