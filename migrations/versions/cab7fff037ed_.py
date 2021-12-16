"""empty message

Revision ID: cab7fff037ed
Revises: f1e08e874a72
Create Date: 2021-12-16 14:55:31.905512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cab7fff037ed'
down_revision = 'f1e08e874a72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('pokemon', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'pokemon', ['pokemon'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'pokemon')
    # ### end Alembic commands ###
