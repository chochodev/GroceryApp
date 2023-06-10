"""empty message

Revision ID: 55cc1c140c51
Revises: dcf470257dc0
Create Date: 2023-06-10 08:44:26.242108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55cc1c140c51'
down_revision = 'dcf470257dc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email_verified')

    # ### end Alembic commands ###
