"""delete duplicates

Revision ID: f8c5aa396f6c
Revises: c3716af7b36d
Create Date: 2023-05-13 19:11:46.597775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c5aa396f6c'
down_revision = 'c3716af7b36d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_registration_phone_key', 'user_registration', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_registration_phone_key', 'user_registration', ['phone'])
    # ### end Alembic commands ###
