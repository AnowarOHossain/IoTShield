Demo-2 Presentation Slide:

Slide-1 (Title Slide)

- University: Shanto-Mariam University of Creative Technology (estd 2003)
- Project Title: Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration
- Presented by:
  - Anowar Hossain (ID: 221071051)
  - Shihab Sarker (ID: 202071004)
- Department: CSE
- Supervised By: Tahsin Alam, Lecturer, Department Of CSE & CSIT, SMUCT


Slide-2 (Background)

Context: Smart homes rely on IoT, but privacy risks are rising.

Problem: Cloud dependence causes latency and data exposure.

Gap: Current solutions lack real-time, local intelligence.

Need: Intelligent, privacy-focused systems at the edge.

Solution: A novel architecture combining IoT, GenAI, and privacy for real-time security.


Slide-3 (Literature Review - Related Work)

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


Slide-4 (Key Findings & Research Gap)

Key Findings:
MQTT : Widely used for fast, lightweight communication.
Cloud ML: Causes latency and privacy risks due to remote processing.
Privacy Gap: Existing tools focus on encryption but lack real-time edge filtering.
GenAI Limit: Rarely integrated into real-time hardware monitoring systems.
Unmet Need: No unified framework combines MQTT, Edge Privacy, GenAI, and Hardware.


- Identified Research Gap:
  - There is still no unified real-time smart home system that jointly integrates MQTT communication, edge-based privacy preservation, GenAI-driven anomaly interpretation, and physical device implementation into a single end-to-end methodology.


Slide-5 (Problem Statement)

Data Exposure: Existing systems expose sensitive data and lack real-time privacy.

Cloud Issues: Cloud-only processing causes latency and data leakage risks.

No Context: Lacks contextual anomaly explanations and actionable alerts.

The Need: Requires a low-latency, privacy-preserving, AI-supported hardware solution.

Goal: Deliver a production-ready system featuring Local AI Privacy, Speed, Context, and seamless hardware integration.


Slide-6 (Objectives)
The primary objectives are:

Privacy: Ensure secure data processing at the edge and backend.

GenAI: Detect anomalies using Gemini for contextual alerts.

Notifications: Automate critical alerts via Gmail SMTP.

Hardware: Validate system using real ESP32 integration.

Security: Implement secure user authentication for the dashboard.

Visualization: Build a centralized real-time monitoring dashboard.

Scalability: Demonstrate a scalable, end-to-end IoT framework.


Slide-7 (Proposed System Overview)

```
╔══════════════════════════════════════════════════════════════════════╗
║                         IoTShield System                              ║
║          Privacy-Preserving IoT Monitoring with AI                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   ESP32     │  WiFi   │    MQTT     │  TCP/IP │   Django    │
│  Hardware   │ ═════► │   Broker    │ ═════► │   Backend   │
│             │  2.4GHz │  Mosquitto  │         │   + AI      │
└─────────────┘         └─────────────┘         └─────────────┘
                                                        │
                                                        ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    User     │  HTTP   │     Web     │  Query  │  Database   │
│  Browser    │ ◄═════  │  Dashboard  │ ◄═════  │   SQLite    │
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```


Key Components:
- Hardware: ESP32 Microcontroller
- Protocol: MQTT (Message Queue Telemetry Transport)
- AI: Google Gemini 2.5 Flash
- Privacy: Differential Privacy Mechanism
- Interface: Real-time Web Dashboard

This overview provides a high-level summary of our end-to-end, privacy-preserving, AI-powered IoT monitoring system with real hardware integration.

---




Slide-8 (ESP32 Hardware Implementation)

ESP32 collects sensor data and sends it securely to the backend over WiFi using MQTT, enabling real-time smart home automation.

---

Slide-9 (Mosquitto & MQTT Integration)

 Mosquitto lets ESP32 and backend exchange sensor data instantly using MQTT topics, making communication fast and reliable. (Screenshot: MQTT messages in terminal)

---




Slide-10 (Privacy-Preserving Mechanism)


```
╔══════════════════════════════════════════════════════════════════════╗
║              Differential Privacy Implementation                      ║
╚══════════════════════════════════════════════════════════════════════╝

Original Sensor Data:
┌────────────────────┐
│  Temperature: 25°C │ 
└────────────────────┘   
            │
            ▼
          ┌──────────────┐
          │ Add Gaussian │
          │    Noise     │
          │ (ε = 0.5)    │
          └──────┬───────┘
            │
            ▼
Privacy-Preserved Data:
┌────────────────────────┐
│  Temperature: 25.5°C   │
│  (Original + Noise)    │
└────────────────────────┘
```

We use differential privacy to protect sensor data by adding random noise before storage or processing. This approach ensures data remains private and secure, with customizable privacy settings for different needs.


Slide-11 (AI Anomaly Detection Workflow)

```
╔══════════════════════════════════════════════════════════════════════╗
║              AI-Powered Anomaly Detection System                      ║
╚══════════════════════════════════════════════════════════════════════╝

Normal Data Flow:
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Sensor  │────>│ Database │────>│ Dashboard│
│ Reading │     │  Store   │     │ Display  │
└─────────┘     └──────────┘     └──────────┘
   25.5°C          ✓ Normal           

Anomaly Detection Flow:
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Sensor  │────>│ Gemini AI│────>│  Alert   │
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

Gemini AI analyzes sensor data in real time to detect unusual patterns or anomalies. Critical events are classified by severity and trigger instant alerts via email, dashboard, and logs. This ensures users receive clear, actionable notifications for fast response.



Slide-12 (Implementation Results)

- Django backend: database, alerts, dashboard, user authentication, email alerts
- Screenshots: dashboard, alert emails, user login
- Show real-time data and alert generation

---

Slide-13 (Conclusion & Future Work)

Conclusion:
- IoTShield Demo 2 delivers a real-time, privacy-preserving smart home monitoring system with full hardware integration (ESP32), secure MQTT communication, and a Django-based backend.
- Generative AI (Gemini) provides contextual, human-readable anomaly alerts, improving interpretability and user actionability.
- The system achieves low-latency, high-accuracy anomaly detection, automated email notifications, and robust privacy via differential privacy mechanisms.
- Demonstrated end-to-end functionality: live sensor data, privacy filtering, AI-powered analysis, alerting, and dashboard visualization.

Future Work:
- Expand hardware support (additional sensors, more device types)
- Integrate Ollama (TinyLlama) for local GenAI to reduce cloud/API dependency
- Enhance privacy and encryption (TLS for MQTT, advanced anonymization)
- Broaden deployment to larger smart environments (multi-room, multi-user)
- Evaluate system performance at scale (latency, throughput, alert accuracy)

---


Slide-14 (Appendix: IoTShield System Demo Video)

 A complete working demonstration of the proposed IoTShield system is available.
* **The demo includes:**
ESP32 (Arduino IDE) serial output
Mosquitto terminal
Django dashboard
Sensor data and alerts in the backend/database
Gmail alerts
Live dashboard visualization for all the pages.
