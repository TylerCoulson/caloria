"""Added food/food_category relationship

Revision ID: beaa24779288
Revises: ed8527b42de7
Create Date: 2023-09-07 16:27:50.579527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beaa24779288'
down_revision = 'ed8527b42de7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('food', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('food_category_id_fkey', 'food', type_='foreignkey')
    op.create_foreign_key(None, 'food', 'food_categories', ['category_id'], ['id'], ondelete='CASCADE')
    op.alter_column('food_log', 'serving_amount',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('food_log', 'serving_amount',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.drop_constraint(None, 'food', type_='foreignkey')
    op.create_foreign_key('food_category_id_fkey', 'food', 'food_categories', ['category_id'], ['id'])
    op.alter_column('food', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###