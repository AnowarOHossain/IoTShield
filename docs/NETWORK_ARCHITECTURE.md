# IoTShield Network Architecture

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     IoTShield System Architecture                    │
└─────────────────────────────────────────────────────────────────────┘

┌────────────────┐         WiFi (2.4GHz)        ┌──────────────────┐
│   ESP32 Device │ ═══════════════════════════► │  WiFi Router     │
│  (Hardware)    │      802.11 b/g/n            │  (Access Point)  │
│                │                               │                  │
│ • Sensors      │                               │ DHCP Server      │
│ • WiFi Module  │                               │ NAT/Firewall     │
│ • MQTT Client  │                               │                  │
└────────────────┘                               └──────────────────┘
        │                                                 │
        │                                                 │
        │              Local Area Network (LAN)          │
        │              IP: 192.168.1.0/24                │
        │                                                 │
        ▼                                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MQTT Broker (Mosquitto)                          │
│                    Port: 1883 (TCP)                                 │
│                    Host: localhost / 192.168.1.XXX                  │
│                                                                      │
│  • Message Queue Management                                         │
│  • Pub/Sub Pattern Implementation                                   │
│  • Quality of Service (QoS) Levels                                  │
│  • Session Persistence                                              │
└─────────────────────────────────────────────────────────────────────┘
        │
        │ Subscribe to: "iotshield/sensors/data"
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│              MQTT Listener (Django Management Command)              │
│                                                                      │
│  • Subscribes to MQTT topics                                        │
│  • Parses JSON sensor data                                          │
│  • Validates data integrity                                         │
│  • Forwards to Django backend                                       │
└─────────────────────────────────────────────────────────────────────┘
        │
        │ Django ORM Insert
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Django Backend Server                            │
│                    Port: 8000 (HTTP)                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Privacy Engine                                             │   │
│  │  • Differential Privacy (Gaussian Noise)                   │   │
│  │  • Data Anonymization                                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                          │                                          │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Gemini AI Anomaly Detector                                │   │
│  │  • Google Gemini 2.5 Flash API                             │   │
│  │  • Real-time Anomaly Analysis                              │   │
│  │  • Severity Classification (CRITICAL/HIGH/MEDIUM/LOW)      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                          │                                          │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Email Alert System                                        │   │
│  │  • Gmail SMTP Integration                                  │   │
│  │  • Async Email Delivery                                    │   │
│  │  • HTML Email Templates                                    │   │
│  └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
        │
        │ Store Data
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SQLite Database                                  │
│                    File: db.sqlite3                                 │
│                                                                      │
│  Tables:                                                            │
│  • dashboard_device (Device information)                            │
│  • dashboard_sensorreading (Sensor data)                            │
│  • dashboard_alert (Anomaly alerts)                                 │
│  • auth_user (User authentication)                                  │
└─────────────────────────────────────────────────────────────────────┘
        │
        │ Query Data
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Web Dashboard (Frontend)                         │
│                    http://127.0.0.1:8000                           │
│                                                                      │
│  • Real-time Charts (Chart.js)                                      │
│  • Device Management Interface                                      │
│  • Alert Monitoring System                                          │
│  • User Authentication                                              │
│  • Responsive Design (Tailwind CSS)                                 │
└─────────────────────────────────────────────────────────────────────┘
        │
        │ Access via Browser
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    End User / System Administrator                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Network Topology

### Physical Layer
```
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │  WiFi Router    │
              │  192.168.1.1    │
              └─────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  ESP32   │  │   PC     │  │  Mobile  │
  │ Device   │  │ (Server) │  │  Device  │
  └──────────┘  └──────────┘  └──────────┘
  192.168.1.150  192.168.1.100  192.168.1.XXX
```

### Communication Protocols

| Layer | Protocol | Purpose |
|-------|----------|---------|
| Application | HTTP/HTTPS | Web Dashboard Access |
| Application | MQTT | IoT Device Communication |
| Application | SMTP | Email Alert Delivery |
| Transport | TCP | Reliable Data Transfer |
| Network | IP (IPv4) | Device Addressing |
| Data Link | WiFi (802.11) | Wireless Communication |
| Physical | 2.4GHz Radio | Wireless Transmission |

---

## 📡 Data Flow Diagram

### 1. Sensor Data Publishing (ESP32 → Backend)

