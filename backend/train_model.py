"""
Train Credit Trust Model
Run this script to train and save the ML model
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ml.model import CreditTrustModel, generate_synthetic_training_data
from app.core.config import settings


def main():
    """Train and save the credit trust model"""
    print("=" * 60)
    print("NEXIS Credit Trust Model Training")
    print("=" * 60)
    
    # Generate synthetic training data
    print("\n📊 Generating synthetic training data...")
    X, y = generate_synthetic_training_data(n_samples=2000)
    print(f"✅ Generated {len(X)} samples")
    print(f"   - Low Risk: {sum(y == 0)} samples")
    print(f"   - Moderate Risk: {sum(y == 1)} samples")
    print(f"   - High Risk: {sum(y == 2)} samples")
    
    # Initialize model
    print("\n🤖 Initializing model...")
    model = CreditTrustModel()
    
    # Train model
    print("\n🎯 Training model...")
    metrics = model.train(X, y)
    
    print("\n📈 Training Results:")
    print(f"   - Train Accuracy: {metrics['train_accuracy']:.2%}")
    print(f"   - Test Accuracy: {metrics['test_accuracy']:.2%}")
    print(f"   - Features: {metrics['n_features']}")
    print(f"   - Samples: {metrics['n_samples']}")
    
    # Save model
    print("\n💾 Saving model...")
    model.save(
        settings.MODEL_PATH,
        settings.SCALER_PATH,
        settings.EXPLAINER_PATH
    )
    print(f"✅ Model saved to {settings.MODEL_PATH}")
    print(f"✅ Scaler saved to {settings.SCALER_PATH}")
    print(f"✅ Explainer saved to {settings.EXPLAINER_PATH}")
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    test_sample = X.iloc[[0]]
    score, risk, confidence = model.predict_score(test_sample)
    print(f"   - Trust Score: {score}")
    print(f"   - Risk Level: {risk}")
    print(f"   - Confidence: {confidence:.2%}")
    
    # Test explanation
    print("\n📝 Testing explanation...")
    explanation = model.explain_prediction(test_sample)
    print(f"   - Top 3 features:")
    for i, exp in enumerate(explanation['explanations'][:3], 1):
        print(f"     {i}. {exp['feature']}: {exp['shap_value']:.3f} ({exp['impact']})")
    
    print("\n" + "=" * 60)
    print("✅ Model training complete!")
    print("=" * 60)
    print("\nYou can now start the API server:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print()


if __name__ == "__main__":
    main()
