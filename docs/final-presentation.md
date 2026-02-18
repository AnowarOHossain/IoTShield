# Final Presentation: IoTShield

## Slide-1(Title Slide)

* **University:** Shanto-Mariam University of Creative Technology (estd 2003)
* **Project Title:** Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration
* **Presented by:**
* Anowar Hossain (ID: 221071051)
* Shihab Sarker (ID: 202071004)


* **Department:** CSE
* **Supervised By:** Tahsin Alam, Lecturer, Department Of CSE & CSIT, SMUCT

## Slide-2(Background)

* Smart homes rely on IoT devices for automation.
* Privacy and security risks are increasing.
* Cloud dependence causes latency & data exposure.
* There is a need for real-time, intelligent, privacy-focused systems.
* **Key Concepts:** Data Privacy Shield, Real-Time Automation, Local AI Processing Unit, Secure Local Storage, Low Latency, Reduced Cloud Reliance.

## Slide-3(Literature Review - Related Work)

| No | Focus Area | Method / Technology | Key Contribution |
| --- | --- | --- | --- |
| 1 | MQTT Smart Home | MQTT + Raspberry Pi | Low-latency smart home communication |
| 2 | GenAI in IoT | Generative AI | AI-based anomaly detection |
| 3 | GAN-based Security | GAN/VAE | Detects subtle IoT anomalies |
| 4 | Privacy-Preserving IoT | Edge + Privacy Filtering | Protects sensitive sensor data |
| 5 | Smart City IoT Security | AI + IoT | Large-scale anomaly detection |
| 6 | Edge AI Smart Home | Edge AI + IoT | Low-latency secure processing |
| 7 | MQTT Security Dataset | MQTT_UAD | Benchmark dataset for attacks |
| 8 | GenAI IoT Security Survey | GenAI + IoT | Future security directions |

## Slide-4(Key Findings & Research Gap)

* **Key Findings:**
* MQTT is widely used for fast and lightweight smart home communication.
* Most anomaly detection systems rely on cloud-based ML, causing latency and privacy risks.
* Existing privacy solutions mainly focus on encryption, but real-time edge filtering is limited.
* Generative AI is emerging for event interpretation but is rarely used in real-time IoT monitoring.
* Most systems do not combine MQTT, Edge Privacy, and GenAI together.


* **Identified Research Gap:**
* There is still no unified real-time smart home system that jointly integrates MQTT communication + Edge-based privacy preservation + GenAI-driven anomaly interpretation into a single end-to-end framework.

## Slide-5(Problem Statement)

* Existing IoT systems expose sensitive sensor data.
* Many rely on cloud-only processing, which leads to slow responses.
* There is a lack of contextual anomaly explanations.
* There is a need for a low-latency, privacy-preserving, AI-supported solution.
* **Goal:** A desired solution featuring Privacy-Preserving (Local AI), Quick Response & Explanation, and AI-Supported Contextual analysis.

## Slide-6(Objectives)

The primary objectives are:

* Ensure privacy-preserving sensor data processing.
* Detect abnormal readings using Generative AI.
* Provide human-readable safety alerts.
* Create a centralized dashboard for visualization.
* Implement real hardware integration (ESP32) for practical demonstration.
* Add user authentication and secure access.
* Enable automated email alerts for critical events using Gmail SMTP.

## Slide-7(System Architecture Overview)

An end-to-end privacy-preserving IoT architecture integrating ESP32 hardware, MQTT messaging, Django backend with AI-powered anomaly detection, and real-time web dashboard for intelligent home automation monitoring.

```
╔══════════════════════════════════════════════════════════════════════╗
║                    IoTShield System Architecture                      ║
║          Privacy-Preserving IoT Monitoring with Local AI              ║
╚══════════════════════════════════════════════════════════════════════╝

┌─────────────┐   WiFi   ┌─────────────┐  TCP/IP  ┌─────────────┐
│   ESP32     │ ══════► │    MQTT     │ ══════► │   Django    │
│  Sensors    │  2.4GHz  │   Broker    │          │  Backend    │
│  (5 Types)  │          │ (Mosquitto) │          │ Processing  │
└─────────────┘          └─────────────┘          └──────┬──────┘
                                                          │
                                                          ▼
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│ Dashboard + │ ◄══════  │   Local AI  │ ◄══════  │   Privacy   │
│   Email     │          │  (Ollama    │          │  Filtering  │
│   Alerts    │          │ llama3.2:1b)│          │             │
└─────────────┘          └─────────────┘          └─────────────┘
                                ▲
                                │
                         ┌──────┴──────┐
                         │  Anomaly    │
                         │  Detection  │
                         │   Engine    │
                         └─────────────┘
```

**Key Components:**
* **Hardware Layer:** ESP32 Microcontroller with multiple sensors
* **Communication:** MQTT Protocol (Message Queue Telemetry Transport)
* **Backend:** Django Framework with SQLite database
* **Privacy:** Differential Privacy Mechanism (Gaussian Noise)
* **AI Engine:** Local Ollama LLM (llama3.2:1b)
* **Output:** Real-time Dashboard + Automated Email Alerts

