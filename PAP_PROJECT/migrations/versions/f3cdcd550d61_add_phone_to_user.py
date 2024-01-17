"""Add phone to User

Revision ID: f3cdcd550d61
Revises: b03737fc3dbc
Create Date: 2023-12-19 05:01:33.727310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3cdcd550d61'
down_revision = 'b03737fc3dbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)

    # ### end Alembic commands ###