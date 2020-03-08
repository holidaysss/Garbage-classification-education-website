"""empty message

Revision ID: 555c1ee207e4
Revises: f4851739c2ee
Create Date: 2020-02-23 21:31:01.467340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '555c1ee207e4'
down_revision = 'f4851739c2ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('extra_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('learn_time', sa.Integer(), nullable=True),
    sa.Column('learn_content', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('extra_info')
    # ### end Alembic commands ###
