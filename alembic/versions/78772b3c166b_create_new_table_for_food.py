"""create new table for food

Revision ID: 78772b3c166b
Revises: dc6df7a62e57
Create Date: 2022-10-21 09:11:43.231865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78772b3c166b'
down_revision = 'dc6df7a62e57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('food_menu',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('food_photo', sa.VARCHAR, nullable=False),
                    sa.Column('food_name', sa.VARCHAR, nullable=False),
                    sa.Column('food_price', sa.VARCHAR, nullable=False),
                    sa.Column('food_compound', sa.VARCHAR, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('food_menu')
