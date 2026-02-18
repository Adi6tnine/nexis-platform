"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('consent_given', sa.Boolean(), nullable=True),
        sa.Column('consent_timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)

    # Behavioral data table
    op.create_table('behavioral_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('utility_payment_months', sa.Integer(), nullable=True),
        sa.Column('utility_payment_consistency', sa.Float(), nullable=True),
        sa.Column('monthly_transaction_count', sa.Integer(), nullable=True),
        sa.Column('transaction_regularity_score', sa.Float(), nullable=True),
        sa.Column('spending_volatility', sa.Float(), nullable=True),
        sa.Column('avg_month_end_balance', sa.Float(), nullable=True),
        sa.Column('savings_growth_rate', sa.Float(), nullable=True),
        sa.Column('withdrawal_discipline_score', sa.Float(), nullable=True),
        sa.Column('income_regularity_score', sa.Float(), nullable=True),
        sa.Column('income_stability_months', sa.Integer(), nullable=True),
        sa.Column('account_tenure_months', sa.Integer(), nullable=True),
        sa.Column('address_stability_years', sa.Float(), nullable=True),
        sa.Column('discretionary_income_ratio', sa.Float(), nullable=True),
        sa.Column('data_collection_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_behavioral_data_user_id'), 'behavioral_data', ['user_id'], unique=False)

    # Credit scores table
    op.create_table('credit_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('trust_score', sa.Integer(), nullable=False),
        sa.Column('risk_level', sa.String(), nullable=False),
        sa.Column('risk_category', sa.String(), nullable=False),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_scores_user_id'), 'credit_scores', ['user_id'], unique=False)

    # Explanations table
    op.create_table('explanations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('score_id', sa.Integer(), nullable=True),
        sa.Column('positive_factors', sa.JSON(), nullable=True),
        sa.Column('neutral_factors', sa.JSON(), nullable=True),
        sa.Column('negative_factors', sa.JSON(), nullable=True),
        sa.Column('shap_values', sa.JSON(), nullable=True),
        sa.Column('feature_values', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_explanations_user_id'), 'explanations', ['user_id'], unique=False)
    op.create_index(op.f('ix_explanations_score_id'), 'explanations', ['score_id'], unique=False)

    # Improvement plans table
    op.create_table('improvement_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('estimated_score_increase', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_improvement_plans_user_id'), 'improvement_plans', ['user_id'], unique=False)

    # Lender decisions table
    op.create_table('lender_decisions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('lender_id', sa.String(), nullable=True),
        sa.Column('ai_recommendation', sa.String(), nullable=True),
        sa.Column('ai_confidence', sa.Float(), nullable=True),
        sa.Column('human_decision', sa.String(), nullable=True),
        sa.Column('decision_justification', sa.Text(), nullable=True),
        sa.Column('loan_amount', sa.Float(), nullable=True),
        sa.Column('interest_rate', sa.Float(), nullable=True),
        sa.Column('term_months', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('decided_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lender_decisions_user_id'), 'lender_decisions', ['user_id'], unique=False)
    op.create_index(op.f('ix_lender_decisions_lender_id'), 'lender_decisions', ['lender_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_lender_decisions_lender_id'), table_name='lender_decisions')
    op.drop_index(op.f('ix_lender_decisions_user_id'), table_name='lender_decisions')
    op.drop_table('lender_decisions')
    op.drop_index(op.f('ix_improvement_plans_user_id'), table_name='improvement_plans')
    op.drop_table('improvement_plans')
    op.drop_index(op.f('ix_explanations_score_id'), table_name='explanations')
    op.drop_index(op.f('ix_explanations_user_id'), table_name='explanations')
    op.drop_table('explanations')
    op.drop_index(op.f('ix_credit_scores_user_id'), table_name='credit_scores')
    op.drop_table('credit_scores')
    op.drop_index(op.f('ix_behavioral_data_user_id'), table_name='behavioral_data')
    op.drop_table('behavioral_data')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
