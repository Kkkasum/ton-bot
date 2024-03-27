"""empty message

Revision ID: a128f4b79865
Revises: 
Create Date: 2024-03-27 00:15:17.381167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a128f4b79865'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category', sa.Enum('wallet', 'defi', 'nft', 'gamefi', 'viewer', 'utils', name='appcategory'), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('tg_links', sa.String(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_apps_name'), 'apps', ['name'], unique=True)
    op.create_table('jettons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=16), nullable=False),
    sa.Column('master_address', sa.String(length=66), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('master_address')
    )
    op.create_index(op.f('ix_jettons_symbol'), 'jettons', ['symbol'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jettons_symbol'), table_name='jettons')
    op.drop_table('jettons')
    op.drop_index(op.f('ix_apps_name'), table_name='apps')
    op.drop_table('apps')
    # ### end Alembic commands ###