"""update food_log table serving_amount to use float

Revision ID: 4f9488732c9b
Revises: 3f2cea6008b1
Create Date: 2023-04-19 15:58:59.761872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f9488732c9b'
down_revision = '3f2cea6008b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
