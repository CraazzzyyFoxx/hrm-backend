"""empty message

Revision ID: 2903e218fad5
Revises: 0e041d52f539
Create Date: 2024-05-14 06:08:36.792446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2903e218fad5'
down_revision: Union[str, None] = '0e041d52f539'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(' Resume_work_experience',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('resume_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('position', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('start_work_month', sa.String(length=255), nullable=False),
    sa.Column('start_work_year', sa.Integer(), nullable=False),
    sa.Column('is_end', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resume_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(' Resume_work_experience')
    # ### end Alembic commands ###
