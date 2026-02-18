"""
Rule-Based Explainability Engine
Generates transparent, deterministic explanations for credit assessments
"""
from typing import List, Dict
from datetime import datetime, timedelta


class ExplainabilityEngine:
    """
    Converts rule evaluation results into user-friendly explanations
    NO AI/ML terminology - Only clear, rule-based language
    """
    
    # Rule-based feature explanations
    RULE_EXPLANATIONS = {
        'A1': {
            'rule_id': 'A1',
            'rule_name': 'Utility Payment Consistency',
            'category': 'Payment Discipline',
            'icon': 'Zap',
            'positive_template': (
                "Rule A1: Utility Payment Consistency\n\n"
                "Your Value: {value} consecutive months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ✓ Rule Satisfied\n\n"
                "You have maintained on-time utility bill payments for {value} consecutive months, "
                "exceeding the required {threshold}-month threshold. This demonstrates consistent payment discipline."
            ),
            'negative_template': (
                "Rule A1: Utility Payment Consistency\n\n"
                "Your Value: {value} consecutive months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your documented utility payment history is {value} months. Maintaining {threshold}+ "
                "consecutive months of on-time payments will satisfy this rule."
            ),
            'insight': (
                "Based on documented financial behavior patterns observed in Indian financial institutions, "
                "this indicator is associated with consistent repayment discipline."
            )
        },
        'A2': {
            'rule_id': 'A2',
            'rule_name': 'Payment Reliability Score',
            'category': 'Payment Discipline',
            'icon': 'CheckCircle2',
            'positive_template': (
                "Rule A2: Payment Reliability Score\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your payment reliability score of {value:.0%} exceeds the required {threshold:.0%} threshold, "
                "demonstrating excellent payment consistency."
            ),
            'negative_template': (
                "Rule A2: Payment Reliability Score\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your payment reliability score is {value:.0%}. Achieving {threshold:.0%}+ consistency "
                "will satisfy this rule."
            ),
            'insight': (
                "Financial institutions in India have documented that individuals maintaining this behavioral "
                "pattern typically demonstrate reliable repayment capacity."
            )
        },
        'B1': {
            'rule_id': 'B1',
            'rule_name': 'Digital Transaction Activity',
            'category': 'Financial Engagement',
            'icon': 'Smartphone',
            'positive_template': (
                "Rule B1: Digital Transaction Activity\n\n"
                "Your Value: {value} transactions/month\n"
                "Required Threshold: {threshold}+ transactions/month\n"
                "Status: ✓ Rule Satisfied\n\n"
                "You maintain {value} regular digital transactions monthly, showing active financial engagement "
                "that exceeds the {threshold} transaction threshold."
            ),
            'negative_template': (
                "Rule B1: Digital Transaction Activity\n\n"
                "Your Value: {value} transactions/month\n"
                "Required Threshold: {threshold}+ transactions/month\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your monthly transaction count is {value}. Increasing to {threshold}+ regular transactions "
                "will satisfy this rule."
            ),
            'insight': (
                "This behavioral indicator has been identified in industry research as a reliable measure "
                "of financial engagement and activity."
            )
        },
        'B2': {
            'rule_id': 'B2',
            'rule_name': 'Transaction Regularity',
            'category': 'Financial Engagement',
            'icon': 'Activity',
            'positive_template': (
                "Rule B2: Transaction Regularity\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your transaction regularity score of {value:.0%} demonstrates consistent financial activity patterns."
            ),
            'negative_template': (
                "Rule B2: Transaction Regularity\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your transaction regularity is {value:.0%}. Achieving {threshold:.0%}+ consistency will satisfy this rule."
            ),
            'insight': (
                "Regular transaction patterns indicate stable financial behavior and predictable cash flow management."
            )
        },
        'C1': {
            'rule_id': 'C1',
            'rule_name': 'Spending Stability',
            'category': 'Financial Discipline',
            'icon': 'TrendingUp',
            'positive_template': (
                "Rule C1: Spending Stability\n\n"
                "Your Value: {value:.1%} volatility\n"
                "Required Threshold: Below {threshold:.1%}\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your spending volatility of {value:.1%} is below the {threshold:.1%} threshold, "
                "indicating excellent financial discipline and predictable spending patterns."
            ),
            'negative_template': (
                "Rule C1: Spending Stability\n\n"
                "Your Value: {value:.1%} volatility\n"
                "Required Threshold: Below {threshold:.1%}\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your spending volatility is {value:.1%}. Reducing volatility below {threshold:.1%} "
                "will satisfy this rule."
            ),
            'insight': (
                "Lower spending volatility indicates better financial planning and budget discipline."
            )
        },
        'C2': {
            'rule_id': 'C2',
            'rule_name': 'Withdrawal Discipline',
            'category': 'Financial Discipline',
            'icon': 'AlertCircle',
            'positive_template': (
                "Rule C2: Withdrawal Discipline\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your withdrawal discipline score of {value:.0%} demonstrates controlled cash management."
            ),
            'negative_template': (
                "Rule C2: Withdrawal Discipline\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your withdrawal discipline is {value:.0%}. Achieving {threshold:.0%}+ will satisfy this rule."
            ),
            'insight': (
                "Disciplined withdrawal patterns indicate better cash flow management and financial planning."
            )
        },
        'D1': {
            'rule_id': 'D1',
            'rule_name': 'Savings Balance Maintenance',
            'category': 'Savings Behavior',
            'icon': 'DollarSign',
            'positive_template': (
                "Rule D1: Savings Balance Maintenance\n\n"
                "Your Value: ₹{value:,.0f}\n"
                "Required Threshold: ₹{threshold:,.0f}+\n"
                "Status: ✓ Rule Satisfied\n\n"
                "You maintain an average month-end balance of ₹{value:,.0f}, exceeding the ₹{threshold:,.0f} threshold "
                "and showing good savings habits."
            ),
            'negative_template': (
                "Rule D1: Savings Balance Maintenance\n\n"
                "Your Value: ₹{value:,.0f}\n"
                "Required Threshold: ₹{threshold:,.0f}+\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your average month-end balance is ₹{value:,.0f}. Building to ₹{threshold:,.0f}+ will satisfy this rule."
            ),
            'insight': (
                "Maintaining consistent savings balances demonstrates financial stability and emergency preparedness."
            )
        },
        'D2': {
            'rule_id': 'D2',
            'rule_name': 'Savings Growth Pattern',
            'category': 'Savings Behavior',
            'icon': 'TrendingUp',
            'positive_template': (
                "Rule D2: Savings Growth Pattern\n\n"
                "Your Value: {value:.1%} monthly growth\n"
                "Required Threshold: {threshold:.1%}+ monthly growth\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your savings are growing at {value:.1%} per month, demonstrating financial progress."
            ),
            'negative_template': (
                "Rule D2: Savings Growth Pattern\n\n"
                "Your Value: {value:.1%} monthly growth\n"
                "Required Threshold: {threshold:.1%}+ monthly growth\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your savings growth rate is {value:.1%}. Achieving {threshold:.1%}+ monthly growth will satisfy this rule."
            ),
            'insight': (
                "Positive savings growth indicates improving financial health and future planning capability."
            )
        },
        'E1': {
            'rule_id': 'E1',
            'rule_name': 'Income Consistency',
            'category': 'Income Stability',
            'icon': 'Briefcase',
            'positive_template': (
                "Rule E1: Income Consistency\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your income regularity score of {value:.0%} demonstrates stable employment and consistent earnings."
            ),
            'negative_template': (
                "Rule E1: Income Consistency\n\n"
                "Your Value: {value:.0%}\n"
                "Required Threshold: {threshold:.0%}+\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your income regularity is {value:.0%}. Achieving {threshold:.0%}+ consistency will satisfy this rule."
            ),
            'insight': (
                "Regular income patterns indicate employment stability and predictable repayment capacity."
            )
        },
        'E2': {
            'rule_id': 'E2',
            'rule_name': 'Income Stability Duration',
            'category': 'Income Stability',
            'icon': 'Clock',
            'positive_template': (
                "Rule E2: Income Stability Duration\n\n"
                "Your Value: {value} months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ✓ Rule Satisfied\n\n"
                "You've maintained stable income for {value} months, exceeding the {threshold}-month threshold."
            ),
            'negative_template': (
                "Rule E2: Income Stability Duration\n\n"
                "Your Value: {value} months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your income stability period is {value} months. Maintaining {threshold}+ months will satisfy this rule."
            ),
            'insight': (
                "Longer income stability periods demonstrate employment security and reliable earning capacity."
            )
        },
        'F1': {
            'rule_id': 'F1',
            'rule_name': 'Account Tenure',
            'category': 'Historical Stability',
            'icon': 'Clock',
            'positive_template': (
                "Rule F1: Account Tenure\n\n"
                "Your Value: {value} months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ✓ Rule Satisfied\n\n"
                "Your account has been active for {value} months, showing long-term financial engagement."
            ),
            'negative_template': (
                "Rule F1: Account Tenure\n\n"
                "Your Value: {value} months\n"
                "Required Threshold: {threshold}+ months\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your account tenure is {value} months. Reaching {threshold}+ months will satisfy this rule."
            ),
            'insight': (
                "Longer account tenure demonstrates sustained financial engagement and relationship stability."
            )
        },
        'F2': {
            'rule_id': 'F2',
            'rule_name': 'Address Stability',
            'category': 'Historical Stability',
            'icon': 'Building2',
            'positive_template': (
                "Rule F2: Address Stability\n\n"
                "Your Value: {value:.1f} years\n"
                "Required Threshold: {threshold:.1f}+ years\n"
                "Status: ✓ Rule Satisfied\n\n"
                "You have resided at your current address for {value:.1f} years, demonstrating residential stability."
            ),
            'negative_template': (
                "Rule F2: Address Stability\n\n"
                "Your Value: {value:.1f} years\n"
                "Required Threshold: {threshold:.1f}+ years\n"
                "Status: ⚠ Threshold Not Met\n\n"
                "Your address stability is {value:.1f} years. Maintaining {threshold:.1f}+ years will satisfy this rule."
            ),
            'insight': (
                "Address stability indicates residential permanence and reduces relocation-related risks."
            )
        }
    }
    
    @staticmethod
    def generate_factors(rule_results: List[Dict], top_n: int = 8) -> List[Dict]:
        """
        Generate user-friendly factor explanations from rule results
        
        Args:
            rule_results: List of rule evaluation results
            top_n: Number of top factors to return
            
        Returns:
            List of factor dictionaries for frontend
        """
        # Sort by points earned (descending) to show most impactful first
        sorted_results = sorted(rule_results, key=lambda x: x['points_earned'], reverse=True)
        
        factors = []
        for idx, result in enumerate(sorted_results[:top_n]):
            rule_id = result['rule_id']
            
            if rule_id not in ExplainabilityEngine.RULE_EXPLANATIONS:
                continue
            
            rule_config = ExplainabilityEngine.RULE_EXPLANATIONS[rule_id]
            
            # Determine factor type
            if result['status'] == 'Fully Satisfied':
                factor_type = 'positive'
                impact = 'High'
            elif result['status'] == 'Partially Satisfied':
                factor_type = 'neutral'
                impact = 'Medium'
            else:
                factor_type = 'negative'
                impact = 'Low'
            
            # Format description
            template = rule_config['positive_template'] if factor_type == 'positive' else rule_config['negative_template']
            description = template.format(
                value=result['user_value'],
                threshold=result['required_threshold']
            )
            
            # Add insight
            description += f"\n\n{rule_config['insight']}"
            
            factors.append({
                'id': idx + 1,
                'rule_id': rule_id,
                'rule_name': rule_config['rule_name'],
                'category': rule_config['category'],
                'type': factor_type,
                'title': f"{rule_config['rule_name']} (Rule {rule_id})",
                'description': description,
                'impact': impact,
                'icon': rule_config['icon'],
                'user_value': result['user_value'],
                'required_threshold': result['required_threshold'],
                'threshold_met': result['threshold_met'],
                'points_earned': result['points_earned'],
                'max_points': result['max_points'],
                'status': result['status']
            })
        
        return factors
    
    @staticmethod
    def generate_rule_summary(rule_results: List[Dict]) -> Dict:
        """
        Generate summary of rule evaluation
        
        Args:
            rule_results: List of rule evaluation results
            
        Returns:
            Dictionary with rule summary statistics
        """
        categories = {}
        for result in rule_results:
            category = result['category']
            if category not in categories:
                categories[category] = {
                    'total_rules': 0,
                    'satisfied': 0,
                    'partial': 0,
                    'not_met': 0,
                    'total_points': 0,
                    'max_points': 0
                }
            
            categories[category]['total_rules'] += 1
            categories[category]['total_points'] += result['points_earned']
            categories[category]['max_points'] += result['max_points']
            
            if result['status'] == 'Fully Satisfied':
                categories[category]['satisfied'] += 1
            elif result['status'] == 'Partially Satisfied':
                categories[category]['partial'] += 1
            else:
                categories[category]['not_met'] += 1
        
        return {
            'by_category': categories,
            'total_rules': len(rule_results),
            'rules_satisfied': sum(1 for r in rule_results if r['status'] == 'Fully Satisfied'),
            'rules_partial': sum(1 for r in rule_results if r['status'] == 'Partially Satisfied'),
            'rules_not_met': sum(1 for r in rule_results if r['status'] == 'Not Satisfied')
        }
