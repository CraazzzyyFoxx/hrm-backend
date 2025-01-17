"""empty message

Revision ID: f382139dd00f
Revises: 
Create Date: 2024-05-13 21:13:28.530205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f382139dd00f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('citizenship',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_verified_email', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=100), nullable=False),
    sa.Column('password_changed_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('search_status', sa.Enum('active', 'considering', 'offer_thinking', 'going_new', 'not_looking', name='searchstatus'), nullable=False),
    sa.Column('search_region', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('access_token_api',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('token', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('belbin_role',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refresh_token',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('resume',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('is_ready_for_move', sa.Boolean(), nullable=False),
    sa.Column('is_ready_for_trips', sa.Boolean(), nullable=False),
    sa.Column('position', sa.String(length=255), nullable=False),
    sa.Column('salary_from', sa.Integer(), nullable=True),
    sa.Column('salary_to', sa.Integer(), nullable=True),
    sa.Column('busyness', sa.Enum('full', 'part', 'project', 'volunteering', 'internship', name='busyness'), nullable=False),
    sa.Column('work_schedule', sa.Enum('full', 'shift', 'remote', 'flexible', 'duty', name='workschedule'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('belbin_role_entity',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('role_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Enum('chairman', 'closer', 'shaper', 'thinker', 'appraiser', 'collectivist', 'scout', 'executor', name='belbinrole'), nullable=False),
    sa.Column('percent', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['belbin_role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume_basic_info',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('resume_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('middle_name', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', name='gender'), nullable=False),
    sa.Column('birthday', sa.DateTime(), nullable=False),
    sa.Column('citizenship_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['citizenship_id'], ['citizenship.id'], ),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resume_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume_basic_info')
    op.drop_table('belbin_role_entity')
    op.drop_table('resume')
    op.drop_table('refresh_token')
    op.drop_table('belbin_role')
    op.drop_table('access_token_api')
    op.drop_table('user')
    op.drop_table('citizenship')
    # ### end Alembic commands ###
