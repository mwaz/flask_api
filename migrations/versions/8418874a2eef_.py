"""empty message

Revision ID: 8418874a2eef
Revises: b04574dee080
Create Date: 2018-01-08 10:53:14.252696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8418874a2eef'
down_revision = 'b04574dee080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auth_token', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auth_token')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=True),
    sa.Column('secret_word', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=256), nullable=False),
    sa.Column('recipe_ingredients', sa.String(length=256), nullable=False),
    sa.Column('recipe_methods', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    op.drop_table('categories')
    op.drop_table('users')
    op.drop_table('token_blacklist')
    # ### end Alembic commands ###
