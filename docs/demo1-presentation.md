Demo-1 Presentation Slide:

**Slide-1(Title Slide)**

* **University:** Shanto-Mariam University of Creative Technology (estd 2003)
* **Project Title:** Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration
* **Presented by:**
* Anowar Hossain (ID: 221071051)
* Shihab Sarker (ID: 202071004)


* **Department:** CSE
* **Supervised By:** Tahsin Alam, Lecturer, Department Of CSE & CSIT, SMUCT

**Slide-2(Background)**

* Smart homes rely on IoT devices for automation.
* Privacy and security risks are increasing.
* Cloud dependence causes latency & data exposure.
* There is a need for real-time, intelligent, privacy-focused systems.
* **Key Concepts:** Data Privacy Shield, Real-Time Automation, Local AI Processing Unit, Secure Local Storage, Low Latency, Reduced Cloud Reliance.

**Slide-3(Literature Review - Related Work)**

| No | Focus Area | Method / Technology | Key Contribution |
| --- | --- | --- | --- |
| 1 | MQTT Smart Home | MQTT + Raspberry Pi | Low-latency smart home communication 

 |
| 2 | GenAI in IoT | Generative AI | AI-based anomaly detection 

 |
| 3 | GAN-based Security | GAN/VAE | Detects subtle IoT anomalies 

 |
| 4 | Privacy-Preserving IoT | Edge + Privacy Filtering | Protects sensitive sensor data 

 |
| 5 | Smart City IoT Security | AI + IoT | Large-scale anomaly detection 

 |
| 6 | Edge AI Smart Home | Edge AI + IoT | Low-latency secure processing 

 |
| 7 | MQTT Security Dataset | MQTT_UAD | Benchmark dataset for attacks 

 |
| 8 | GenAI IoT Security Survey | GenAI + IoT | Future security directions 

 |

**Slide-4(Key Findings & Research Gap)**

* **Key Findings:**
* MQTT is widely used for fast and lightweight smart home communication.
* Most anomaly detection systems rely on cloud-based ML, causing latency and privacy risks.
* Existing privacy solutions mainly focus on encryption, but real-time edge filtering is limited.
* Generative AI is emerging for event interpretation but is rarely used in real-time IoT monitoring.
* Most systems do not combine MQTT, Edge Privacy, and GenAI together.


* **Identified Research Gap:**
* There is still no unified real-time smart home system that jointly integrates MQTT communication + Edge-based privacy preservation + GenAI-driven anomaly interpretation into a single end-to-end framework.



**Slide-5(Problem Statement)**

* Existing IoT systems expose sensitive sensor data.
* Many rely on cloud-only processing, which leads to slow responses.
* There is a lack of contextual anomaly explanations.
* There is a need for a low-latency, privacy-preserving, AI-supported solution.
* **Goal:** A desired solution featuring Privacy-Preserving (Local AI), Quick Response & Explanation, and AI-Supported Contextual analysis.

**Slide-6(Objectives)**
The primary objectives are:

* Ensure privacy-preserving sensor data processing.
* Detect abnormal readings using Generative AI.
* Provide human-readable safety alerts.
* Create a centralized dashboard for visualization.
* Implement real hardware integration (ESP32) for practical demonstration.
* Add user authentication and secure access.
* Enable automated email alerts for critical events using Gmail SMTP.

**Slide-7(System Architecture Overview)**

* **ESP32:** Temperature, Humidity, Gas (MQ2), Flame Sensor, Motion (PIR), Light (LDR).
* **Raspberry Pi:** Collects sensor data plus CPU Temperature, Memory Usage, Disk Usage; performs MQTT Publish.
* **Mosquitto Broker:** Runs on `localhost:1883` handling MQTT Publish/Subscribe.
* **Django MQTT Client:** Handles Data Validation, Privacy Filtering, and DB Storage.
* **Gemini AI:** Performs Anomaly Detection, Context Analysis, Alert Generation, and Suggestions.
* **Web Dashboard:** Displays Real-time Data, Alerts, Device Status, and Charts & Stats.

**Slide-8(Proposed System Overview)**

* **IoTShield:** A smart, privacy-preserving monitoring system.
* **Communication:** Uses MQTT for lightweight communication.
* **Backend:** Django backend for secure processing & storage.
* **Privacy:** Privacy filtering and encryption are applied before data reaches AI or database.
* **AI:** Gemini AI for anomaly detection & alert generation.
* **Visualization:** Dashboard for real-time visualization.

**Slide-9(Secure & Privacy-Aware Data Flow)**

1. Sensors generate raw data (example: temperature, gas, motion).
2. Local data filtering & noise injection applied at device/edge.
3. Privacy-preserved data published via MQTT to broker.
4. Django subscriber validates and sanitizes incoming data.
5. Clean data stored securely in database.
6. Gemini AI analyzes anomalies on sanitized data.
7. Interpreted alerts shown on dashboard.
8. Raw sensor data never reaches the cloud or AI without privacy protection.

**Slide-10(How Privacy & Encryption Are Implemented)**

* **Local Privacy Filtering:** Sensitive data patterns removed at device/edge.
* **Noise Injection:** Small random noise added to prevent exact user behavior tracking.
* **Encrypted MQTT Transmission:** Secure messaging blocks unauthorized access.
* **Secure Backend Storage:** Only privacy-protected data stored; no raw personal info saved.

**Slide-11(Anomaly Detection Workflow)**

1. **Rule-Based Anomaly Triggers:** Define & detect deviations based on fixed rules.
2. **Contextual Analysis Using Gemini:** AI-driven analysis for deeper insights & context.
3. **Severity Classification:** Categorize based on impact & urgency (Low / Medium / High / Critical).
4. **Human-Readable Alert Generation:** Convert findings into clear, actionable alerts.
5. **Alert Logs Stored & Shown In Dashboard:** Archive logs and visualize for monitoring.

**Slide-12(Dashboard & Features)**

* **Features:**
* Real-time live sensor readings.
* Real-time charts (temperature, gas, flame, humidity, etc.).
* Live device monitoring.
* Alert notifications with AI explanations.
* Sensor history.


* **Interface Data:** Shows Active Devices (2), Total Readings (1448), Active Alerts (198), and System Status (Online).

**Slide-13(Implementation Results)**

* **Metrics:**
* Sensor readings: 5,833
* AI alerts: 1,004
* Latency: 1.2 - 1.7 s
* System: Stable in long-run tests


* **Detected Anomalies:** Motion irregularities (High), Gas leak (Critical), Memory spikes (High), Flame detection, CPU overheating.
* **Console Logs:** Displays active status for Kitchen Edge Gateway and Living Room Sensor Hub.

**Slide-14(Conclusion & Future Work)**

* **Conclusion:**
* IoTShield enables real-time, privacy-focused smart home monitoring.
* Generative AI provides human-readable alerts and contextual anomaly interpretation.
* The system demonstrates low-latency, secure, and actionable monitoring, showing the potential for next-generation smart home security.


* **Future Work:**
* Hardware-level deployment with ESP32 and Raspberry Pi.
* Enhance privacy & encryption mechanisms for stronger data protection.
* Integrate more sensors and device types for comprehensive coverage.
* Evaluate system performance (latency, throughput, alert accuracy) in real scenarios.



**Slide-15(Appendix: IoTShield System Demo Video)**

* A complete working demonstration of the proposed IoTShield system is available.
* **The demo includes:**
* Real-time sensor data generation
* MQTT communication
* Backend data processing with privacy filtering
* GenAI-based anomaly interpretation
* Live dashboard visualization