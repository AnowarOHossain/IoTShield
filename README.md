# 🛡️ IoTShield  
### *Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration*

---

## 📘 Overview

**IoTShield** is a smart home automation and monitoring system designed to provide **real-time, privacy-preserving data communication** and **AI-driven anomaly detection** using the **MQTT protocol**.  
The system integrates **Generative AI (Gemini API)** to interpret and generate meaningful alerts from anomalies, ensuring an intelligent and secure home environment.

IoTShield is developed as part of the **CSE Final Year Thesis Project** at **Shanto-Mariam University of Creative Technology**, under the supervision of **Tahsin Alam (Lecturer)**.

---

## 👨‍🎓 Project Information

| Role | Name |
|------|------|
| **Project Title** | Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration |
| **System Name** | IoTShield |
| **Tagline** | *Smart Privacy-Preserving IoT Monitoring System — Powered by AI, Edge Computing, and Generative Intelligence* |
| **Team Members** | Anowar Hossain & Shihab Sarker |
| **Supervisor** | Tahsin Alam, Lecturer |
| **Institution** | Shanto-Mariam University of Creative Technology |
| **Thesis Instructor** | Rabiul Sir |
| **Base Paper** | [Internet of Things-based Home Automation with Network Mapper and MQTT Protocol (Elsevier, 2024)](https://www.sciencedirect.com/science/article/pii/S0045790624007341) |

---

## 🧩 System Architecture

IoTShield follows a **hybrid edge-cloud architecture** integrating IoT devices, an MQTT-based communication layer, a Django web server, and GenAI services for intelligent insights.

```
ESP32 Sensors → MQTT Broker (Raspberry Pi) → Django Backend → ML Anomaly Engine → Gemini API → Dashboard Alerts → MQTT Actuator
```

---

### 🔹 Components
1. **ESP32 Microcontroller (IoT Node)**
   - Collects real-time sensor data (temperature, gas, flame, motion, etc.).
   - Publishes data to MQTT broker after adding privacy-preserving noise.

2. **Raspberry Pi (Edge Node)**
   - Acts as a **local MQTT broker** (Mosquitto).
   - Performs local edge-level data filtering and buffering.

3. **Django Backend (Cloud/Server Layer)**
   - Subscribes to MQTT topics.
   - Stores data in SQL database.
   - Hosts anomaly detection and alert dashboard.

4. **Anomaly Detection Engine**
   - Implements **Isolation Forest / Autoencoder** models using scikit-learn.
   - Flags outliers and sends them to GenAI for descriptive interpretation.

5. **Generative AI Integration (Gemini API)**
   - Converts anomaly context into **human-readable alerts**.
   - Provides intelligent suggestions (e.g., “Possible gas leakage detected in kitchen — ventilation advised”).

6. **Control Loop (Actuation)**
   - Django publishes MQTT control messages.
   - ESP32 (or simulation script) acts as actuator node to execute the command.

---

## 🏗️ System Modules

| **Module** | **Description** | **Technologies** |
|-------------|------------------|------------------|
| **Data Acquisition Module** | Collects sensor readings from ESP32 and adds differential privacy noise | MicroPython, DHT11/MQ2 sensors |
| **MQTT Communication Module** | Secure publish/subscribe data exchange | Mosquitto, paho-mqtt |
| **Edge Processing Module** | Temporary caching and pre-filtering | Raspberry Pi, Python |
| **Backend & Storage Module** | Data ingestion, storage, and management | Django, SQLite/MySQL |
| **Anomaly Detection Module** | Detects unusual sensor patterns | Python, scikit-learn |
| **GenAI Alert Module** | Generates natural language alerts | Gemini API |
| **Dashboard Module** | Visualizes data and alerts | Django, Tailwind CSS, Chart.js |
| **Actuation Module** | Executes control actions | MQTT Commands, ESP32 |

---

## 🧱 System Architecture Diagram

```
+-----------------------+
|       ESP32 Node      |
| Sensors: Gas, Temp,   |
| Motion, Fire          |
+----------+------------+
           |
           |  MQTT (Publish)
           v
+-----------------------+
|   Raspberry Pi (Edge) |
| MQTT Broker (Mosquitto)|
| Local DB / Cache       |
+----------+------------+
           |
           |  MQTT (Subscribe)
           v
+-----------------------+
|   Django Backend      |
| ML: Isolation Forest  |
| Privacy Filter + GenAI|
+----------+------------+
           |
           | Gemini API (Anomaly Context)
           v
+-----------------------+
| Web Dashboard         |
| Alerts, Charts, Logs  |
| MQTT Command (Publish)|
+-----------------------+
           |
           | MQTT (Actuation)
           v
+-----------------------+
| Actuator Simulator /  |
| Real Device (ESP32)   |
+-----------------------+
```

---

## ⚙️ Installation & Setup

### 🔧 Prerequisites

Ensure the following are installed:
- **Python 3.10+**
- **Django 5.x**
- **Mosquitto MQTT Broker**
- **paho-mqtt**
- **scikit-learn**
- **numpy, pandas**
- **requests** (for Gemini API calls)
- **Tailwind CSS / Chart.js** (for dashboard)

---

### 🧩 Setup Steps

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AnowarOHossain/IoTShield.git
cd IoTShield
```

#### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux
venv\Scripts\activate     # On Windows
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Setup Django Project
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### 5️⃣ Run MQTT Broker (Raspberry Pi)
```bash
sudo systemctl start mosquitto
```

#### 6️⃣ Run IoT Sensor Simulator (if no hardware)
```bash
python simulator.py
```

#### 7️⃣ Start Django MQTT Subscriber
```bash
python manage.py mqtt_listener
```

---

## 🧠 AI Integration Details

### 🔹 Anomaly Detection (Python ML)

- Uses **Isolation Forest** trained on historical sensor data.
- Detects abnormal readings in **real-time**.
- Flags anomalies with a **confidence score**.

### 🔹 Generative AI (Gemini API)

**Input:** JSON context of anomaly (sensor type, timestamp, severity).  
**Output:** Short, actionable natural-language alert.

#### Example:

**Input:**
```json
{
  "sensor": "Gas Sensor MQ2",
  "value": "0.86",
  "threshold": "0.60",
  "location": "Kitchen"
}
```

**Gemini Output:**
```
"Possible gas leak detected in the kitchen — ventilation recommended."
```

---

## 🧩 Privacy-Preserving Mechanism

IoTShield ensures user data confidentiality using:

- **Differential Privacy Noise Addition:** Random Gaussian noise before publishing.
- **Secure MQTT (TLS/SSL) communication.**
- **Edge-First Data Handling:** Sensitive data processed on Raspberry Pi before cloud transmission.

---

## 📊 Data Flow Summary

| **Flow Stage** | **Process** | **Description** |
|----------------|-------------|-----------------|
| 1️⃣ Data Collection | ESP32 → MQTT Broker | Sensor reads environment data |
| 2️⃣ Privacy Layer | ESP32 Noise Filter | Adds noise for privacy |
| 3️⃣ Edge Processing | Raspberry Pi | Buffers, filters data locally |
| 4️⃣ Cloud Processing | Django Server | Stores, analyzes, and detects anomalies |
| 5️⃣ GenAI Processing | Gemini API | Generates descriptive alerts |
| 6️⃣ Actuation | MQTT Command | Executes automated control |

---

## 📈 Evaluation Metrics

| **Metric** | **Description** |
|------------|-----------------|
| **Latency** | End-to-end delay (sensor → dashboard) |
| **Detection Accuracy** | % of correct anomaly classifications |
| **Privacy Loss (ε)** | Effectiveness of noise-based privacy |
| **CPU/Memory Usage** | Edge and Cloud performance |
| **Alert Response Time** | Gemini API response latency |

---

## 🧾 License

This project is developed for academic and research purposes under the **Shanto-Mariam University of Creative Technology**.

---

## 📬 Contact & Credits

### Developed by:
- 👨‍💻 **Anowar Hossain** – CSE Student, Web & Software Developer
- 👨‍💻 **Shihab Sarker** – CSE Student

### Supervised by:
- 🎓 **Tahsin Alam**, Lecturer – Department of CSE & CSIT  
  **Shanto-Mariam University of Creative Technology**

### 📧 Contact
**Email:** anowarhossain.dev@gmail.com

---

## ⭐ Acknowledgment

This research and development effort is a part of the **Final Year Thesis Project** under the Department of Computer Science and Engineering (CSE).

Special thanks to **Rabiul Sir** & **Tahsin Sir** for guidance in research methodology and documentation.

---

## 🧭 Future Enhancements

- 🔗 Integrate **blockchain** for decentralized IoT trust.
- 📱 Deploy trained anomaly models **on-device (TinyML)**.
- 🎙️ Add **voice control** via Google Assistant API.
- 🏠 Expand support for more **smart devices** and automation rules.

---

<div align="center">

### 💡 **IoTShield — Combining Privacy, Intelligence, and Automation for the Next Generation of Smart Homes.**

</div>