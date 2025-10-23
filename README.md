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
Created a file named **docker-compose.yml** to start apache/kafka on docker:

Run: 
  ```bash docker compose up -d```

Check: 
  ```docker ps```

Create topics:

  ```docker exec -it kafka kafka-topics --create --topic transactions --bootstrap-server localhost:9092```
  
  ```docker exec -it kafka kafka-topics --create --topic alerts --bootstrap-server localhost:9092```
  
  ```docker exec -it kafka kafka-topics --create --topic ai_alerts --bootstrap-server localhost:9092```



2️⃣ WSL2 (Ubuntu) — Python Environment

Create a virtual environment:

  ```python3 -m venv pathway-env```
  ```source pathway-env/bin/activate```

Install dependencies:

  ```pip install -r requirements.txt```

Set your OpenAI key:

  export OPENAI_API_KEY="sk-xxxx"

3️⃣ Run Components

🧾 Producer(in Windows)

  ```python producer.py```

⚡ Pathway Consumer(in WSL2)

  ```python3 pathway_consumer1.py```

 ⚠ Alerts(in Windows)
 
  ```docker exec -it kafka kafka-console-consumer --topic alerts --bootstrap-server localhost:9092 --from-beginning```

🧠 LangChain AI Service(in WSL2)

  ```python3 langchain_service.py```


4️⃣ Verify in Kafka

Check topics:

  ```docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092```

  Three topics: transactions , alerts and ai_alerts

Consume messages:

  ```docker exec -it kafka kafka-console-consumer --topic ai_alerts --bootstrap-server localhost:9092 --from-beginning```


The anonymous transcations are outputted like this with explaination: 

AI explanation: This transaction might be considered suspicious for several reasons:
1. **Unusual Amount**: The amount of 819.06 could be significantly higher than typical transaction amounts for the user or within the region, raising flags.
2. **Timestamp and Transaction Diff**: The proximity of the timestamp and time suggests that this transaction occurred very rapidly, which could indicate automated or fraudulent behavior.
3. **Country**: Depending on the user's usual transaction behavior, a transaction from or to a certain country may be flagged as suspicious. If this user typically makes transactions in a different country, it could raise concerns about identity theft or unauthorized transactions.
4. **User Profile**: If user_id 46 is a new or relatively inactive account that suddenly engages in high-value transactions, this might also indicate suspicious activity.

Considering these factors, the transaction could warrant further investigation to determine its legitimacy.
