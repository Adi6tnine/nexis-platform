"""add authentication fields

Revision ID: 002
Revises: 001
Create Date: 2026-02-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add authentication columns to users table
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='0'))
    op.add_column('users', sa.Column('profile_completed', sa.Boolean(), nullable=True, server_default='0'))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))
    
    # Make consent_timestamp nullable (was server_default before)
    op.alter_column('users', 'consent_timestamp',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    server_default=None)


def downgrade():
    # Remove authentication columns
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'profile_completed')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    
    # Restore consent_timestamp server_default
    op.alter_column('users', 'consent_timestamp',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    server_default=sa.func.now())
