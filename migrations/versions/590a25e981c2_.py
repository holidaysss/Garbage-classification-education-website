"""empty message

Revision ID: 590a25e981c2
Revises: e694f2a44756
Create Date: 2020-04-22 13:49:58.166249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '590a25e981c2'
down_revision = 'e694f2a44756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sign_in', sa.Column('num', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sign_in', 'num')
    # ### end Alembic commands ###
