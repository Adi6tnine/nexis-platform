"""
Feature engineering for credit trust scoring
"""
import numpy as np
import pandas as pd
from typing import Dict, List


class FeatureEngineer:
    """Transform raw behavioral data into ML features"""
    
    FEATURE_NAMES = [
        'utility_payment_months',
        'utility_payment_consistency',
        'monthly_transaction_count',
        'transaction_regularity_score',
        'spending_volatility',
        'avg_month_end_balance',
        'savings_growth_rate',
        'withdrawal_discipline_score',
        'income_regularity_score',
        'income_stability_months',
        'account_tenure_months',
        'address_stability_years',
        'discretionary_income_ratio',
        # Engineered features
        'payment_consistency_score',
        'transaction_stability_score',
        'savings_discipline_index',
        'volatility_index',
        'income_regularity_flag',
        'tenure_score',
        'financial_health_score'
    ]
    
    @staticmethod
    def engineer_features(raw_data: Dict) -> pd.DataFrame:
        """
        Convert raw behavioral data into engineered features
        
        Args:
            raw_data: Dictionary of raw behavioral metrics
            
        Returns:
            DataFrame with engineered features
        """
        features = raw_data.copy()
        
        # 1. Payment Consistency Score (0-100)
        payment_score = (
            features['utility_payment_months'] * 2 +  # Months weight
            features['utility_payment_consistency'] * 50  # Consistency weight
        )
        features['payment_consistency_score'] = min(payment_score, 100)
        
        # 2. Transaction Stability Score (0-100)
        # Normalize transaction count (assume 50 is good)
        tx_normalized = min(features['monthly_transaction_count'] / 50, 1.0)
        transaction_score = (
            tx_normalized * 40 +
            features['transaction_regularity_score'] * 40 +
            (1 - features['spending_volatility']) * 20  # Lower volatility is better
        )
        features['transaction_stability_score'] = transaction_score
        
        # 3. Savings Discipline Index (0-100)
        # Normalize balance (assume 5000 is good baseline)
        balance_normalized = min(features['avg_month_end_balance'] / 5000, 1.0)
        savings_score = (
            balance_normalized * 40 +
            max(features['savings_growth_rate'], 0) * 30 +  # Only positive growth
            features['withdrawal_discipline_score'] * 30
        )
        features['savings_discipline_index'] = savings_score
        
        # 4. Volatility Index (0-100, lower is better, so invert)
        features['volatility_index'] = (1 - features['spending_volatility']) * 100
        
        # 5. Income Regularity Flag (binary)
        features['income_regularity_flag'] = 1 if (
            features['income_regularity_score'] >= 0.7 and
            features['income_stability_months'] >= 6
        ) else 0
        
        # 6. Tenure Score (0-100)
        # Longer tenure is better
        account_score = min(features['account_tenure_months'] / 60, 1.0) * 50
        address_score = min(features['address_stability_years'] / 5, 1.0) * 50
        features['tenure_score'] = account_score + address_score
        
        # 7. Financial Health Score (composite, 0-100)
        health_score = (
            features['payment_consistency_score'] * 0.25 +
            features['transaction_stability_score'] * 0.20 +
            features['savings_discipline_index'] * 0.25 +
            features['volatility_index'] * 0.15 +
            features['tenure_score'] * 0.15
        )
        features['financial_health_score'] = health_score
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Ensure all expected features are present
        for feature in FeatureEngineer.FEATURE_NAMES:
            if feature not in df.columns:
                df[feature] = 0.0
        
        return df[FeatureEngineer.FEATURE_NAMES]
    
    @staticmethod
    def get_feature_descriptions() -> Dict[str, str]:
        """Get human-readable descriptions for features"""
        return {
            'utility_payment_months': 'Consecutive months of on-time utility payments',
            'utility_payment_consistency': 'Consistency of utility payment behavior',
            'monthly_transaction_count': 'Average monthly digital transactions',
            'transaction_regularity_score': 'Regularity of transaction patterns',
            'spending_volatility': 'Volatility in spending behavior',
            'avg_month_end_balance': 'Average month-end account balance',
            'savings_growth_rate': 'Rate of savings growth',
            'withdrawal_discipline_score': 'Discipline in withdrawal behavior',
            'income_regularity_score': 'Regularity of income deposits',
            'income_stability_months': 'Months of stable income',
            'account_tenure_months': 'Account age in months',
            'address_stability_years': 'Years at current address',
            'discretionary_income_ratio': 'Ratio of discretionary to total income',
            'payment_consistency_score': 'Overall payment consistency',
            'transaction_stability_score': 'Overall transaction stability',
            'savings_discipline_index': 'Savings discipline indicator',
            'volatility_index': 'Financial volatility measure',
            'income_regularity_flag': 'Income regularity indicator',
            'tenure_score': 'Account and address tenure score',
            'financial_health_score': 'Composite financial health score'
        }
