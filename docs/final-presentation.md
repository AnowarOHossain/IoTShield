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
