"""Cambio en insituto model

Revision ID: 53ee9f3b028a
Revises: 
Create Date: 2022-10-25 16:47:29.862569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ee9f3b028a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instituto', sa.Column('clave', sa.String(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instituto', 'clave')
    # ### end Alembic commands ###
