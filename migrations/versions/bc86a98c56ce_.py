"""empty message

Revision ID: bc86a98c56ce
Revises: 555c1ee207e4
Create Date: 2020-02-25 22:26:15.943525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc86a98c56ce'
down_revision = '555c1ee207e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extra_info', sa.Column('telephone', sa.String(length=11), nullable=False))
    op.drop_constraint('extra_info_ibfk_1', 'extra_info', type_='foreignkey')
    op.drop_column('extra_info', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extra_info', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('extra_info_ibfk_1', 'extra_info', 'user', ['user_id'], ['id'])
    op.drop_column('extra_info', 'telephone')
    # ### end Alembic commands ###
