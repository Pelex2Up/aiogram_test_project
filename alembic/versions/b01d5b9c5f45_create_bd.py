"""create bd

Revision ID: b01d5b9c5f45
Revises: 
Create Date: 2022-10-20 10:15:23.359238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b01d5b9c5f45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('f_name', sa.VARCHAR(length=24), nullable=False),
                    sa.Column('date', sa.VARCHAR(length=11), nullable=False),
                    sa.Column('time', sa.VARCHAR(length=5), nullable=False),
                    sa.Column('num_of_ppl', sa.Integer, nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
