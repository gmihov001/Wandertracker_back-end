"""empty message

Revision ID: 14ea34e418ac
Revises: 05ac944e030f
Create Date: 2019-11-20 14:04:37.099772

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '14ea34e418ac'
down_revision = '05ac944e030f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emergengy_contac',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=2000), nullable=False),
    sa.Column('phone_number', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('stamp', 'country_label',
               existing_type=mysql.VARCHAR(length=500),
               nullable=False)
    op.alter_column('stamp', 'country_value',
               existing_type=mysql.VARCHAR(length=5),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stamp', 'country_value',
               existing_type=mysql.VARCHAR(length=5),
               nullable=True)
    op.alter_column('stamp', 'country_label',
               existing_type=mysql.VARCHAR(length=500),
               nullable=True)
    op.drop_table('emergengy_contac')
    # ### end Alembic commands ###
