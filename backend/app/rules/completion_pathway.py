"""
Rule Completion Pathway Generator
Provides actionable steps to satisfy unmet or partially met rules
"""
from typing import List, Dict


class CompletionPathwayGenerator:
    """
    Generates personalized pathways to complete unmet rules
    All recommendations are specific, actionable, and verifiable
    """
    
    # Rule completion guidance
    RULE_GUIDANCE = {
        'A1': {
            'action': 'Extend Utility Payment History',
            'completion_criteria': 'Maintain on-time utility payments for {gap} additional consecutive months',
            'verification': 'Utility bill payment records will be verified through Account Aggregator framework',
            'tips': [
                'Set up auto-pay for electricity and water bills',
                'Maintain sufficient balance before due dates',
                'Keep digital payment receipts for verification'
            ]
        },
        'A2': {
            'action': 'Improve Payment Reliability',
            'completion_criteria': 'Achieve {target_threshold:.0%} payment consistency over next {gap} months',
            'verification': 'Payment consistency calculated from utility and subscription payment records',
            'tips': [
                'Never miss payment due dates',
                'Set calendar reminders 3 days before due dates',
                'Use automatic payment methods where available'
            ]
        },
        'B1': {
            'action': 'Increase Digital Transaction Activity',
            'completion_criteria': 'Maintain {target_threshold}+ digital transactions monthly for {gap} months',
            'verification': 'Transaction count verified through bank statement and UPI records',
            'tips': [
                'Use UPI for daily purchases instead of cash',
                'Pay bills digitally (mobile, DTH, utilities)',
                'Use digital wallets for regular expenses'
            ]
        },
        'B2': {
            'action': 'Establish Transaction Regularity',
            'completion_criteria': 'Achieve {target_threshold:.0%} transaction regularity over {gap} months',
            'verification': 'Regularity score calculated from transaction timing patterns',
            'tips': [
                'Maintain consistent monthly spending patterns',
                'Avoid large irregular transactions',
                'Spread purchases evenly throughout the month'
            ]
        },
        'C1': {
            'action': 'Reduce Spending Volatility',
            'completion_criteria': 'Maintain spending volatility below {target_threshold:.1%} for {gap} months',
            'verification': 'Volatility calculated from monthly spending variance',
            'tips': [
                'Create and follow a monthly budget',
                'Avoid impulsive large purchases',
                'Plan major expenses in advance'
            ]
        },
        'C2': {
            'action': 'Improve Withdrawal Discipline',
            'completion_criteria': 'Achieve {target_threshold:.0%} withdrawal discipline score over {gap} months',
            'verification': 'Discipline score based on withdrawal frequency and timing patterns',
            'tips': [
                'Limit ATM withdrawals to planned amounts',
                'Avoid frequent small withdrawals',
                'Maintain minimum balance consistently'
            ]
        },
        'D1': {
            'action': 'Build Savings Balance',
            'completion_criteria': 'Maintain average month-end balance of ₹{target_threshold:,.0f}+ for {gap} months',
            'verification': 'Balance verified from bank statements at month-end',
            'tips': [
                'Set up automatic savings transfer on salary day',
                'Reduce discretionary spending by 10-15%',
                'Keep emergency fund separate from spending account'
            ]
        },
        'D2': {
            'action': 'Establish Savings Growth',
            'completion_criteria': 'Achieve {target_threshold:.1%}+ monthly savings growth for {gap} months',
            'verification': 'Growth rate calculated from month-over-month balance changes',
            'tips': [
                'Increase savings amount by small increments monthly',
                'Deposit bonuses and extra income into savings',
                'Track savings progress weekly'
            ]
        },
        'E1': {
            'action': 'Stabilize Income Pattern',
            'completion_criteria': 'Achieve {target_threshold:.0%} income regularity over {gap} months',
            'verification': 'Regularity calculated from income deposit timing and amounts',
            'tips': [
                'Maintain consistent employment',
                'Document all income sources',
                'Ensure salary credits on regular schedule'
            ]
        },
        'E2': {
            'action': 'Extend Income Stability Duration',
            'completion_criteria': 'Maintain stable income for {gap} additional months',
            'verification': 'Stability verified through consistent salary credits',
            'tips': [
                'Continue current employment',
                'Document income through bank statements',
                'Maintain regular income deposit patterns'
            ]
        },
        'F1': {
            'action': 'Build Account History',
            'completion_criteria': 'Maintain active account for {gap} additional months',
            'verification': 'Tenure verified from account opening date',
            'tips': [
                'Keep account active with regular transactions',
                'Maintain minimum balance requirements',
                'Use account for primary financial activities'
            ]
        },
        'F2': {
            'action': 'Establish Address Stability',
            'completion_criteria': 'Maintain current address for {gap} additional months',
            'verification': 'Address verified through utility bills and bank records',
            'tips': [
                'Update address on all financial accounts',
                'Maintain utility connections at current address',
                'Keep address proof documents current'
            ]
        }
    }
    
    @staticmethod
    def generate_recommendations(rule_results: List[Dict], current_score: int) -> List[Dict]:
        """
        Generate actionable recommendations for unmet or partially met rules
        
        Args:
            rule_results: List of rule evaluation results
            current_score: Current trust score
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Focus on rules that are not fully satisfied
        improvable_rules = [
            r for r in rule_results 
            if r['status'] in ['Partially Satisfied', 'Not Satisfied']
        ]
        
        # Sort by potential impact (max_points - points_earned)
        improvable_rules.sort(
            key=lambda x: x['max_points'] - x['points_earned'],
            reverse=True
        )
        
        for result in improvable_rules:
            rule_id = result['rule_id']
            
            if rule_id not in CompletionPathwayGenerator.RULE_GUIDANCE:
                continue
            
            guidance = CompletionPathwayGenerator.RULE_GUIDANCE[rule_id]
            
            # Calculate gap
            current_value = result['user_value']
            target_threshold = result['required_threshold']
            
            # Determine if inverse rule (lower is better)
            if rule_id == 'C1':  # Spending volatility
                gap = current_value - target_threshold
                gap_unit = 'percentage points'
            elif rule_id in ['A1', 'E2', 'F1']:  # Month-based rules
                gap = max(0, target_threshold - current_value)
                gap_unit = 'months'
            elif rule_id == 'F2':  # Year-based rule
                gap = max(0, target_threshold - current_value)
                gap_unit = 'years'
            elif rule_id == 'D1':  # Balance-based rule
                gap = max(0, target_threshold - current_value)
                gap_unit = 'rupees'
            else:  # Percentage-based rules
                gap = max(0, target_threshold - current_value)
                gap_unit = 'percentage points'
            
            # Calculate score impact (potential points gain)
            score_impact = result['max_points'] - result['points_earned']
            
            # Estimate timeframe
            if rule_id in ['A1', 'E2', 'F1', 'F2']:
                # Time-based rules: gap is the timeframe
                timeframe = f"{int(gap)} {gap_unit}"
                difficulty = 'Easy' if gap <= 6 else 'Medium' if gap <= 12 else 'Hard'
            elif rule_id in ['D1', 'D2']:
                # Savings rules: 3-6 months typically
                timeframe = "3-6 months"
                difficulty = 'Medium'
            else:
                # Behavioral rules: 2-4 months typically
                timeframe = "2-4 months"
                difficulty = 'Easy' if score_impact <= 15 else 'Medium'
            
            # Format completion criteria
            completion_criteria = guidance['completion_criteria'].format(
                gap=int(gap) if gap_unit in ['months', 'years'] else gap,
                target_threshold=target_threshold
            )
            
            recommendations.append({
                'rule_id': rule_id,
                'rule_name': result['rule_name'],
                'action': guidance['action'],
                'description': f"Currently at {current_value}, target is {target_threshold}",
                'current_value': current_value,
                'target_threshold': target_threshold,
                'gap': gap,
                'gap_unit': gap_unit,
                'score_impact': score_impact,
                'timeframe': timeframe,
                'difficulty': difficulty,
                'category': result['category'],
                'status': 'Recommended',
                'completion_criteria': completion_criteria,
                'verification': guidance['verification'],
                'tips': guidance['tips']
            })
        
        return recommendations
    
    @staticmethod
    def calculate_potential_score(current_score: int, recommendations: List[Dict]) -> int:
        """
        Calculate potential score if all recommendations are completed
        
        Args:
            current_score: Current trust score
            recommendations: List of recommendations
            
        Returns:
            Estimated new score
        """
        total_potential_increase = sum(r['score_impact'] for r in recommendations)
        
        # Convert points to score increase (approximate)
        # 360 max points = 440 score range (420-860)
        score_per_point = 440 / 360
        estimated_increase = int(total_potential_increase * score_per_point)
        
        # Cap at maximum score
        estimated_new_score = min(860, current_score + estimated_increase)
        
        return estimated_new_score
