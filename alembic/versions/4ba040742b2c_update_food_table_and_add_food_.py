"""update food table and add food_categories table

Revision ID: 4ba040742b2c
Revises: 4f9488732c9b
Create Date: 2023-06-15 21:29:33.237520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ba040742b2c'
down_revision = '4f9488732c9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('food_categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String)
    )

    op.add_column('food', sa.Column('category', sa.Integer, sa.ForeignKey('food_categories.id')))
    op.add_column('food', sa.Column('type', sa.String))
    op.add_column('food', sa.Column('subtype', sa.String))

    # Remove old columns
    op.drop_column('food', 'brand')
    op.drop_column('food', 'name')



def downgrade() -> None:
    op.add_column('food', sa.Column('brand', sa.String))
    op.add_column('food', sa.Column('name', sa.String))

    op.drop_column('food', 'category')
    op.drop_column('food', 'type')
    op.drop_column('food', 'subtype')


    op.drop_table('food_categories')
