"""change 'user' -  one to many - 'confidential_data' and alter fields in confidential_data

Revision ID: 38303cca22c7
Revises: 179517334b7d
Create Date: 2024-08-11 16:49:19.991729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38303cca22c7'
down_revision: Union[str, None] = '179517334b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('confidentialdatas', sa.Column('name', sa.String(length=32), nullable=False))
    op.add_column('confidentialdatas', sa.Column('value', sa.String(length=2048), nullable=False))
    op.drop_column('confidentialdatas', 'tg_query_hashed')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('confidentialdatas', sa.Column('tg_query_hashed', sa.VARCHAR(length=1024), nullable=False))
    op.drop_column('confidentialdatas', 'value')
    op.drop_column('confidentialdatas', 'name')
    # ### end Alembic commands ###
