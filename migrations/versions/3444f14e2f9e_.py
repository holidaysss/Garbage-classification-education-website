"""empty message

Revision ID: 3444f14e2f9e
Revises: bc86a98c56ce
Create Date: 2020-02-28 19:54:12.695128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3444f14e2f9e'
down_revision = 'bc86a98c56ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('learn_content', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('learn_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'learn_time')
    op.drop_column('user', 'learn_content')
    # ### end Alembic commands ###
