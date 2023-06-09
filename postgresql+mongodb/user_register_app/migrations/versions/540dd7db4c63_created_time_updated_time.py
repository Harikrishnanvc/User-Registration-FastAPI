"""created_time & updated_time

Revision ID: 540dd7db4c63
Revises: d3b710f6a46f
Create Date: 2023-05-13 19:20:51.715786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '540dd7db4c63'
down_revision = 'd3b710f6a46f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_registration', sa.Column('created_time', sa.DateTime(), nullable=True))
    op.add_column('user_registration', sa.Column('updated_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_registration', 'updated_time')
    op.drop_column('user_registration', 'created_time')
    # ### end Alembic commands ###
