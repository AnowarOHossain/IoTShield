# IoTShield ML Models

This directory contains machine learning models for IoT sensor anomaly detection in the IoTShield system.

## Directory Structure

```
ml_models/
├── dataset/
│   └── sensor_data.csv          # 10,000 sensor samples with labels
├── notebooks/
│   └── sensor_data_analysis.ipynb  # Complete ML analysis workflow
├── train_model.py                # Automated training script
├── model.pkl                     # Trained Isolation Forest model
├── score_distribution.png        # Anomaly score visualization
└── README.md                     # This file
```

## Dataset

**File**: `dataset/sensor_data.csv`
- **Samples**: 10,000 sensor readings
- **Time Period**: 30 days (5-minute intervals)
- **Sensors**: Temperature, Humidity, Gas, Flame, Motion, Light
- **Devices**: ESP32_001, ESP32_002, ESP32_003, RPI_001
- **Locations**: Living Room, Kitchen, Bedroom, Garage
- **Labels**: 90% normal, 10% anomalies

## Usage

### 1. Train the Model (Automated)

```bash
cd ml_models
python train_model.py
```

**Output**:
- `model.pkl` - Trained Isolation Forest model
- `score_distribution.png` - Anomaly score distribution plot

### 2. Analyze Dataset (Interactive)

```bash
jupyter notebook notebooks/sensor_data_analysis.ipynb
```

**Notebook Sections**:
1. Load and explore dataset
2. Data preprocessing and cleaning
3. Exploratory data analysis (EDA)
4. Feature engineering
5. Train-test split
6. Train multiple ML models
7. Model evaluation and comparison
8. Save best models

### 3. Integration with Django Backend

The trained model (`model.pkl`) is automatically loaded by:
- `iotshield_backend/anomaly_detector.py`

## Model Details

### Isolation Forest (Primary Model)
- **Type**: Unsupervised anomaly detection
- **Algorithm**: Isolation Forest
- **Estimators**: 100 trees
- **Contamination**: 0.1 (10% anomaly rate)
- **Features**: 
  - Current sensor value
  - Historical mean
  - Historical standard deviation
  - Historical max/min
  - Deviation from mean

### Random Forest Classifier (Alternative)
- **Type**: Supervised classification
- **Algorithm**: Random Forest
- **Estimators**: 100 trees
- **Max Depth**: 10
- **Purpose**: Comparison and validation

## Model Performance

Run the Jupyter notebook to see:
- Classification reports
- Confusion matrices
- Accuracy comparisons
- Feature importance rankings

## Generated Files

After training, you will have:
- `model.pkl` - Isolation Forest model (used by system)
- `isolation_forest_model.pkl` - Isolation Forest (from notebook)
- `random_forest_classifier.pkl` - Random Forest (from notebook)
- `scaler.pkl` - Feature scaler (from notebook)
- `score_distribution.png` - Visualization

## Integration

The trained model is used by:
1. **Backend**: `iotshield_backend/anomaly_detector.py` loads `model.pkl`
2. **Real-time**: Detects anomalies in incoming sensor data
3. **Alerts**: Triggers Gemini AI alert generation for anomalies

## Retraining

To retrain with new data:
1. Replace `dataset/sensor_data.csv` with new data
2. Run `python train_model.py` or execute notebook
3. Models will be automatically updated

## Requirements

All dependencies are in `requirements.txt`:
- numpy
- pandas
- scikit-learn
- joblib
- matplotlib
- seaborn

Install with: `pip install -r requirements.txt`
