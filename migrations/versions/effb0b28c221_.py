"""empty message

Revision ID: effb0b28c221
Revises: cab7fff037ed
Create Date: 2021-12-16 15:37:45.523901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'effb0b28c221'
down_revision = 'cab7fff037ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('pokemon_id', sa.Integer(), nullable=True))
    op.drop_constraint('user_pokemon_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'pokemon', ['pokemon_id'], ['id'])
    op.drop_column('user', 'pokemon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('pokemon', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_pokemon_fkey', 'user', 'pokemon', ['pokemon'], ['id'])
    op.drop_column('user', 'pokemon_id')
    # ### end Alembic commands ###
