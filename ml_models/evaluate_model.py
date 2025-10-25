"""
Model Evaluation Script for IoTShield
Test and evaluate the trained Isolation Forest model
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_model(model_path='model.pkl'):
    """Load trained model"""
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found!")
        print("Please train the model first by running: python train_model.py")
        return None
    
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    print("Model loaded successfully!")
    return model


def load_test_data(csv_path='dataset/sensor_data.csv'):
    """Load test data from CSV"""
    if not os.path.exists(csv_path):
        print(f"Error: Dataset '{csv_path}' not found!")
        return None, None
    
    print(f"Loading test data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Use last 20% as test data
    test_size = int(len(df) * 0.2)
    test_df = df.tail(test_size)
    
    # Extract features
    feature_columns = ['temperature', 'humidity', 'gas_level', 
                      'flame_detected', 'motion_detected', 'light_level']
    
    X_test = test_df[feature_columns].values
    y_test = test_df['is_anomaly'].values
    
    print(f"Test samples: {len(X_test)}")
    print(f"Anomalies: {y_test.sum()} ({y_test.sum()/len(y_test)*100:.2f}%)")
    
    return X_test, y_test


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Convert predictions: 1 for normal, -1 for anomaly
    y_pred = (predictions == -1).astype(int)
    
    # Get anomaly scores
    scores = model.score_samples(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy*100:.2f}%")
    print(f"\nDetected anomalies: {y_pred.sum()} / {len(y_test)}")
    print(f"True anomalies: {y_test.sum()} / {len(y_test)}")
    
    # Classification report
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Normal', 'Anomaly']))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    return y_pred, scores, cm, accuracy


def visualize_results(y_test, y_pred, scores, cm, accuracy):
    """Visualize evaluation results"""
    print("\nGenerating visualizations...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Confusion Matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Normal', 'Anomaly'],
                yticklabels=['Normal', 'Anomaly'])
    axes[0].set_title(f'Confusion Matrix\nAccuracy: {accuracy*100:.2f}%', 
                     fontsize=12, fontweight='bold')
    axes[0].set_ylabel('True Label')
    axes[0].set_xlabel('Predicted Label')
    
    # Anomaly Score Distribution
    axes[1].hist(scores, bins=50, edgecolor='black', alpha=0.7)
    axes[1].axvline(x=-0.05, color='r', linestyle='--', 
                   label='Typical threshold', linewidth=2)
    axes[1].set_title('Anomaly Score Distribution', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Anomaly Score')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_path = 'evaluation_results.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    plt.show()


def main():
    """Main evaluation pipeline"""
    print("""
    ============================================================
         IoTShield Model Evaluation Script
       Test Trained Isolation Forest Model
    ============================================================
    """)
    
    # Change to ml_models directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Load model
    model = load_model('model.pkl')
    if model is None:
        return
    
    # Load test data
    X_test, y_test = load_test_data('dataset/sensor_data.csv')
    if X_test is None:
        return
    
    # Evaluate model
    y_pred, scores, cm, accuracy = evaluate_model(model, X_test, y_test)
    
    # Visualize results
    visualize_results(y_test, y_pred, scores, cm, accuracy)
    
    print("\n" + "="*60)
    print("Evaluation completed successfully!")
    print("="*60)
    
    # Summary
    print("\nSummary:")
    print(f"  Model Performance: {accuracy*100:.2f}% accuracy")
    print(f"  True Positives: {cm[1,1]} (correctly detected anomalies)")
    print(f"  False Positives: {cm[0,1]} (normal flagged as anomaly)")
    print(f"  True Negatives: {cm[0,0]} (correctly detected normal)")
    print(f"  False Negatives: {cm[1,0]} (missed anomalies)")
    
    # Calculate additional metrics
    if cm[1,1] + cm[1,0] > 0:
        recall = cm[1,1] / (cm[1,1] + cm[1,0])
        print(f"\n  Recall (Detection Rate): {recall*100:.2f}%")
    
    if cm[1,1] + cm[0,1] > 0:
        precision = cm[1,1] / (cm[1,1] + cm[0,1])
        print(f"  Precision: {precision*100:.2f}%")


if __name__ == '__main__':
    main()
