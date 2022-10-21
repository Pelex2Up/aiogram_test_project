"""upgrade columns

Revision ID: cc6c0a445ffb
Revises: b01d5b9c5f45
Create Date: 2022-10-20 11:53:15.557654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc6c0a445ffb'
down_revision = 'b01d5b9c5f45'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users_booking',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('f_name', sa.VARCHAR(length=24), nullable=False),
                    sa.Column('l_name', sa.VARCHAR(length=24), nullable=False),
                    sa.Column('date', sa.VARCHAR(length=11), nullable=False),
                    sa.Column('time', sa.VARCHAR(length=5), nullable=False),
                    sa.Column('num_of_ppl', sa.Integer, nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users_booking')