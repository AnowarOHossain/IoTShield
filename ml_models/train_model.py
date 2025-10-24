"""
ML Model Training Script for IoTShield
Train Isolation Forest model for anomaly detection
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_training_data(n_samples=10000):
    """Generate synthetic training data"""
    print(f"Generating {n_samples} training samples...")
    
    # Normal data distribution
    normal_temp = np.random.normal(25, 3, int(n_samples * 0.9))
    normal_humidity = np.random.normal(60, 10, int(n_samples * 0.9))
    normal_gas = np.random.normal(0.1, 0.05, int(n_samples * 0.9))
    normal_light = np.random.normal(300, 100, int(n_samples * 0.9))
    
    # Anomalous data (10%)
    anomaly_temp = np.random.choice([
        np.random.uniform(40, 50, int(n_samples * 0.05)),
        np.random.uniform(5, 15, int(n_samples * 0.05))
    ]).flatten()
    
    anomaly_humidity = np.random.uniform(85, 95, int(n_samples * 0.1))
    anomaly_gas = np.random.uniform(0.7, 0.95, int(n_samples * 0.1))
    anomaly_light = np.random.choice([
        np.random.uniform(0, 50, int(n_samples * 0.05)),
        np.random.uniform(900, 1500, int(n_samples * 0.05))
    ]).flatten()
    
    # Combine normal and anomalous data
    temperature = np.concatenate([normal_temp, anomaly_temp])
    humidity = np.concatenate([normal_humidity, anomaly_humidity])
    gas = np.concatenate([normal_gas, anomaly_gas])
    light = np.concatenate([normal_light, anomaly_light])
    
    # Calculate statistical features
    data = []
    for i in range(len(temperature)):
        # Current values
        temp = temperature[i]
        hum = humidity[i % len(humidity)]
        g = gas[i % len(gas)]
        l = light[i % len(light)]
        
        # Statistical features (simulated historical)
        mean_temp = 25 + np.random.normal(0, 1)
        std_temp = 3 + np.random.normal(0, 0.5)
        
        features = [
            temp,  # Current temperature
            mean_temp,  # Historical mean
            std_temp,  # Historical std
            35,  # Historical max
            15,  # Historical min
            temp - mean_temp,  # Deviation from mean
        ]
        
        data.append(features)
    
    return np.array(data)


def train_model(X_train, contamination=0.1):
    """Train Isolation Forest model"""
    print("\nTraining Isolation Forest model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Contamination factor: {contamination}")
    
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100,
        max_samples='auto',
        verbose=1
    )
    
    model.fit(X_train)
    
    return model


def evaluate_model(model, X_test):
    """Evaluate model performance"""
    print("\nEvaluating model...")
    
    # Predictions
    predictions = model.predict(X_test)
    anomaly_scores = model.score_samples(X_test)
    
    # Count anomalies
    n_anomalies = np.sum(predictions == -1)
    anomaly_rate = n_anomalies / len(X_test) * 100
    
    print(f"Test samples: {len(X_test)}")
    print(f"Detected anomalies: {n_anomalies} ({anomaly_rate:.2f}%)")
    print(f"Score range: [{anomaly_scores.min():.3f}, {anomaly_scores.max():.3f}]")
    
    return predictions, anomaly_scores


def save_model(model, output_path='model.pkl'):
    """Save trained model"""
    print(f"\nSaving model to {output_path}...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(model, output_path)
    
    print("Model saved successfully!")


def main():
    """Main training pipeline"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     IoTShield ML Model Training Script               ║
    ║   Anomaly Detection using Isolation Forest           ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Generate training data
    data = generate_training_data(n_samples=10000)
    
    # Split data
    X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)
    
    # Train model
    model = train_model(X_train, contamination=0.1)
    
    # Evaluate model
    predictions, scores = evaluate_model(model, X_test)
    
    # Save model
    output_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    save_model(model, output_path)
    
    print("\n" + "="*60)
    print("Training completed successfully!")
    print("="*60)
    
    # Optional: Plot score distribution
    try:
        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=50, edgecolor='black')
        plt.xlabel('Anomaly Score')
        plt.ylabel('Frequency')
        plt.title('Distribution of Anomaly Scores')
        plt.axvline(x=-0.05, color='r', linestyle='--', label='Typical threshold')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(os.path.dirname(__file__), 'score_distribution.png'))
        print("\nScore distribution plot saved!")
    except Exception as e:
        print(f"Could not generate plot: {e}")


if __name__ == '__main__':
    main()
