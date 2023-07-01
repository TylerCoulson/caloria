"""added food categories table

Revision ID: ed8527b42de7
Revises: 4ba040742b2c
Create Date: 2023-06-30 22:33:28.029664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8527b42de7'
down_revision = '4ba040742b2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'food', 'food_categories', ['category_id'], ['id'])
    op.drop_column('food', 'category')
    op.create_index(op.f('ix_food_categories_id'), 'food_categories', ['id'], unique=False)
    op.alter_column('food_log', 'serving_amount',
               existing_type=sa.INTEGER(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('food_log', 'serving_amount',
               existing_type=sa.Float(precision=2),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_index(op.f('ix_food_categories_id'), table_name='food_categories')
    op.add_column('food', sa.Column('category', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'food', type_='foreignkey')
    op.drop_column('food', 'category_id')
    # ### end Alembic commands ###
