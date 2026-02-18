"""
Improvement Recommendation Engine
"""
from typing import List, Dict
import pandas as pd


class ImprovementEngine:
    """
    Generate personalized, actionable improvement recommendations
    """
    
    @staticmethod
    def generate_recommendations(
        feature_values: pd.Series,
        shap_explanation: Dict,
        current_score: int
    ) -> List[Dict]:
        """
        Generate improvement recommendations based on weak signals
        
        Args:
            feature_values: User's feature values
            shap_explanation: SHAP explanation
            current_score: Current trust score
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Analyze weak points from SHAP
        weak_features = [
            exp for exp in shap_explanation['explanations']
            if exp['shap_value'] < 0  # Negative contributors
        ]
        
        # Sort by impact (most negative first)
        weak_features.sort(key=lambda x: x['shap_value'])
        
        # Generate specific recommendations
        for weak in weak_features[:5]:  # Top 5 weak points
            feature = weak['feature']
            value = weak['value']
            
            rec = ImprovementEngine._get_recommendation(feature, value, current_score)
            if rec:
                recommendations.append(rec)
        
        # Always include utility payment recommendation if not perfect
        if feature_values.get('utility_payment_months', 0) < 24:
            recommendations.insert(0, {
                'title': 'The Utility Buffer',
                'description': 'Set up auto-payments for your linked utility accounts. Consistent on-time payments for another 3 months could add ~25 points to your score.',
                'difficulty': 'Easy',
                'estimated_score_increase': 25,
                'timeframe': '3 months',
                'category': 'payment_consistency'
            })
        
        # Limit to top 3 recommendations
        return recommendations[:3]
    
    @staticmethod
    def _get_recommendation(feature: str, value: float, current_score: int) -> Dict:
        """
        Get specific recommendation for a feature
        
        Args:
            feature: Feature name
            value: Current value
            current_score: Current trust score
            
        Returns:
            Recommendation dictionary or None
        """
        recommendations_map = {
            'utility_payment_months': {
                'title': 'Build Payment History',
                'description': 'Continue paying your utility bills on time. Each additional month of perfect payments strengthens your profile.',
                'difficulty': 'Easy',
                'estimated_score_increase': 20,
                'timeframe': '3-6 months',
                'category': 'payment_history'
            },
            'account_tenure_months': {
                'title': 'Maintain Account Stability',
                'description': 'Keep your current accounts active and avoid opening too many new accounts. Longer tenure builds trust.',
                'difficulty': 'Easy',
                'estimated_score_increase': 15,
                'timeframe': '6-12 months',
                'category': 'stability'
            },
            'savings_growth_rate': {
                'title': 'Savings Consistency',
                'description': 'Avoid withdrawing more than 80% of your monthly deposits. Maintaining a larger month-end balance shows "Liquid Trust".',
                'difficulty': 'Hard',
                'estimated_score_increase': 40,
                'timeframe': '3-6 months',
                'category': 'savings'
            },
            'transaction_regularity_score': {
                'title': 'Stabilize Transaction Patterns',
                'description': 'Maintain consistent spending patterns. Avoid large irregular transactions that create volatility.',
                'difficulty': 'Medium',
                'estimated_score_increase': 30,
                'timeframe': '2-4 months',
                'category': 'behavior'
            },
            'spending_volatility': {
                'title': 'Reduce Spending Volatility',
                'description': 'Create a monthly budget and stick to it. Predictable spending patterns significantly boost your score.',
                'difficulty': 'Medium',
                'estimated_score_increase': 35,
                'timeframe': '3-6 months',
                'category': 'behavior'
            },
            'income_regularity_score': {
                'title': 'Income Consistency',
                'description': 'Maintain regular income deposits. If you have irregular income, consider setting up automatic transfers to simulate regularity.',
                'difficulty': 'Medium',
                'estimated_score_increase': 30,
                'timeframe': '3-6 months',
                'category': 'income'
            },
            'withdrawal_discipline_score': {
                'title': 'Improve Withdrawal Discipline',
                'description': 'Plan your withdrawals in advance. Avoid emergency withdrawals by maintaining a small buffer.',
                'difficulty': 'Medium',
                'estimated_score_increase': 25,
                'timeframe': '2-4 months',
                'category': 'discipline'
            },
            'financial_health_score': {
                'title': 'Micro-Credit Activity',
                'description': 'Apply for a secure credit card with a small limit ($200). Use only 30% of it and pay in full. This creates "Formal History" which is currently your biggest gap.',
                'difficulty': 'Medium',
                'estimated_score_increase': 60,
                'timeframe': '6-12 months',
                'category': 'credit_building'
            }
        }
        
        return recommendations_map.get(feature)
    
    @staticmethod
    def generate_roadmap(
        current_score: int,
        recommendations: List[Dict]
    ) -> List[Dict]:
        """
        Generate step-by-step roadmap
        
        Args:
            current_score: Current trust score
            recommendations: List of recommendations
            
        Returns:
            List of roadmap steps
        """
        roadmap = []
        
        # Step 1: Always start with easiest wins
        easy_recs = [r for r in recommendations if r['difficulty'] == 'Easy']
        if easy_recs:
            roadmap.append({
                'title': 'Maintain Bill Cycle',
                'description': 'Keep paying utilities by the 5th of every month.',
                'status': 'ongoing'
            })
        
        # Step 2: Medium difficulty
        medium_recs = [r for r in recommendations if r['difficulty'] == 'Medium']
        if medium_recs:
            roadmap.append({
                'title': 'Small Credit Product',
                'description': 'Consider a micro-savings account or a secure card to build history.',
                'status': 'next'
            })
        
        # Step 3: Long-term goals
        roadmap.append({
            'title': 'Portfolio Diversification',
            'description': 'Maintain your current spending habits without large sudden withdrawals.',
            'status': 'future'
        })
        
        return roadmap
