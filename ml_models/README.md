# IoTShield ML Models

This directory contains machine learning models for anomaly detection.

## Files

- `train_model.py` - Training script for Isolation Forest model
- `evaluate_model.py` - Model evaluation script
- `model.pkl` - Trained model (generated after training)
- `dataset/` - Training datasets
- `notebooks/` - Jupyter notebooks for analysis

## Usage

### Train the Model

```bash
cd ml_models
python train_model.py
```

This will generate a trained model file `model.pkl` that will be used by the backend for real-time anomaly detection.

## Model Details

- **Algorithm**: Isolation Forest
- **Purpose**: Unsupervised anomaly detection
- **Features**: Statistical features from sensor readings
- **Contamination**: 0.1 (10% expected anomaly rate)
