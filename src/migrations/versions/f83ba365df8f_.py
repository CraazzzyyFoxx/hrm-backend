"""empty message

Revision ID: f83ba365df8f
Revises: f382139dd00f
Create Date: 2024-05-14 01:40:44.977818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f83ba365df8f'
down_revision: Union[str, None] = 'f382139dd00f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume_basic_info', sa.Column('city', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resume_basic_info', 'city')
    # ### end Alembic commands ###
