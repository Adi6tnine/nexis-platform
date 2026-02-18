"""
Credit Trust Scoring Model
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import shap
from typing import Tuple, Dict
import os


class CreditTrustModel:
    """
    Explainable credit trust scoring model
    Uses Random Forest for interpretability and stability
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.explainer = None
        self.feature_names = None
        
    def train(self, X: pd.DataFrame, y: np.ndarray) -> Dict:
        """
        Train the credit trust model
        
        Args:
            X: Feature DataFrame
            y: Target labels (risk categories: 0=Low, 1=Moderate, 2=High)
            
        Returns:
            Training metrics
        """
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest (interpretable and stable)
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced data
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Create SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'n_features': len(self.feature_names),
            'n_samples': len(X)
        }
    
    def predict_score(self, X: pd.DataFrame) -> Tuple[int, str, float]:
        """
        Predict credit trust score
        
        Args:
            X: Feature DataFrame (single row)
            
        Returns:
            Tuple of (trust_score, risk_level, confidence)
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained or loaded")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict risk category
        risk_category = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = float(probabilities[risk_category])
        
        # Convert risk category to trust score (300-900)
        # Low risk (0) -> 700-900
        # Moderate risk (1) -> 500-699
        # High risk (2) -> 300-499
        
        if risk_category == 0:  # Low risk
            base_score = 700
            score_range = 200
        elif risk_category == 1:  # Moderate risk
            base_score = 500
            score_range = 199
        else:  # High risk
            base_score = 300
            score_range = 199
        
        # Use confidence to determine position within range
        trust_score = int(base_score + (confidence * score_range))
        
        # Map to risk level string
        risk_levels = {
            0: "Low",
            1: "Low-Moderate" if trust_score >= 600 else "Moderate",
            2: "High"
        }
        risk_level = risk_levels[risk_category]
        
        return trust_score, risk_level, confidence
    
    def explain_prediction(self, X: pd.DataFrame) -> Dict:
        """
        Generate SHAP-based explanation
        
        Args:
            X: Feature DataFrame (single row)
            
        Returns:
            Dictionary with SHAP values and feature contributions
        """
        if self.explainer is None:
            raise ValueError("Explainer not initialized")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_scaled)
        
        # For multi-class, take the predicted class SHAP values
        predicted_class = self.model.predict(X_scaled)[0]
        class_shap_values = shap_values[predicted_class][0]
        
        # Create explanation dictionary
        explanations = []
        for i, feature_name in enumerate(self.feature_names):
            if i < len(class_shap_values):  # Safety check
                explanations.append({
                    'feature': feature_name,
                    'value': float(X.iloc[0][feature_name]),
                    'shap_value': float(class_shap_values[i]),
                    'impact': 'positive' if class_shap_values[i] > 0 else 'negative'
                })
        
        # Sort by absolute SHAP value
        explanations.sort(key=lambda x: abs(x['shap_value']), reverse=True)
        
        return {
            'explanations': explanations,
            'base_value': float(self.explainer.expected_value[predicted_class]),
            'predicted_class': int(predicted_class)
        }
    
    def save(self, model_path: str, scaler_path: str, explainer_path: str):
        """Save model, scaler, and explainer"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump({
            'explainer': self.explainer,
            'feature_names': self.feature_names
        }, explainer_path)
    
    def load(self, model_path: str, scaler_path: str, explainer_path: str):
        """Load model, scaler, and explainer"""
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        explainer_data = joblib.load(explainer_path)
        self.explainer = explainer_data['explainer']
        self.feature_names = explainer_data['feature_names']


def generate_synthetic_training_data(n_samples: int = 1000) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Generate synthetic training data for model development
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (features DataFrame, target array)
    """
    np.random.seed(42)
    
    from .feature_engineering import FeatureEngineer
    
    data = []
    labels = []
    
    for _ in range(n_samples):
        # Generate correlated behavioral data
        # Low risk profile (40%)
        if np.random.random() < 0.4:
            raw_data = {
                'utility_payment_months': np.random.randint(12, 36),
                'utility_payment_consistency': np.random.uniform(0.85, 1.0),
                'monthly_transaction_count': np.random.randint(30, 80),
                'transaction_regularity_score': np.random.uniform(0.75, 1.0),
                'spending_volatility': np.random.uniform(0.0, 0.2),
                'avg_month_end_balance': np.random.uniform(3000, 15000),
                'savings_growth_rate': np.random.uniform(0.05, 0.3),
                'withdrawal_discipline_score': np.random.uniform(0.7, 1.0),
                'income_regularity_score': np.random.uniform(0.8, 1.0),
                'income_stability_months': np.random.randint(12, 48),
                'account_tenure_months': np.random.randint(24, 120),
                'address_stability_years': np.random.uniform(2.0, 10.0),
                'discretionary_income_ratio': np.random.uniform(0.15, 0.35)
            }
            label = 0  # Low risk
        
        # Moderate risk profile (40%)
        elif np.random.random() < 0.75:
            raw_data = {
                'utility_payment_months': np.random.randint(6, 18),
                'utility_payment_consistency': np.random.uniform(0.6, 0.85),
                'monthly_transaction_count': np.random.randint(15, 45),
                'transaction_regularity_score': np.random.uniform(0.5, 0.75),
                'spending_volatility': np.random.uniform(0.2, 0.5),
                'avg_month_end_balance': np.random.uniform(1000, 5000),
                'savings_growth_rate': np.random.uniform(-0.05, 0.15),
                'withdrawal_discipline_score': np.random.uniform(0.4, 0.7),
                'income_regularity_score': np.random.uniform(0.5, 0.8),
                'income_stability_months': np.random.randint(6, 24),
                'account_tenure_months': np.random.randint(12, 48),
                'address_stability_years': np.random.uniform(1.0, 4.0),
                'discretionary_income_ratio': np.random.uniform(0.1, 0.25)
            }
            label = 1  # Moderate risk
        
        # High risk profile (20%)
        else:
            raw_data = {
                'utility_payment_months': np.random.randint(0, 8),
                'utility_payment_consistency': np.random.uniform(0.3, 0.6),
                'monthly_transaction_count': np.random.randint(5, 25),
                'transaction_regularity_score': np.random.uniform(0.2, 0.5),
                'spending_volatility': np.random.uniform(0.5, 0.9),
                'avg_month_end_balance': np.random.uniform(0, 2000),
                'savings_growth_rate': np.random.uniform(-0.3, 0.05),
                'withdrawal_discipline_score': np.random.uniform(0.1, 0.4),
                'income_regularity_score': np.random.uniform(0.2, 0.5),
                'income_stability_months': np.random.randint(0, 12),
                'account_tenure_months': np.random.randint(3, 24),
                'address_stability_years': np.random.uniform(0.5, 2.0),
                'discretionary_income_ratio': np.random.uniform(0.05, 0.15)
            }
            label = 2  # High risk
        
        # Engineer features
        features = FeatureEngineer.engineer_features(raw_data)
        data.append(features.iloc[0])
        labels.append(label)
    
    X = pd.DataFrame(data)
    y = np.array(labels)
    
    return X, y