```
┌─────────────┐
│   ESP32     │  Step 1: Read Sensors
│   Sensors   │  • Temperature
└──────┬──────┘  • Humidity
       │         • Gas Level
       │         • etc.
       ▼
┌─────────────┐
│   Format    │  Step 2: Create JSON
│    JSON     │  {
└──────┬──────┘    "device_id": "ESP32_001",
       │           "sensor_type": "TEMPERATURE",
       │           "value": 25.3,
       │           "unit": "°C"
       │         }
       ▼
┌─────────────┐
│   MQTT      │  Step 3: Publish to Topic
│  Publish    │  Topic: iotshield/sensors/data
└──────┬──────┘  QoS: 0 (At most once)
       │
       ▼
┌─────────────┐
│   MQTT      │  Step 4: Message Routing
│   Broker    │  Port: 1883
└──────┬──────┘  Protocol: TCP
       │
       ▼
┌─────────────┐
│   MQTT      │  Step 5: Receive Message
│  Listener   │  Subscribe: iotshield/sensors/data
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Django    │  Step 6: Process & Store
│   Backend   │  • Parse JSON
└──────┬──────┘  • Validate Data
       │         • Apply Privacy Noise
       │         • Store in Database
       ▼
┌─────────────┐
│   AI        │  Step 7: Anomaly Detection
│  Analysis   │  • Gemini API Call
└──────┬──────┘  • Severity Classification
       │         • Alert Generation
       ▼
┌─────────────┐
│   Email     │  Step 8: Alert Notification
│   Alert     │  (if CRITICAL or HIGH)
└─────────────┘
```

### 2. Dashboard Data Retrieval (User → Backend)

```
┌─────────────┐
│   User      │  Step 1: Open Browser
│  Browser    │  URL: http://127.0.0.1:8000
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   HTTP      │  Step 2: HTTP Request
│  Request    │  GET /dashboard/
└──────┬──────┘  Headers: Cookie (auth)
       │
       ▼
┌─────────────┐
│   Django    │  Step 3: Process Request
│    View     │  • Authenticate User
└──────┬──────┘  • Query Database
       │         • Render Template
       ▼
┌─────────────┐
│  Database   │  Step 4: Fetch Data
│   Query     │  SELECT * FROM sensors
└──────┬──────┘  ORDER BY timestamp DESC
       │
       ▼
┌─────────────┐
│   HTTP      │  Step 5: HTTP Response
│  Response   │  Content-Type: text/html
└──────┬──────┘  Body: Dashboard HTML + Data
       │
       ▼
┌─────────────┐
│  Render     │  Step 6: Display Dashboard
│  Dashboard  │  • Charts (Chart.js)
└─────────────┘  • Real-time Updates (JS)
```

---

## 🔒 Security Architecture

### Network Security

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Network Layer                                            │
│     • WiFi WPA2/WPA3 Encryption                             │
│     • Firewall Rules (Port Filtering)                       │
│     • Private LAN (192.168.1.0/24)                          │
│                                                              │
│  2. Transport Layer                                          │
│     • TCP Connection Security                                │
│     • (Future: TLS/SSL for MQTT)                            │
│     • HTTPS for Web Dashboard (Production)                   │
│                                                              │
│  3. Application Layer                                        │
│     • User Authentication (Django)                           │
│     • Session Management                                     │
│     • CSRF Protection                                        │
│     • JWT Token Authentication (API)                         │
│                                                              │
│  4. Data Layer                                               │
│     • Differential Privacy (Gaussian Noise)                  │
│     • Data Anonymization                                     │
│     • Encrypted Database (Future)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Privacy-Preserving Mechanism

```python
# Example: Differential Privacy Implementation
def add_privacy_noise(value, epsilon=0.5):
    """
    Add Gaussian noise for differential privacy
    """
    sensitivity = 1.0
    noise_scale = sensitivity / epsilon
    noise = np.random.normal(0, noise_scale)
    return value + noise
```

---

## 🌐 IP Addressing Scheme

| Device | IP Address | Role | Port(s) |
|--------|-----------|------|---------|
| WiFi Router | 192.168.1.1 | Gateway/DHCP | 80, 443 |
| PC (Server) | 192.168.1.100 | Django + MQTT Broker | 8000, 1883 |
| ESP32 Device | 192.168.1.150 (DHCP) | IoT Sensor Node | N/A |
| Mobile Device | 192.168.1.XXX (DHCP) | Dashboard Access | N/A |

### Port Allocation

