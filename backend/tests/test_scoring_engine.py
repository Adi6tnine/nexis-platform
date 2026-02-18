"""
Test Suite for Rule-Based Scoring Engine
Tests deterministic score calculation with known inputs
"""
import pytest
from app.rules.scoring_engine import ScoringEngine


class TestScoringEngine:
    """Test the deterministic scoring engine"""
    
    def test_perfect_score_calculation(self):
        """Test calculation with perfect behavioral data"""
        behavioral_data = {
            'utility_payment_months': 24,
            'utility_payment_consistency': 0.98,
            'monthly_transaction_count': 50,
            'transaction_regularity_score': 0.90,
            'spending_volatility': 0.10,
            'withdrawal_discipline_score': 0.85,
            'avg_month_end_balance': 8000,
            'savings_growth_rate': 0.15,
            'income_regularity_score': 0.92,
            'income_stability_months': 24,
            'account_tenure_months': 48,
            'address_stability_years': 5.0,
            'discretionary_income_ratio': 0.25
        }
        
        result = ScoringEngine.calculate_score(behavioral_data)
        
        # Assertions
        assert result['trust_score'] >= 750, "Perfect data should yield high score"
        assert result['trust_score'] <= 860, "Score should not exceed maximum"
        assert result['risk_level'] == 'Low', "Perfect data should be low risk"
        assert result['rules_evaluated'] == 12, "All 12 rules should be evaluated"
        assert result['rules_satisfied'] >= 10, "Most rules should be satisfied"
        assert result['total_points'] > 300, "Should earn substantial points"
        assert result['max_points'] == 360, "Maximum points should be 360"
    
    def test_poor_score_calculation(self):
        """Test calculation with poor behavioral data"""
        behavioral_data = {
            'utility_payment_months': 3,
            'utility_payment_consistency': 0.45,
            'monthly_transaction_count': 8,
            'transaction_regularity_score': 0.35,
            'spending_volatility': 0.75,
            'withdrawal_discipline_score': 0.30,
            'avg_month_end_balance': 500,
            'savings_growth_rate': -0.10,
            'income_regularity_score': 0.40,
            'income_stability_months': 4,
            'account_tenure_months': 6,
            'address_stability_years': 0.5,
            'discretionary_income_ratio': 0.08
        }
        
        result = ScoringEngine.calculate_score(behavioral_data)
        
        # Assertions
        assert result['trust_score'] >= 420, "Score should not go below minimum"
        assert result['trust_score'] < 550, "Poor data should yield lower score"
        assert result['risk_level'] in ['High', 'Moderate'], "Poor data should be higher risk"
        assert result['rules_evaluated'] == 12, "All 12 rules should be evaluated"
        assert result['rules_not_met'] > 0, "Some rules should not be met"
    
    def test_moderate_score_calculation(self):
        """Test calculation with moderate behavioral data"""
        behavioral_data = {
            'utility_payment_months': 14,
            'utility_payment_consistency': 0.78,
            'monthly_transaction_count': 28,
            'transaction_regularity_score': 0.68,
            'spending_volatility': 0.28,
            'withdrawal_discipline_score': 0.65,
            'avg_month_end_balance': 3000,
            'savings_growth_rate': 0.06,
            'income_regularity_score': 0.72,
            'income_stability_months': 14,
            'account_tenure_months': 26,
            'address_stability_years': 2.2,
            'discretionary_income_ratio': 0.18
        }
        
        result = ScoringEngine.calculate_score(behavioral_data)
        
        # Assertions
        assert 550 <= result['trust_score'] < 700, "Moderate data should yield moderate score"
        assert result['risk_level'] == 'Moderate', "Should be moderate risk"
        assert result['rules_evaluated'] == 12, "All 12 rules should be evaluated"
        assert result['rules_satisfied'] > 0, "Some rules should be satisfied"
        assert result['rules_partial'] > 0, "Some rules should be partial"
    
    def test_deterministic_calculation(self):
        """Test that same input always produces same output"""
        behavioral_data = {
            'utility_payment_months': 16,
            'utility_payment_consistency': 0.85,
            'monthly_transaction_count': 35,
            'transaction_regularity_score': 0.75,
            'spending_volatility': 0.20,
            'withdrawal_discipline_score': 0.70,
            'avg_month_end_balance': 4500,
            'savings_growth_rate': 0.10,
            'income_regularity_score': 0.80,
            'income_stability_months': 18,
            'account_tenure_months': 30,
            'address_stability_years': 3.0,
            'discretionary_income_ratio': 0.20
        }
        
        # Calculate multiple times
        result1 = ScoringEngine.calculate_score(behavioral_data)
        result2 = ScoringEngine.calculate_score(behavioral_data)
        result3 = ScoringEngine.calculate_score(behavioral_data)
        
        # All results should be identical
        assert result1['trust_score'] == result2['trust_score'] == result3['trust_score']
        assert result1['total_points'] == result2['total_points'] == result3['total_points']
        assert result1['rules_satisfied'] == result2['rules_satisfied'] == result3['rules_satisfied']
    
    def test_score_bounds(self):
        """Test that scores stay within 420-860 range"""
        # Test with extreme high values
        high_data = {k: 999999 for k in [
            'utility_payment_months', 'monthly_transaction_count',
            'avg_month_end_balance', 'income_stability_months',
            'account_tenure_months', 'address_stability_years'
        ]}
        high_data.update({k: 1.0 for k in [
            'utility_payment_consistency', 'transaction_regularity_score',
            'withdrawal_discipline_score', 'income_regularity_score',
            'discretionary_income_ratio'
        ]})
        high_data['spending_volatility'] = 0.0
        high_data['savings_growth_rate'] = 1.0
        
        result_high = ScoringEngine.calculate_score(high_data)
        assert result_high['trust_score'] <= 860, "Score should not exceed 860"
        
        # Test with extreme low values
        low_data = {k: 0 for k in high_data.keys()}
        result_low = ScoringEngine.calculate_score(low_data)
        assert result_low['trust_score'] >= 420, "Score should not go below 420"
    
    def test_assessment_strength_strong(self):
        """Test strong assessment strength calculation"""
        behavioral_data = {k: 20 for k in [
            'utility_payment_months', 'monthly_transaction_count',
            'income_stability_months', 'account_tenure_months'
        ]}
        behavioral_data.update({k: 0.9 for k in [
            'utility_payment_consistency', 'transaction_regularity_score',
            'spending_volatility', 'withdrawal_discipline_score',
            'income_regularity_score', 'discretionary_income_ratio'
        ]})
        behavioral_data['avg_month_end_balance'] = 5000
        behavioral_data['savings_growth_rate'] = 0.1
        behavioral_data['address_stability_years'] = 3.0
        
        strength = ScoringEngine.get_assessment_strength(behavioral_data, 20)
        assert strength == 'Strong', "Complete data with 20 months should be Strong"
    
    def test_assessment_strength_moderate(self):
        """Test moderate assessment strength calculation"""
        behavioral_data = {k: 14 for k in [
            'utility_payment_months', 'monthly_transaction_count',
            'income_stability_months', 'account_tenure_months'
        ]}
        behavioral_data.update({k: 0.7 for k in [
            'utility_payment_consistency', 'transaction_regularity_score',
            'spending_volatility', 'withdrawal_discipline_score',
            'income_regularity_score', 'discretionary_income_ratio'
        ]})
        behavioral_data['avg_month_end_balance'] = 3000
        behavioral_data['savings_growth_rate'] = 0.05
        behavioral_data['address_stability_years'] = 2.0
        
        strength = ScoringEngine.get_assessment_strength(behavioral_data, 14)
        assert strength == 'Moderate', "Partial data with 14 months should be Moderate"
    
    def test_assessment_strength_weak(self):
        """Test weak assessment strength calculation"""
        behavioral_data = {k: 5 for k in [
            'utility_payment_months', 'monthly_transaction_count',
            'income_stability_months', 'account_tenure_months'
        ]}
        behavioral_data.update({k: 0.5 for k in [
            'utility_payment_consistency', 'transaction_regularity_score',
            'spending_volatility', 'withdrawal_discipline_score',
            'income_regularity_score', 'discretionary_income_ratio'
        ]})
        behavioral_data['avg_month_end_balance'] = 1000
        behavioral_data['savings_growth_rate'] = 0.0
        behavioral_data['address_stability_years'] = 0.5
        
        strength = ScoringEngine.get_assessment_strength(behavioral_data, 8)
        assert strength == 'Weak', "Limited data with 8 months should be Weak"
    
    def test_rule_match_level_high(self):
        """Test high rule match level"""
        match_level = ScoringEngine.get_rule_match_level(10, 12)
        assert match_level == 'High', "10/12 rules satisfied should be High"
    
    def test_rule_match_level_medium(self):
        """Test medium rule match level"""
        match_level = ScoringEngine.get_rule_match_level(7, 12)
        assert match_level == 'Medium', "7/12 rules satisfied should be Medium"
    
    def test_rule_match_level_low(self):
        """Test low rule match level"""
        match_level = ScoringEngine.get_rule_match_level(3, 12)
        assert match_level == 'Low', "3/12 rules satisfied should be Low"
    
    def test_rule_results_structure(self):
        """Test that rule results have correct structure"""
        behavioral_data = {
            'utility_payment_months': 15,
            'utility_payment_consistency': 0.80,
            'monthly_transaction_count': 30,
            'transaction_regularity_score': 0.70,
            'spending_volatility': 0.25,
            'withdrawal_discipline_score': 0.68,
            'avg_month_end_balance': 3500,
            'savings_growth_rate': 0.08,
            'income_regularity_score': 0.75,
            'income_stability_months': 15,
            'account_tenure_months': 28,
            'address_stability_years': 2.5,
            'discretionary_income_ratio': 0.19
        }
        
        result = ScoringEngine.calculate_score(behavioral_data)
        
        # Check rule results structure
        assert 'rule_results' in result
        assert len(result['rule_results']) == 12
        
        for rule in result['rule_results']:
            assert 'rule_id' in rule
            assert 'rule_name' in rule
            assert 'category' in rule
            assert 'user_value' in rule
            assert 'required_threshold' in rule
            assert 'threshold_met' in rule
            assert 'points_earned' in rule
            assert 'max_points' in rule
            assert 'status' in rule
            assert rule['status'] in ['Fully Satisfied', 'Partially Satisfied', 'Not Satisfied']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
