"""
Rule-Based Scoring Engine
Deterministic credit trust assessment using predefined behavioral rules
"""
from typing import Dict, List
from datetime import datetime, timedelta


class ScoringEngine:
    """
    Deterministic rule-based scoring engine
    Applies predefined behavioral rules to calculate credit trust assessments
    All calculations are deterministic and fully auditable
    """
    
    # 12 Predefined Behavioral Rules
    RULES = {
        'A1': {
            'name': 'Utility Payment Consistency',
            'category': 'Payment Discipline',
            'thresholds': {'high': 18, 'medium': 12, 'low': 6},
            'points': {'high': 40, 'medium': 30, 'low': 20, 'minimum': 10},
            'field': 'utility_payment_months'
        },
        'A2': {
            'name': 'Payment Reliability Score',
            'category': 'Payment Discipline',
            'thresholds': {'high': 0.90, 'medium': 0.75, 'low': 0.60},
            'points': {'high': 35, 'medium': 25, 'low': 15, 'minimum': 5},
            'field': 'utility_payment_consistency'
        },
        'B1': {
            'name': 'Digital Transaction Activity',
            'category': 'Financial Engagement',
            'thresholds': {'high': 40, 'medium': 25, 'low': 15},
            'points': {'high': 30, 'medium': 20, 'low': 10, 'minimum': 5},
            'field': 'monthly_transaction_count'
        },
        'B2': {
            'name': 'Transaction Regularity',
            'category': 'Financial Engagement',
            'thresholds': {'high': 0.80, 'medium': 0.65, 'low': 0.50},
            'points': {'high': 25, 'medium': 18, 'low': 10, 'minimum': 5},
            'field': 'transaction_regularity_score'
        },
        'C1': {
            'name': 'Spending Stability',
            'category': 'Financial Discipline',
            'thresholds': {'high': 0.15, 'medium': 0.30, 'low': 0.50},  # Lower is better
            'points': {'high': 35, 'medium': 25, 'low': 15, 'minimum': 5},
            'field': 'spending_volatility',
            'inverse': True  # Lower value = higher points
        },
        'C2': {
            'name': 'Withdrawal Discipline',
            'category': 'Financial Discipline',
            'thresholds': {'high': 0.80, 'medium': 0.65, 'low': 0.50},
            'points': {'high': 25, 'medium': 18, 'low': 10, 'minimum': 5},
            'field': 'withdrawal_discipline_score'
        },
        'D1': {
            'name': 'Savings Balance Maintenance',
            'category': 'Savings Behavior',
            'thresholds': {'high': 5000, 'medium': 2500, 'low': 1000},
            'points': {'high': 30, 'medium': 20, 'low': 10, 'minimum': 5},
            'field': 'avg_month_end_balance'
        },
        'D2': {
            'name': 'Savings Growth Pattern',
            'category': 'Savings Behavior',
            'thresholds': {'high': 0.10, 'medium': 0.05, 'low': 0.00},
            'points': {'high': 25, 'medium': 18, 'low': 10, 'minimum': 5},
            'field': 'savings_growth_rate'
        },
        'E1': {
            'name': 'Income Consistency',
            'category': 'Income Stability',
            'thresholds': {'high': 0.85, 'medium': 0.70, 'low': 0.55},
            'points': {'high': 30, 'medium': 20, 'low': 10, 'minimum': 5},
            'field': 'income_regularity_score'
        },
        'E2': {
            'name': 'Income Stability Duration',
            'category': 'Income Stability',
            'thresholds': {'high': 18, 'medium': 12, 'low': 6},
            'points': {'high': 30, 'medium': 20, 'low': 10, 'minimum': 5},
            'field': 'income_stability_months'
        },
        'F1': {
            'name': 'Account Tenure',
            'category': 'Historical Stability',
            'thresholds': {'high': 36, 'medium': 24, 'low': 12},
            'points': {'high': 25, 'medium': 18, 'low': 10, 'minimum': 5},
            'field': 'account_tenure_months'
        },
        'F2': {
            'name': 'Address Stability',
            'category': 'Historical Stability',
            'thresholds': {'high': 3.0, 'medium': 2.0, 'low': 1.0},
            'points': {'high': 20, 'medium': 15, 'low': 8, 'minimum': 3},
            'field': 'address_stability_years'
        }
    }
    
    MAX_POINTS = 360  # Sum of all high points
    SCORE_MIN = 420  # Realistic minimum for demo
    SCORE_MAX = 860  # Realistic maximum for demo
    
    @classmethod
    def calculate_score(cls, behavioral_data: Dict) -> Dict:
        """
        Calculate trust score using deterministic rules
        
        Args:
            behavioral_data: Dictionary of behavioral metrics
            
        Returns:
            Dictionary with score, breakdown, and metadata
        """
        rule_results = []
        total_points = 0
        
        # Apply all 12 rules
        for rule_id, rule_config in cls.RULES.items():
            field = rule_config['field']
            user_value = behavioral_data.get(field, 0)
            
            # Determine points based on thresholds
            if rule_config.get('inverse', False):
                # Lower is better (e.g., spending volatility)
                if user_value <= rule_config['thresholds']['high']:
                    points = rule_config['points']['high']
                    level = 'high'
                elif user_value <= rule_config['thresholds']['medium']:
                    points = rule_config['points']['medium']
                    level = 'medium'
                elif user_value <= rule_config['thresholds']['low']:
                    points = rule_config['points']['low']
                    level = 'low'
                else:
                    points = rule_config['points']['minimum']
                    level = 'minimum'
                
                threshold_met = user_value <= rule_config['thresholds']['medium']
                required_threshold = rule_config['thresholds']['medium']
            else:
                # Higher is better (most rules)
                if user_value >= rule_config['thresholds']['high']:
                    points = rule_config['points']['high']
                    level = 'high'
                elif user_value >= rule_config['thresholds']['medium']:
                    points = rule_config['points']['medium']
                    level = 'medium'
                elif user_value >= rule_config['thresholds']['low']:
                    points = rule_config['points']['low']
                    level = 'low'
                else:
                    points = rule_config['points']['minimum']
                    level = 'minimum'
                
                threshold_met = user_value >= rule_config['thresholds']['medium']
                required_threshold = rule_config['thresholds']['medium']
            
            total_points += points
            
            # Determine status
            if level == 'high':
                status = 'Fully Satisfied'
            elif level in ['medium', 'low']:
                status = 'Partially Satisfied'
            else:
                status = 'Not Satisfied'
            
            rule_results.append({
                'rule_id': rule_id,
                'rule_name': rule_config['name'],
                'category': rule_config['category'],
                'user_value': user_value,
                'required_threshold': required_threshold,
                'threshold_met': threshold_met,
                'points_earned': points,
                'max_points': rule_config['points']['high'],
                'status': status,
                'level': level
            })
        
        # Convert points to score (420-860 range)
        point_ratio = total_points / cls.MAX_POINTS
        score_range = cls.SCORE_MAX - cls.SCORE_MIN
        trust_score = cls.SCORE_MIN + int(point_ratio * score_range)
        
        # Ensure bounds
        trust_score = max(cls.SCORE_MIN, min(cls.SCORE_MAX, trust_score))
        
        # Classify risk
        if trust_score >= 700:
            risk_level = 'Low'
        elif trust_score >= 550:
            risk_level = 'Moderate'
        else:
            risk_level = 'High'
        
        # Count rule satisfaction
        rules_satisfied = sum(1 for r in rule_results if r['status'] == 'Fully Satisfied')
        rules_partial = sum(1 for r in rule_results if r['status'] == 'Partially Satisfied')
        rules_not_met = sum(1 for r in rule_results if r['status'] == 'Not Satisfied')
        
        return {
            'trust_score': trust_score,
            'risk_level': risk_level,
            'total_points': total_points,
            'max_points': cls.MAX_POINTS,
            'rule_results': rule_results,
            'rules_evaluated': len(rule_results),
            'rules_satisfied': rules_satisfied,
            'rules_partial': rules_partial,
            'rules_not_met': rules_not_met
        }
    
    @classmethod
    def get_assessment_strength(cls, behavioral_data: Dict, documentation_months: int) -> str:
        """
        Calculate assessment strength based on data quality
        
        Args:
            behavioral_data: Dictionary of behavioral metrics
            documentation_months: Months of documented behavior
            
        Returns:
            Assessment strength: 'Strong', 'Moderate', or 'Weak'
        """
        # Calculate data completeness
        required_fields = [rule['field'] for rule in cls.RULES.values()]
        provided_fields = sum(1 for field in required_fields if behavioral_data.get(field, 0) > 0)
        data_completeness = provided_fields / len(required_fields)
        
        # Strong: 18+ months, 95%+ data, all rules applicable
        if documentation_months >= 18 and data_completeness >= 0.95:
            return 'Strong'
        
        # Moderate: 12-17 months, 80%+ data
        elif documentation_months >= 12 and data_completeness >= 0.80:
            return 'Moderate'
        
        # Weak: Less than above
        else:
            return 'Weak'
    
    @classmethod
    def get_rule_match_level(cls, rules_satisfied: int, total_rules: int) -> str:
        """
        Calculate rule match level
        
        Args:
            rules_satisfied: Number of rules fully satisfied
            total_rules: Total number of rules evaluated
            
        Returns:
            Match level: 'High', 'Medium', or 'Low'
        """
        satisfaction_rate = rules_satisfied / total_rules if total_rules > 0 else 0
        
        if satisfaction_rate >= 0.80:
            return 'High'
        elif satisfaction_rate >= 0.50:
            return 'Medium'
        else:
            return 'Low'