## Slide-8(ESP32 Hardware Implementation)

Our hardware prototype integrates ESP32 microcontroller with multiple IoT sensors including DHT11 (temperature/humidity), MQ-2 (gas detection), PIR motion sensor, flame sensor, and LDR (light sensor) on a breadboard. The ESP32 collects real-time sensor data every 5 seconds and transmits it securely to the backend via WiFi and MQTT protocol for AI-powered anomaly detection.

## Slide-9(Privacy Mechanism - Dual Layer)

IoTShield implements a comprehensive dual-layer privacy protection system combining differential privacy with cryptographic security to ensure maximum data confidentiality.

```
╔══════════════════════════════════════════════════════════════════════╗
║              Dual-Layer Privacy Architecture                          ║
╚══════════════════════════════════════════════════════════════════════╝

┌──────────────┐      ┌────────────────────────┐      ┌──────────────────┐
│Raw Sensor    │      │  LAYER 1:              │      │  LAYER 2:        │
│Data (25.0°C) │─────►│  Differential Privacy  │─────►│  RSA Encryption  │
│              │      │  (Gaussian Noise)      │      │  RSA-2048+OAEP   │
└──────────────┘      │  ε = 0.5               │      │  SHA-256         │
                      └────────┬───────────────┘      └────────┬─────────┘
                               │                               │
                               ▼                               ▼
                    ┌──────────────────────┐    ┌──────────────────────────┐
                    │ Noisy Data Output    │    │  Encrypted Ciphertext    │
                    │ (25.523°C)           │    │  Ready for Storage       │
                    └──────────────────────┘    └────────┬─────────────────┘
                                                          │
                                                          ▼
                                          ┌───────────────────────────────┐
                                          │ Encrypted Database Storage    │
                                          │ (SQLite + RSA-2048 Protected) │
                                          └───────────────────────────────┘
```

**Key Features:**
* **Layer 1 - Differential Privacy:** Adds calibrated Gaussian noise (ε = 0.5) to raw sensor readings, protecting individual privacy
* **Layer 2 - RSA-2048 Encryption:** Takes noisy data and encrypts it using public-key cryptography with OAEP padding and SHA-256 hashing
* **End-to-End Protection:** Ensures data privacy from collection to storage
* **Secure Storage:** All sensitive data stored in encrypted format in SQLite database
* **Key Management:** RSA key pairs managed securely with private key protection

## Slide-10(AI Anomaly Detection Workflow)

IoTShield uses local Ollama LLM (llama3.2:1b) to analyze sensor data in real-time and detect anomalies. The system classifies events by severity and triggers instant alerts via email, dashboard, and logs, providing users with clear and actionable notifications.

```
╔══════════════════════════════════════════════════════════════════════╗
║              AI-Powered Anomaly Detection System                      ║
╚══════════════════════════════════════════════════════════════════════╝

Normal Data Flow:
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Sensor  │────►│ Database │────►│ Dashboard│
│ Reading │     │  Store   │     │ Display  │
└─────────┘     └──────────┘     └──────────┘
   25.5°C          ✓ Normal           

Anomaly Detection Flow:
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Sensor  │────►│Ollama LLM│────►│  Alert   │
│ Reading │     │ Analysis │     │ System   │
└─────────┘     └────┬─────┘     └──────────┘
   85.3°C            │                 
                     ▼
              ┌──────────────┐
              │  Severity:   │
              │  CRITICAL    │
              │              │
              │  Action:     │
              │  • Email     │
              │  • Dashboard │
              │  • Log       │
              └──────────────┘
```

**Key Workflow Steps:**
* **Data Collection:** Encrypted sensor data retrieved from database
* **LLM Analysis:** Ollama llama3.2:1b processes data to detect anomalies
* **Severity Classification:** Events classified as CRITICAL, HIGH, MEDIUM, or LOW
* **Alert Generation:** Critical events trigger immediate notifications
* **Multi-Channel Delivery:** Alerts sent via email, web dashboard, and system logs
* **Real-Time Response:** Instant actionable insights for users

## Slide-11(Conclusion & Future Work)

**Conclusion:**
- Complete System: Real-time monitoring using ESP32, MQTT, and Django backend
- AI-Powered: Uses Ollama LLM (llama3.2:1b) to provide clear, easy-to-read alerts
- Privacy-Protected: Dual-layer security with differential privacy and RSA-2048 encryption
- Reliable: Fast response, sends email alerts, and maintains strong data protection
- Proven: Successfully works end-to-end from sensor readings to dashboard display

**Future Work:**
- Enhanced AI: Integrate advanced local LLMs for improved anomaly detection
- Better Security: Strengthen encryption and implement TLS for MQTT
- More Hardware: Support additional sensors and device types
- Scalability: Test latency and accuracy for larger deployments

