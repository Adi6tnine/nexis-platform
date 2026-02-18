"""
Test Suite for Completion Pathway Generator
Tests improvement recommendation generation
"""
import pytest
from app.rules.completion_pathway import CompletionPathwayGenerator
from app.rules.scoring_engine import ScoringEngine


class TestCompletionPathwayGenerator:
    """Test the completion pathway generator"""
    
    @pytest.fixture
    def sample_rule_results(self):
        """Sample rule results with some unmet rules"""
        behavioral_data = {
            'utility_payment_months': 10,  # Below threshold
            'utility_payment_consistency': 0.70,  # Below threshold
            'monthly_transaction_count': 20,  # Below threshold
            'transaction_regularity_score': 0.60,  # Below threshold
            'spending_volatility': 0.35,  # Above threshold (inverse)
            'withdrawal_discipline_score': 0.60,  # Below threshold
            'avg_month_end_balance': 2000,  # Below threshold
            'savings_growth_rate': 0.03,  # Below threshold
            'income_regularity_score': 0.68,  # Below threshold
            'income_stability_months': 10,  # Below threshold
            'account_tenure_months': 20,  # Below threshold
            'address_stability_years': 1.5,  # Below threshold
            'discretionary_income_ratio': 0.12  # Below threshold
        }
        result = ScoringEngine.calculate_score(behavioral_data)
        return result['rule_results'], result['trust_score']
    
    def test_generate_recommendations_returns_list(self, sample_rule_results):
        """Test that generate_recommendations returns a list"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
    
    def test_recommendation_structure(self, sample_rule_results):
        """Test that recommendations have correct structure"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            # Required fields
            assert 'rule_id' in rec
            assert 'rule_name' in rec
            assert 'action' in rec
            assert 'description' in rec
            assert 'current_value' in rec
            assert 'target_threshold' in rec
            assert 'gap' in rec
            assert 'gap_unit' in rec
            assert 'score_impact' in rec
            assert 'timeframe' in rec
            assert 'difficulty' in rec
            assert 'category' in rec
            assert 'status' in rec
            assert 'completion_criteria' in rec
            assert 'verification' in rec
            assert 'tips' in rec
            
            # Value validations
            assert rec['difficulty'] in ['Easy', 'Medium', 'Hard']
            assert rec['status'] == 'Recommended'
            assert isinstance(rec['score_impact'], int)
            assert rec['score_impact'] > 0
            assert isinstance(rec['tips'], list)
            assert len(rec['tips']) > 0
    
    def test_recommendations_sorted_by_impact(self, sample_rule_results):
        """Test that recommendations are sorted by potential impact"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        impacts = [r['score_impact'] for r in recommendations]
        assert impacts == sorted(impacts, reverse=True), "Should be sorted by score impact"
    
    def test_no_recommendations_for_satisfied_rules(self):
        """Test that satisfied rules don't get recommendations"""
        # Perfect behavioral data
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
        
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            result['rule_results'], result['trust_score']
        )
        
        # Should have few or no recommendations since most rules are satisfied
        assert len(recommendations) <= 3, "Perfect data should have minimal recommendations"
    
    def test_completion_criteria_specific(self, sample_rule_results):
        """Test that completion criteria are specific and actionable"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            criteria = rec['completion_criteria']
            # Should contain specific numbers or thresholds
            assert any(char.isdigit() for char in criteria), \
                f"Completion criteria should contain specific numbers: {criteria}"
            # Should not be vague
            assert 'improve' not in criteria.lower() or 'achieve' in criteria.lower(), \
                "Criteria should be specific, not vague"
    
    def test_verification_methods_present(self, sample_rule_results):
        """Test that verification methods are specified"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            verification = rec['verification']
            assert len(verification) > 20, "Verification should be detailed"
            assert 'verified' in verification.lower() or 'calculated' in verification.lower(), \
                "Should explain how verification works"
    
    def test_tips_are_actionable(self, sample_rule_results):
        """Test that tips are practical and actionable"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            tips = rec['tips']
            assert len(tips) >= 2, "Should have at least 2 tips"
            
            for tip in tips:
                assert len(tip) > 10, "Tips should be detailed"
                # Should contain action verbs
                action_verbs = ['set', 'maintain', 'keep', 'use', 'avoid', 'create', 
                               'increase', 'reduce', 'track', 'document', 'ensure']
                assert any(verb in tip.lower() for verb in action_verbs), \
                    f"Tip should contain action verb: {tip}"
    
    def test_calculate_potential_score(self, sample_rule_results):
        """Test potential score calculation"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        estimated_new_score = CompletionPathwayGenerator.calculate_potential_score(
            current_score, recommendations
        )
        
        # New score should be higher
        assert estimated_new_score > current_score, "Estimated score should be higher"
        # Should not exceed maximum
        assert estimated_new_score <= 860, "Should not exceed maximum score"
        # Should be realistic increase
        increase = estimated_new_score - current_score
        assert increase <= 200, "Increase should be realistic (not more than 200 points)"
    
    def test_gap_calculation_correct(self, sample_rule_results):
        """Test that gap calculations are correct"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            current = rec['current_value']
            target = rec['target_threshold']
            gap = rec['gap']
            
            # For inverse rules (like spending volatility), gap should be positive
            if rec['rule_id'] == 'C1':
                assert gap >= 0, "Gap should be non-negative"
            else:
                # For normal rules, gap should be target - current
                expected_gap = max(0, target - current)
                assert abs(gap - expected_gap) < 0.01, \
                    f"Gap calculation incorrect: {gap} vs {expected_gap}"
    
    def test_timeframe_realistic(self, sample_rule_results):
        """Test that timeframes are realistic"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            timeframe = rec['timeframe']
            # Should contain time unit
            time_units = ['month', 'year', 'week']
            assert any(unit in timeframe.lower() for unit in time_units), \
                f"Timeframe should contain time unit: {timeframe}"
    
    def test_no_ai_ml_terminology(self, sample_rule_results):
        """Test that recommendations don't contain AI/ML terminology"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        forbidden_terms = [
            'ai', 'ml', 'machine learning', 'artificial intelligence',
            'model', 'prediction', 'confidence', 'algorithm', 'could increase'
        ]
        
        for rec in recommendations:
            text_to_check = f"{rec['action']} {rec['description']} {rec['completion_criteria']}"
            text_lower = text_to_check.lower()
            
            for term in forbidden_terms:
                assert term not in text_lower, \
                    f"Found forbidden term '{term}' in recommendation"
    
    def test_score_impact_fixed_not_range(self, sample_rule_results):
        """Test that score impact is a fixed number, not a range"""
        rule_results, current_score = sample_rule_results
        recommendations = CompletionPathwayGenerator.generate_recommendations(
            rule_results, current_score
        )
        
        for rec in recommendations:
            score_impact = rec['score_impact']
            description = rec['description']
            
            # Should be integer
            assert isinstance(score_impact, int), "Score impact should be integer"
            # Should not use vague language
            assert 'could' not in description.lower(), "Should not use 'could increase'"
            assert 'might' not in description.lower(), "Should not use 'might increase'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
