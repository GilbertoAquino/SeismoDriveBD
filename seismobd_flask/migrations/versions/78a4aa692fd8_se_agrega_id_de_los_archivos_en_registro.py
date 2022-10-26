"""Se agrega id de los archivos en registro

Revision ID: 78a4aa692fd8
Revises: 5cc269740fab
Create Date: 2022-10-25 18:30:07.327752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a4aa692fd8'
down_revision = '5cc269740fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estacion', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['clave'])

    with op.batch_alter_table('instituto', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['clave'])

    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_archivo', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.drop_column('id_archivo')

    with op.batch_alter_table('instituto', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('estacion', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