| Port | Service | Protocol | Purpose |
|------|---------|----------|---------|
| 1883 | MQTT | TCP | Device Communication |
| 8000 | Django | HTTP | Web Dashboard |
| 8883 | MQTT-TLS | TCP | Secure MQTT (Future) |
| 443 | HTTPS | TCP | Secure Web (Production) |
| 465/587 | SMTP | TCP | Email Alerts |

---

## 📊 MQTT Topic Structure

```
iotshield/
├── sensors/
│   ├── data              # All sensor readings (ESP32 publishes here)
│   ├── status            # Device status updates (future)
│   └── heartbeat         # Device health monitoring (future)
├── control/
│   ├── commands          # Control commands to devices (future)
│   └── config            # Configuration updates (future)
└── alerts/
    ├── critical          # Critical severity alerts
    ├── high              # High severity alerts
    └── notifications     # General notifications
```

### Message Format

**Topic**: `iotshield/sensors/data`

**Payload** (JSON):
```json
{
  "device_id": "ESP32_HARDWARE_001",
  "device_name": "ESP32 Smart Sensor Hub",
  "device_type": "ESP32",
  "sensor_type": "TEMPERATURE",
  "value": 25.3,
  "unit": "°C",
  "location": "Demo Lab",
  "timestamp": "2026-01-08T10:30:45Z"
}
```

---

## ⚡ System Performance

### Latency Analysis

| Stage | Average Latency | Description |
|-------|----------------|-------------|
| Sensor Read | <10ms | ESP32 reads sensor value |
| JSON Creation | <5ms | Format data to JSON |
| WiFi Transmission | 10-50ms | Send to MQTT broker |
| MQTT Routing | <10ms | Broker to listener |
| Database Insert | 10-30ms | Store in SQLite |
| AI Analysis | 500-1000ms | Gemini API call |
| Dashboard Update | <100ms | Query and display |
| **Total (E2E)** | **~1-2 seconds** | Sensor to Dashboard |

### Throughput

- **Sensor Readings**: 6 sensors × 1 reading/5s = **1.2 readings/second**
- **Multiple Devices**: Supports 10+ devices simultaneously
- **Data Rate**: ~500 bytes/message × 1.2/s = **600 bytes/second**
- **Daily Storage**: ~50MB/day for 1 device

---

## 🔄 Fault Tolerance & Reliability

### Auto-Reconnection Mechanisms

1. **ESP32 WiFi Reconnection**
   - Timeout: 20 seconds
   - Auto-retry on disconnect
   - Status LED indicators

2. **MQTT Connection Recovery**
   - Retry interval: 5 seconds
   - Persistent session (QoS 1 future)
   - Last will message (future)

3. **Django Service Recovery**
   - MQTT listener auto-restart
   - Database connection pooling
   - Exception handling and logging

### Data Integrity

- **Validation**: JSON schema validation
- **Duplicate Detection**: Timestamp-based deduplication
- **Missing Data Handling**: Default values and interpolation
- **Error Logging**: Comprehensive logging system

---

## 📈 Scalability

### Current Capacity
- **Devices**: 1 ESP32 (expandable to 100+)
- **Sensors per Device**: 6 types
- **Data Points**: 10,000+ stored
- **Alerts**: 150+ generated
- **Users**: Unlimited (Django handles)

### Future Expansion
- **Multiple ESP32 Devices**: Each with unique ID
- **Edge Gateways**: Raspberry Pi for local processing
- **Cloud Integration**: AWS IoT / Azure IoT Hub
- **Load Balancing**: Multiple MQTT brokers
- **Distributed Database**: PostgreSQL cluster

---

## 🎯 For Demo 2

### Key Architecture Points to Highlight:

1. ✅ **Complete System Integration** - All components working together
2. ✅ **Real Hardware** - Physical ESP32 device proven
3. ✅ **Wireless Communication** - WiFi + MQTT protocol
4. ✅ **Privacy-Preserving** - Differential privacy implemented
5. ✅ **AI-Powered** - Gemini 2.5 Flash for anomaly detection
6. ✅ **Production-Ready** - Professional architecture design
7. ✅ **Scalable** - Supports multiple devices and expansion

### Live Demo Flow:

1. Show network topology diagram
2. Explain data flow step-by-step
3. Demonstrate ESP32 connection
4. Show MQTT message flow (mosquitto_sub)
5. Show real-time dashboard updates
6. Explain security and privacy features
7. Discuss scalability and future expansion

---

**Created for Demo 2: January 11, 2026**  
**Authors**: Anowar Hossain & Shihab Sarker  
**Institution**: Shanto-Mariam University of Creative Technology
