"""empty message

Revision ID: f1e08e874a72
Revises: cf4817911266
Create Date: 2021-12-16 01:02:40.297731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1e08e874a72'
down_revision = 'cf4817911266'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('base_hp', sa.Integer(), nullable=True),
    sa.Column('base_attack', sa.Integer(), nullable=True),
    sa.Column('base_defense', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_user_email', table_name='user')
    op.create_unique_constraint(None, 'user', ['email'])
    op.drop_column('user', 'icon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('icon', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.drop_table('pokemon')
    # ### end Alembic commands ###