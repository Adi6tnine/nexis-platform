"""
Test Suite for Rule-Based Explainability Engine
Tests explanation generation and factor formatting
"""
import pytest
from app.rules.explainability import ExplainabilityEngine
from app.rules.scoring_engine import ScoringEngine


class TestExplainabilityEngine:
    """Test the explainability engine"""
    
    @pytest.fixture
    def sample_rule_results(self):
        """Sample rule results for testing"""
        behavioral_data = {
            'utility_payment_months': 18,
            'utility_payment_consistency': 0.88,
            'monthly_transaction_count': 40,
            'transaction_regularity_score': 0.78,
            'spending_volatility': 0.18,
            'withdrawal_discipline_score': 0.75,
            'avg_month_end_balance': 5000,
            'savings_growth_rate': 0.12,
            'income_regularity_score': 0.85,
            'income_stability_months': 20,
            'account_tenure_months': 36,
            'address_stability_years': 3.5,
            'discretionary_income_ratio': 0.22
        }
        result = ScoringEngine.calculate_score(behavioral_data)
        return result['rule_results']
    
    def test_generate_factors_returns_list(self, sample_rule_results):
        """Test that generate_factors returns a list"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        assert isinstance(factors, list)
        assert len(factors) > 0
        assert len(factors) <= 8  # Should return top 8
    
    def test_factor_structure(self, sample_rule_results):
        """Test that factors have correct structure"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        for factor in factors:
            # Required fields
            assert 'id' in factor
            assert 'rule_id' in factor
            assert 'rule_name' in factor
            assert 'category' in factor
            assert 'type' in factor
            assert 'title' in factor
            assert 'description' in factor
            assert 'impact' in factor
            assert 'icon' in factor
            assert 'user_value' in factor
            assert 'required_threshold' in factor
            assert 'threshold_met' in factor
            assert 'points_earned' in factor
            assert 'max_points' in factor
            assert 'status' in factor
            
            # Value validations
            assert factor['type'] in ['positive', 'neutral', 'negative']
            assert factor['impact'] in ['High', 'Medium', 'Low']
            assert factor['status'] in ['Fully Satisfied', 'Partially Satisfied', 'Not Satisfied']
            assert isinstance(factor['threshold_met'], bool)
    
    def test_factor_descriptions_contain_rule_info(self, sample_rule_results):
        """Test that descriptions contain rule identification"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        for factor in factors:
            description = factor['description']
            # Should contain rule ID
            assert f"Rule {factor['rule_id']}" in description
            # Should contain status indicator
            assert ('✓' in description or '⚠' in description)
            # Should contain value and threshold
            assert 'Your Value:' in description or 'Your value:' in description.lower()
    
    def test_no_ai_ml_terminology(self, sample_rule_results):
        """Test that explanations don't contain AI/ML terminology"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        forbidden_terms = [
            'ai', 'ml', 'machine learning', 'artificial intelligence',
            'model', 'prediction', 'confidence', 'shap', 'algorithm',
            'neural', 'training', 'correlates strongly'
        ]
        
        for factor in factors:
            description_lower = factor['description'].lower()
            title_lower = factor['title'].lower()
            
            for term in forbidden_terms:
                assert term not in description_lower, f"Found forbidden term '{term}' in description"
                assert term not in title_lower, f"Found forbidden term '{term}' in title"
    
    def test_factors_sorted_by_impact(self, sample_rule_results):
        """Test that factors are sorted by points earned"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        # Check that factors are sorted by points (descending)
        points = [f['points_earned'] for f in factors]
        assert points == sorted(points, reverse=True), "Factors should be sorted by points earned"
    
    def test_generate_rule_summary(self, sample_rule_results):
        """Test rule summary generation"""
        summary = ExplainabilityEngine.generate_rule_summary(sample_rule_results)
        
        # Check structure
        assert 'by_category' in summary
        assert 'total_rules' in summary
        assert 'rules_satisfied' in summary
        assert 'rules_partial' in summary
        assert 'rules_not_met' in summary
        
        # Check values
        assert summary['total_rules'] == 12
        assert summary['rules_satisfied'] + summary['rules_partial'] + summary['rules_not_met'] == 12
        
        # Check categories
        categories = summary['by_category']
        assert isinstance(categories, dict)
        
        for category, stats in categories.items():
            assert 'total_rules' in stats
            assert 'satisfied' in stats
            assert 'partial' in stats
            assert 'not_met' in stats
            assert 'total_points' in stats
            assert 'max_points' in stats
    
    def test_positive_factors_have_satisfied_status(self, sample_rule_results):
        """Test that positive factors have 'Fully Satisfied' status"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        positive_factors = [f for f in factors if f['type'] == 'positive']
        for factor in positive_factors:
            assert factor['status'] == 'Fully Satisfied'
            assert factor['threshold_met'] is True
            assert factor['impact'] == 'High'
    
    def test_negative_factors_have_not_satisfied_status(self, sample_rule_results):
        """Test that negative factors have 'Not Satisfied' status"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        negative_factors = [f for f in factors if f['type'] == 'negative']
        for factor in negative_factors:
            assert factor['status'] == 'Not Satisfied'
            assert factor['impact'] == 'Low'
    
    def test_all_rule_ids_valid(self, sample_rule_results):
        """Test that all rule IDs are valid"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        valid_rule_ids = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2']
        
        for factor in factors:
            assert factor['rule_id'] in valid_rule_ids, f"Invalid rule ID: {factor['rule_id']}"
    
    def test_all_categories_valid(self, sample_rule_results):
        """Test that all categories are valid"""
        factors = ExplainabilityEngine.generate_factors(sample_rule_results)
        
        valid_categories = [
            'Payment Discipline',
            'Financial Engagement',
            'Financial Discipline',
            'Savings Behavior',
            'Income Stability',
            'Historical Stability'
        ]
        
        for factor in factors:
            assert factor['category'] in valid_categories, f"Invalid category: {factor['category']}"
    
    def test_top_n_parameter(self):
        """Test that top_n parameter limits results"""
        behavioral_data = {
            'utility_payment_months': 18,
            'utility_payment_consistency': 0.88,
            'monthly_transaction_count': 40,
            'transaction_regularity_score': 0.78,
            'spending_volatility': 0.18,
            'withdrawal_discipline_score': 0.75,
            'avg_month_end_balance': 5000,
            'savings_growth_rate': 0.12,
            'income_regularity_score': 0.85,
            'income_stability_months': 20,
            'account_tenure_months': 36,
            'address_stability_years': 3.5,
            'discretionary_income_ratio': 0.22
        }
        result = ScoringEngine.calculate_score(behavioral_data)
        
        factors_3 = ExplainabilityEngine.generate_factors(result['rule_results'], top_n=3)
        factors_5 = ExplainabilityEngine.generate_factors(result['rule_results'], top_n=5)
        factors_12 = ExplainabilityEngine.generate_factors(result['rule_results'], top_n=12)
        
        assert len(factors_3) == 3
        assert len(factors_5) == 5
        assert len(factors_12) == 12


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
