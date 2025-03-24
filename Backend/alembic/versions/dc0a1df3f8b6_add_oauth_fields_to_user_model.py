"""Add OAuth fields to User model

Revision ID: dc0a1df3f8b6
Revises: 
Create Date: 2025-03-24 10:32:49.230123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'dc0a1df3f8b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add OAuth-related columns to users table
    op.add_column('users', sa.Column('auth_provider', sa.Enum('LOCAL', 'GOOGLE', 'FACEBOOK', name='authprovider'), nullable=True))
    op.add_column('users', sa.Column('oauth_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_picture', sa.String(length=255), nullable=True))
    
    # Modify existing columns
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('current_timestamp()'))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove OAuth-related columns
    op.drop_column('users', 'profile_picture')
    op.drop_column('users', 'oauth_id')
    op.drop_column('users', 'auth_provider')
    
    # Restore column constraints
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
